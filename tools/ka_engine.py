"""knowledge-archaeology 确定性逻辑引擎（CI 各层共享）。

本模块承载 Skill 的"可测试规则"——所有被 CI 验证的确定性逻辑都集中在这里。
设计原则：
- 纯函数、无副作用、可单测
- 规则来源：contracts/knowledge-schema.md + contracts/epistemic-status.md + contracts/ek-graph-schema.md
- 规则阈值统一从 rules/*.json 权威规则集加载，禁止在代码里硬编码
- 本文件是 Layer 2 Deterministic Unit Tests 的直接测试对象
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
RULES_DIR = REPO_ROOT / "rules"


# ---------------------------------------------------------------------------
# 规则集加载（权威规则集 = rules/*.json，替代硬编码）
# ---------------------------------------------------------------------------

_rules_cache: Dict[str, dict] = {}


def load_rules_file(name: str) -> dict:
    """加载 rules/<name>.json。带缓存；文件缺失时返回 {}（调用方负责默认值/报错）。"""
    if name in _rules_cache:
        return _rules_cache[name]
    path = RULES_DIR / f"{name}.json"
    data: dict = {}
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
    _rules_cache[name] = data
    return data


def get_promotion_gate() -> dict:
    """Promotion Gate 硬门槛（rules/quality-gates.json → promotion_gate）。"""
    return load_rules_file("quality-gates").get("promotion_gate", {})


def get_promotion_rules() -> dict:
    """晋升确定性规则（rules/promotion-rules.json → rules）。"""
    return load_rules_file("promotion-rules").get("rules", {})


def get_ek_graph_rules() -> dict:
    """EK Graph 质量规则（rules/ek-graph-rules.json → ek_graph_gates）。"""
    return load_rules_file("ek-graph-rules").get("ek_graph_gates", {})


def get_ideal_ratio() -> dict:
    """三层配比（rules/ek-graph-rules.json → ideal_ratio）。"""
    return load_rules_file("ek-graph-rules").get("ideal_ratio", {})


def get_risk_rules() -> dict:
    """自动合并风险分级（rules/risk-paths.json）。"""
    return load_rules_file("risk-paths")


# ---------------------------------------------------------------------------
# 合法枚举（从 contracts/*.md 提取，Layer 1 Contract Tests 也引用）
# ---------------------------------------------------------------------------

VALID_ABSTRACTION_LEVELS = ["L0", "L1", "L2", "L3", "L4", "L5"]
VALID_KNOWLEDGE_LAYERS = ["engineering", "generalized"]
VALID_EPISTEMIC_STATUS = [
    "Fact", "Observation", "Hypothesis", "Validated Pattern", "Principle", "Law",
]
VALID_VALUES = ["A", "B", "C", "D", "E"]
VALID_CATEGORIES = [
    "PRODUCT", "ARCHITECTURE", "ENGINEERING", "DESIGN", "AGENT", "RUNTIME",
    "MEMORY", "CONTEXT", "PERMISSION", "TESTING", "EVALUATION", "TOOLING",
    "WORKFLOW", "DECISION", "FAILURE", "EXPERIMENT", "PATTERN", "PRINCIPLE",
    "METHODOLOGY",
]
VALID_FLOW_TYPES = [
    "control", "state", "data", "evidence", "authority", "memory", "policy",
]
VALID_EK_EDGE_TYPES = [
    "mechanism", "subsystem", "causal", "dependency", "constraint", "contrast",
]
VALID_AGGREGATION_RULES = ["R1", "R2", "R3", "R4"]
VALID_CONFIDENCE = ["high", "medium", "low"]
VALID_AGENTS = [
    "repository-mapper", "code-analyst", "doc-analyst", "test-analyst",
    "failure-analyst", "authority-analyst", "policy-governance-analyst",
    "problem-miner", "decision-miner", "pattern-miner", "flow-miner",
    "engineering-knowledge-miner", "knowledge-synthesizer",
    "truth-auditor", "coverage-auditor", "flow-auditor",
    "abstraction-auditor", "counterexample-hunter", "epistemic-auditor",
    "reconciler",
]
# 文档约定的理想配比（宽底座 + 窄尖顶）——从 rules/ek-graph-rules.json 加载
IDEAL_RATIO = get_ideal_ratio()
# EK Graph 质量门（v3.1）——从 rules/ek-graph-rules.json 加载
EK_GRAPH_GATES = get_ek_graph_rules()


# ---------------------------------------------------------------------------
# 知识对象校验（Layer 1 Contract）
# ---------------------------------------------------------------------------

@dataclass
class ValidationIssue:
    path: str
    message: str
    severity: str = "error"  # error / warning


def validate_knowledge_object(ko: Dict[str, Any], path: str = "KO") -> List[ValidationIssue]:
    """校验单个 Knowledge Object 是否符合 contracts/knowledge-schema.md。

    返回 issue 列表；空列表 = 通过。
    """
    issues: List[ValidationIssue] = []

    def err(msg: str) -> None:
        issues.append(ValidationIssue(path=path, message=msg, severity="error"))

    def warn(msg: str) -> None:
        issues.append(ValidationIssue(path=path, message=msg, severity="warning"))

    # 必需字段
    for req in ["knowledge_layer", "claim", "category", "abstraction", "value",
                "epistemic_status", "derivation", "evidence", "scope", "confidence"]:
        if req not in ko:
            err(f"缺少必需字段: {req}")

    if "knowledge_layer" in ko and ko["knowledge_layer"] not in VALID_KNOWLEDGE_LAYERS:
        err(f"knowledge_layer 非法: {ko['knowledge_layer']}（合法: {VALID_KNOWLEDGE_LAYERS}）")

    if "abstraction" in ko and ko["abstraction"] not in VALID_ABSTRACTION_LEVELS:
        err(f"abstraction 非法: {ko['abstraction']}（合法: {VALID_ABSTRACTION_LEVELS}）")

    if "value" in ko and ko["value"] not in VALID_VALUES:
        err(f"value 非法: {ko['value']}（合法: {VALID_VALUES}）")

    if "category" in ko and ko["category"] not in VALID_CATEGORIES:
        err(f"category 非法: {ko['category']}")

    if "epistemic_status" in ko and ko["epistemic_status"] not in VALID_EPISTEMIC_STATUS:
        err(f"epistemic_status 非法: {ko['epistemic_status']}（合法: {VALID_EPISTEMIC_STATUS}）")

    if "confidence" in ko and ko["confidence"] not in VALID_CONFIDENCE:
        err(f"confidence 非法: {ko['confidence']}")

    # 层-抽象级一致性（knowledge-schema.md §knowledge_layer 语义）
    layer = ko.get("knowledge_layer")
    abstraction = ko.get("abstraction")
    if layer and abstraction:
        if layer == "engineering" and abstraction.startswith("L3"):
            err(f"engineering 层不允许 L3+ 抽象（当前 {abstraction}）——工程层是 L0/L1/L2 底座")
        if layer == "generalized" and abstraction in ("L0", "L1"):
            err(f"generalized 层不允许 L0/L1 抽象（当前 {abstraction}）——认知层是 L3/L4/L5")

    # 层-认知状态一致性
    if abstraction in ("L4", "L5") and layer == "generalized":
        status = ko.get("epistemic_status")
        if status in ("Hypothesis", "Observation"):
            err(f"L4/L5 抽象不能是 {status}——高抽象层必须有 Validated Pattern 以上状态支撑")
        if status == "Law":
            # Law 需要 S8 跨项目验证，标记 warning（仅凭本项目 KO 无法自证）
            warn("Law 状态需要 S8 跨项目验证，单项目 KO 无法自证")

    # 高抽象必须有 promotion 论证（abstraction > L3 铁律）
    if abstraction in ("L4", "L5"):
        promo = (ko.get("derivation") or {}).get("promotion_arguments")
        if not promo:
            err(f"{abstraction} 抽象必须有 derivation.promotion_arguments（Abstraction Promotion Gate）")
        elif isinstance(promo, list) and len(promo) == 0:
            err(f"{abstraction} 抽象必须有 derivation.promotion_arguments（Abstraction Promotion Gate）")

    # v3.1 铁律：generalized 必须有 aggregation_rule
    if layer == "generalized":
        if "aggregation_rule" not in ko:
            err("generalized 对象必须声明 aggregation_rule（v3.1：KO 不是手工挑选的 EK 列表）")
        else:
            ar = ko["aggregation_rule"]
            if ar.get("rule") not in VALID_AGGREGATION_RULES:
                err(f"aggregation_rule.rule 非法: {ar.get('rule')}（合法: R1/R2/R3/R4）")
            cluster = ar.get("cluster_eks", [])
            if not cluster:
                err("aggregation_rule.cluster_eks 不能为空——簇内 EK 必须明确")
            # 反退化铁律：聚合理由不能是"同子系统"（分类不是知识）
            naming = ar.get("naming", "").lower()
            if any(phrase in naming for phrase in ["同子系统", "同属一个子系统", "都属于", "同一分类", "模块说明"]):
                err(f"聚合理由是'同子系统'式分类，不是知识聚合: {ar.get('naming')}")

    # v3.1 铁律：engineering 必须有 links
    if layer == "engineering" and "links" not in ko:
        err("engineering 对象必须声明 links（v3.1：EK 是图的节点，不能孤立）")
    if layer == "engineering" and ko.get("links") == []:
        err("engineering 对象 links 不能为空列表——孤立 EK 要么被连接，要么降级 D 级")

    # links 边类型校验
    for link in ko.get("links", []) or []:
        if link.get("type") not in VALID_EK_EDGE_TYPES:
            err(f"links 边类型非法: {link.get('type')}（合法: {VALID_EK_EDGE_TYPES}）")
        if not link.get("to"):
            err("links 必须指向具体 EK（to 字段不能为空）")

    # flows 校验（v2：flow_traceability 非空）
    if "flows" in ko and isinstance(ko["flows"], dict):
        for ft in ko["flows"]:
            if ft not in VALID_FLOW_TYPES:
                err(f"flows 键非法: {ft}（合法: {VALID_FLOW_TYPES}）")
    if layer == "generalized":
        if not ko.get("flow_traceability"):
            warn("generalized 对象建议声明 flow_traceability（Flow→KO 交叉校验门）")

    # provenance
    if "provenance" not in ko:
        err("缺少 provenance（谁发现/支持/反对）")
    else:
        pv = ko["provenance"]
        if pv.get("discovered_by") and pv["discovered_by"] not in VALID_AGENTS:
            err(f"provenance.discovered_by 非法角色: {pv['discovered_by']}")

    # v3 铁律：generalized 必须有 derivation.facts 回溯到底座
    if layer == "generalized":
        facts = (ko.get("derivation") or {}).get("facts", [])
        if not facts:
            err("generalized 对象必须通过 derivation.facts 回溯到 engineering 底座（无底座 = 悬空升维）")

    # validation.blind_reconstruction（v2 铁律）
    val = ko.get("validation") or {}
    if val.get("blind_reconstruction") == "not_performed":
        err("validation.blind_reconstruction 必须为 performed，否则验证结果无效")

    return issues


# ---------------------------------------------------------------------------
# Epistemic Promotion（Layer 2 核心确定性逻辑）
# ---------------------------------------------------------------------------

@dataclass
class PromotionInput:
    """晋升判定输入（来自 evidence 层）。"""
    evidence_count: int = 0
    independent_instances: int = 0      # 独立出现次数（跨模块/跨流）
    different_modules: int = 0          # 涉及不同模块/子系统数
    cross_context: bool = False         # 是否跨上下文（如核心流 + Agent 流都出现）
    cross_project: bool = False         # 是否跨项目验证（S8）
    human_confirmed: bool = False       # 是否人工确认（S7）
    runtime_validated: bool = False     # 是否运行时验证（S5/S6）
    test_validated: bool = False        # 是否测试验证（S4）
    counterexamples_found: int = 0      # 反例数（counterexample-hunter 预算）
    observed_structure_only: bool = False  # 是否仅 Observed Structure（无 Pattern 依据）


def compute_max_abstraction(pi: PromotionInput) -> str:
    """根据证据强度计算允许的最高抽象层（确定性规则）。

    规则来源：rules/promotion-rules.json（权威规则集，勿在此硬编码阈值）
    核心原则：
    - 单实例、无跨上下文 → 最高 L2（工程知识）
    - 有重复结构（≥2 独立实例）→ L3（Pattern），但需 ≥2 独立模块
    - L4（Cognitive Model）需要跨上下文 + 运行时/人工验证 + 无反例
    - L5（Methodology）需要跨项目验证（S8）或人类确认 + 强证据
    - 反例存在 → 降级；counterexample 预算未满足 → 不得升 L3+
    """
    pr = get_promotion_rules()
    cb_blocks_above = pr.get("counterexample_blocks_above", "L2")
    l3_req = pr.get("l3_requires", {"independent_instances_min": 2, "different_modules_min": 2})
    l4_req = pr.get("l4_requires", {})
    l5_req = pr.get("l5_requires", {})

    # 反例压制：任何反例都禁止升到 L3+
    if pi.counterexamples_found > 0:
        return cb_blocks_above

    # 反例预算：L3+ 必须有 ≥3 反例攻击记录（counterexample-hunter 预算制）
    # 该检查由调用方传入 budget_satisfied；此处用 counterexamples_found 表示已执行搜索，
    # 无法区分"搜索了 0 个"和"没搜"。调用方负责传 budget 信息。

    # 跨项目验证 → 允许 L5（但仍需强证据）
    if (pi.cross_project and pi.runtime_validated and pi.counterexamples_found == 0
            and l5_req.get("cross_project", True)):
        return "L5"

    # 人工确认 + 运行时 + 跨上下文 → L4
    if (pi.human_confirmed and pi.runtime_validated and pi.cross_context
            and pi.independent_instances >= l4_req.get("independent_instances_min", 2)
            and pi.counterexamples_found == 0):
        return "L4"

    # 跨上下文 + 运行时验证（无人工）→ L3（Pattern 已成型，但无 L4 稳定关系）
    if (pi.cross_context and pi.runtime_validated
            and pi.independent_instances >= l3_req.get("independent_instances_min", 2)
            and pi.counterexamples_found == 0):
        return "L3"

    # 重复结构（≥2 独立实例 + ≥2 不同模块）→ L3（Pattern）
    if (pi.independent_instances >= l3_req.get("independent_instances_min", 2)
            and pi.different_modules >= l3_req.get("different_modules_min", 2)
            and pi.counterexamples_found == 0):
        return "L3"

    # 单实例但跨上下文 → 观察到的结构（Observed Structure），不升 Pattern
    if pi.cross_context and pi.independent_instances < l3_req.get("independent_instances_min", 2):
        return pr.get("observed_structure_max", "L2")

    # 单一实现 + 解释因果 → L2（工程知识）
    if pi.evidence_count >= 1:
        return pr.get("single_implementation_max", "L2")

    # 纯描述 → L1
    return pr.get("pure_description_max", "L1")


def check_promotion_legitimacy(pi: PromotionInput, claimed_level: str) -> Dict[str, Any]:
    """判断某个 claim 声称的抽象级是否被证据支持（Abstraction Promotion Gate）。

    返回:
      {"allowed": bool, "max_allowed": str, "reason": str}
    """
    max_allowed = compute_max_abstraction(pi)
    level_rank = {"L1": 1, "L2": 2, "L3": 3, "L4": 4, "L5": 5}
    if level_rank[claimed_level] <= level_rank[max_allowed]:
        return {"allowed": True, "max_allowed": max_allowed,
                "reason": f"claim {claimed_level} ≤ max_allowed {max_allowed}，晋升合法"}
    return {"allowed": False, "max_allowed": max_allowed,
            "reason": f"claim {claimed_level} > max_allowed {max_allowed}——证据不足，须降级（Abstraction Promotion Gate）"}


# ---------------------------------------------------------------------------
# EK Graph 与聚合规则（v3.1 核心确定性逻辑）
# ---------------------------------------------------------------------------

def validate_ek_graph(eks: List[Dict[str, Any]], kos: List[Dict[str, Any]]) -> Dict[str, Any]:
    """校验 EK Graph 与聚合规则（Layer 2 + Layer 4）。

    检查：
    - EK 平均出边数（≥1）
    - 游离 EK 比例（<20%）
    - KO 聚合规则覆盖率（100%）
    - KO 簇边界：derivation.facts 应等于 aggregation_rule.cluster_eks
    - 假聚合（同子系统式理由）检测
    """
    report = {
        "ek_count": len(eks),
        "isolated_eks": [],
        "avg_edges": 0.0,
        "isolated_ratio": 0.0,
        "aggregation_coverage": 0.0,
        "ko_cluster_sizes": [],
        "fake_aggregations": [],
        "cluster_mismatches": [],
        "pass": True,
    }
    if not eks:
        return report

    total_edges = 0
    isolated = []
    for ek in eks:
        links = ek.get("links") or []
        total_edges += len(links)
        if len(links) == 0:
            isolated.append(ek.get("id", "?"))

    report["isolated_eks"] = isolated
    report["avg_edges"] = total_edges / len(eks)
    report["isolated_ratio"] = len(isolated) / len(eks) if eks else 0.0

    # 聚合覆盖率
    generalized = [ko for ko in kos if ko.get("knowledge_layer") == "generalized"]
    if generalized:
        with_rule = sum(1 for ko in generalized if ko.get("aggregation_rule"))
        report["aggregation_coverage"] = with_rule / len(generalized)

    # KO 簇边界
    for ko in generalized:
        ar = ko.get("aggregation_rule") or {}
        cluster = set(ar.get("cluster_eks", []))
        facts = set((ko.get("derivation") or {}).get("facts", []))
        report["ko_cluster_sizes"].append(len(cluster))
        if cluster and facts and cluster != facts:
            report["cluster_mismatches"].append({
                "ko": ko.get("claim", "?")[:50],
                "cluster_only": sorted(cluster - facts),
                "facts_only": sorted(facts - cluster),
            })
        naming = (ar.get("naming") or "").lower()
        if any(p in naming for p in ["同子系统", "同属一个子系统", "都属于", "模块说明"]):
            report["fake_aggregations"].append(ko.get("claim", "?")[:60])

    # 质量门判定
    failures = []
    if report["avg_edges"] < EK_GRAPH_GATES["min_avg_edges"]:
        failures.append(f"EK 平均出边数 {report['avg_edges']:.2f} < {EK_GRAPH_GATES['min_avg_edges']}")
    if report["isolated_ratio"] > EK_GRAPH_GATES["max_isolated_ratio"]:
        failures.append(f"游离 EK 比例 {report['isolated_ratio']:.2%} > {EK_GRAPH_GATES['max_isolated_ratio']:.0%}")
    if report["aggregation_coverage"] < EK_GRAPH_GATES["aggregation_coverage"]:
        failures.append(f"聚合规则覆盖率 {report['aggregation_coverage']:.0%} < 100%")
    if report["fake_aggregations"]:
        failures.append(f"假聚合 {len(report['fake_aggregations'])} 个（同子系统式理由）")
    if report["cluster_mismatches"]:
        failures.append(f"簇边界不匹配 {len(report['cluster_mismatches'])} 个")
    for size in report["ko_cluster_sizes"]:
        if not (EK_GRAPH_GATES["ko_cluster_min"] <= size <= EK_GRAPH_GATES["ko_cluster_max"]):
            failures.append(f"KO 簇规模 {size} 超出健康区间 [{EK_GRAPH_GATES['ko_cluster_min']},{EK_GRAPH_GATES['ko_cluster_max']}]")

    report["failures"] = failures
    report["pass"] = len(failures) == 0
    return report


# ---------------------------------------------------------------------------
# 断言辅助（供测试使用）
# ---------------------------------------------------------------------------

def find_missing_required_fields(ko: Dict[str, Any]) -> List[str]:
    required = ["knowledge_layer", "claim", "category", "abstraction", "value",
                "epistemic_status", "derivation", "evidence", "scope", "confidence"]
    return [r for r in required if r not in ko]


def is_valid_flow_type(ft: str) -> bool:
    return ft in VALID_FLOW_TYPES


def is_valid_edge_type(et: str) -> bool:
    return et in VALID_EK_EDGE_TYPES
