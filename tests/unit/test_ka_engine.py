"""Layer 2 · Deterministic Unit Tests —— 测试 Skill 的确定性逻辑。

重点：Epistemic Promotion 规则、EK Graph 聚合规则、Knowledge Object schema 校验。
这些是"知识生产系统"的确定性内核——同一输入必须得到同一输出，禁止"看情况"。

关键场景（来自 Codex 审计教训）：
1. 单实例 → 不得自动升 L3（Observed Structure 不是 Pattern）
2. 有反例 → 禁止升 L3+
3. 4 实例 + 3 模块 + 0 反例 → L3 candidate，而不是自动 L5
4. 泛化规则：同子系统 ≠ 聚合理由（分类不是知识）
5. KO 簇边界：derivation.facts 必须等于 aggregation_rule.cluster_eks
"""

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))
import ka_engine  # noqa: E402


# ---------------------------------------------------------------------------
# Epistemic Promotion 确定性规则
# ---------------------------------------------------------------------------

def test_single_observation_cannot_be_l3():
    """单实例、单模块、无跨上下文 → 只能 L2（工程知识），不得升 Pattern。"""
    pi = ka_engine.PromotionInput(
        evidence_count=1, independent_instances=1, different_modules=1,
        cross_context=False, cross_project=False,
    )
    assert ka_engine.compute_max_abstraction(pi) == "L2"
    # 声称 L3 应被拒绝
    result = ka_engine.check_promotion_legitimacy(pi, "L3")
    assert result["allowed"] is False
    assert result["max_allowed"] == "L2"


def test_two_instances_two_modules_is_l3():
    """≥2 独立实例 + ≥2 不同模块 + 0 反例 → L3 Pattern。"""
    pi = ka_engine.PromotionInput(
        evidence_count=2, independent_instances=2, different_modules=2,
        cross_context=False,
    )
    assert ka_engine.compute_max_abstraction(pi) == "L3"


def test_counterexample_blocks_l3():
    """反例存在 → 强制降级 L2，任何声称 L3+ 都必须被拦。"""
    pi = ka_engine.PromotionInput(
        evidence_count=4, independent_instances=3, different_modules=3,
        cross_context=True, counterexamples_found=1,
    )
    assert ka_engine.compute_max_abstraction(pi) == "L2"
    result = ka_engine.check_promotion_legitimacy(pi, "L3")
    assert result["allowed"] is False


def test_cross_context_without_runtime_validation_not_l4():
    """跨上下文但无运行时验证 → L3（Pattern 成型，但无 L4 稳定关系证据）。"""
    pi = ka_engine.PromotionInput(
        evidence_count=3, independent_instances=3, different_modules=3,
        cross_context=True, runtime_validated=False,
    )
    assert ka_engine.compute_max_abstraction(pi) == "L3"


def test_l4_requires_runtime_and_cross_context_and_human_or_strong():
    """L4（Cognitive Model）需要：跨上下文 + 运行时验证 + 独立实例≥2 + 无反例。"""
    pi = ka_engine.PromotionInput(
        evidence_count=5, independent_instances=3, different_modules=3,
        cross_context=True, runtime_validated=True, human_confirmed=True,
    )
    assert ka_engine.compute_max_abstraction(pi) == "L4"
    # 无运行时验证不能 L4
    pi2 = ka_engine.PromotionInput(
        evidence_count=5, independent_instances=3, different_modules=3,
        cross_context=True, runtime_validated=False, human_confirmed=True,
    )
    assert ka_engine.compute_max_abstraction(pi2) == "L3"


def test_l5_requires_cross_project():
    """L5（Methodology）需要跨项目验证（S8）——单项目无论多强都不能自动 L5。"""
    # 单项目强证据 → 最高 L4
    pi_single = ka_engine.PromotionInput(
        evidence_count=10, independent_instances=5, different_modules=5,
        cross_context=True, runtime_validated=True, human_confirmed=True,
        cross_project=False,
    )
    assert ka_engine.compute_max_abstraction(pi_single) == "L4"
    # 跨项目 → L5
    pi_cross = ka_engine.PromotionInput(
        evidence_count=10, independent_instances=5, different_modules=5,
        cross_context=True, runtime_validated=True, human_confirmed=True,
        cross_project=True,
    )
    assert ka_engine.compute_max_abstraction(pi_cross) == "L5"


def test_observed_structure_not_promoted_to_pattern():
    """跨上下文但只有单实例 → Observed Structure（L2），不得升 Pattern（L3）。

    这是 Codex 审计 KO-03 的核心教训：单实例递归模型被包装成高阶 Pattern 是过度升维。
    """
    pi = ka_engine.PromotionInput(
        evidence_count=1, independent_instances=1, different_modules=1,
        cross_context=True,  # 只有"看起来跨上下文"，但只有一个实例
    )
    assert ka_engine.compute_max_abstraction(pi) == "L2"
    result = ka_engine.check_promotion_legitimacy(pi, "L3")
    assert result["allowed"] is False
    assert "降级" in result["reason"]


def test_abstraction_gate_demotion():
    """Abstraction Promotion Gate：claimed L5 但证据只支持 L3 → 必须降级。"""
    pi = ka_engine.PromotionInput(
        evidence_count=2, independent_instances=2, different_modules=2,
        cross_context=False,
    )
    result = ka_engine.check_promotion_legitimacy(pi, "L5")
    assert result["allowed"] is False
    assert result["max_allowed"] == "L3"


# ---------------------------------------------------------------------------
# Knowledge Object Schema 校验
# ---------------------------------------------------------------------------

def _valid_ko():
    return {
        "knowledge_layer": "generalized",
        "claim": "Intelligence ≠ Authority：判断力与执行权是两个独立维度",
        "category": "AGENT",
        "abstraction": "L4",
        "value": "A",
        "epistemic_status": "Validated Pattern",
        "provenance": {"discovered_by": "code-analyst",
                       "supported_by": ["authority-analyst"], "contested_by": []},
        "derivation": {"facts": ["EK-01", "EK-02"],
                       "observations": [], "patterns": [], "models": [],
                       "promotion_arguments": ["L3→L4: 跨上下文证据 + 运行时验证"]},
        "evidence": {"supporting": ["EV-001"], "contradicting": []},
        "flows": {"control": "…", "state": "…", "data": "…", "evidence": "…",
                  "authority": "…", "memory": "…", "policy": "…"},
        "flow_traceability": {"l1_facts_to_edges": []},
        "scope": {"applies_when": "Agent 系统", "does_not_apply_when": "纯 CRUD"},
        "confidence": "high",
        "aggregation_rule": {"rule": "R2", "cluster_eks": ["EK-01", "EK-02"],
                             "edges": ["causal: EK-01→EK-02"],
                             "naming": "审批决策→执行的因果链", "scope_expansion": "…"},
    }


def test_valid_ko_passes():
    assert ka_engine.validate_knowledge_object(_valid_ko()) == []


def test_invalid_abstraction_level_rejected():
    ko = _valid_ko()
    ko["abstraction"] = "L7"  # 不存在 L7
    issues = ka_engine.validate_knowledge_object(ko)
    assert any("abstraction 非法" in i.message for i in issues)


def test_engineering_layer_cannot_be_l3():
    ko = _valid_ko()
    ko["knowledge_layer"] = "engineering"
    ko["abstraction"] = "L3"  # 工程层禁止 L3+
    issues = ka_engine.validate_knowledge_object(ko)
    assert any("engineering 层不允许 L3+" in i.message for i in issues)


def test_generalized_without_aggregation_rule_rejected():
    ko = _valid_ko()
    del ko["aggregation_rule"]
    issues = ka_engine.validate_knowledge_object(ko)
    assert any("aggregation_rule" in i.message for i in issues)


def test_generalized_without_derivation_facts_rejected():
    """无底座的悬空升维：generalized 必须有 derivation.facts 回溯。"""
    ko = _valid_ko()
    ko["derivation"] = {"facts": [], "promotion_arguments": ["…"]}
    issues = ka_engine.validate_knowledge_object(ko)
    assert any("回溯到 engineering 底座" in i.message for i in issues)


def test_fake_aggregation_by_subsystem_rejected():
    """反退化铁律：'同子系统'式聚合理由 = 分类，不是知识，必须拒绝。"""
    ko = _valid_ko()
    ko["aggregation_rule"]["naming"] = "因为它们都属于 exec_policy 子系统"
    issues = ka_engine.validate_knowledge_object(ko)
    assert any("同子系统" in i.message for i in issues)


def test_engineering_without_links_rejected():
    """v3.1：engineering 对象必须声明 links（EK 是图的节点）。"""
    ko = _valid_ko()
    ko["knowledge_layer"] = "engineering"
    ko["abstraction"] = "L2"
    ko["epistemic_status"] = "Fact"
    del ko["aggregation_rule"]
    del ko["derivation"]["promotion_arguments"]  # engineering 不需要 promotion
    ko.pop("links", None)  # 确保 links 不存在
    issues = ka_engine.validate_knowledge_object(ko)
    assert any("links" in i.message for i in issues)


def test_invalid_ek_edge_type_rejected():
    ko = _valid_ko()
    ko["knowledge_layer"] = "engineering"
    ko["abstraction"] = "L2"
    ko["epistemic_status"] = "Fact"
    del ko["aggregation_rule"]
    ko["links"] = [{"to": "EK-02", "type": "related"}]  # 非法边类型
    issues = ka_engine.validate_knowledge_object(ko)
    assert any("边类型非法" in i.message for i in issues)


def test_l4_with_hypothesis_status_rejected():
    """L4/L5 抽象不能是 Hypothesis/Observation——高抽象必须有 Validated Pattern 以上状态。"""
    ko = _valid_ko()
    ko["epistemic_status"] = "Hypothesis"
    issues = ka_engine.validate_knowledge_object(ko)
    assert any("不能是 Hypothesis" in i.message for i in issues)


def test_l4_without_promotion_arguments_rejected():
    ko = _valid_ko()
    ko["derivation"] = {"facts": ["EK-01", "EK-02"], "promotion_arguments": []}
    issues = ka_engine.validate_knowledge_object(ko)
    assert any("promotion_arguments" in i.message for i in issues)


# ---------------------------------------------------------------------------
# EK Graph 聚合规则
# ---------------------------------------------------------------------------

def _make_ek(eid, links=None):
    return {"id": eid, "claim": f"EK {eid}", "links": links or []}


def _make_ko(claim, eks, rule="R2", naming="机制共享 + 因果链"):
    return {
        "knowledge_layer": "generalized",
        "claim": claim,
        "abstraction": "L3",
        "aggregation_rule": {"rule": rule, "cluster_eks": list(eks),
                             "naming": naming, "scope_expansion": "…"},
        "derivation": {"facts": list(eks)},
    }


def test_ek_graph_healthy():
    """EK 全部有边、无游离、聚合规则 100% 覆盖 → PASS。"""
    eks = [
        _make_ek("EK-01", [{"to": "EK-02", "type": "causal"}]),
        _make_ek("EK-02", [{"to": "EK-01", "type": "causal"}, {"to": "EK-03", "type": "mechanism"}]),
        _make_ek("EK-03", [{"to": "EK-02", "type": "mechanism"}]),
    ]
    kos = [_make_ko("KO-1", ["EK-01", "EK-02", "EK-03"], rule="R2")]
    report = ka_engine.validate_ek_graph(eks, kos)
    assert report["pass"] is True
    assert report["avg_edges"] >= 1.0
    assert report["isolated_ratio"] == 0.0
    assert report["aggregation_coverage"] == 1.0


def test_isolated_ek_flagged():
    """游离 EK（无边）必须被检测——工程层退化成模块说明的信号。"""
    eks = [
        _make_ek("EK-01", [{"to": "EK-02", "type": "causal"}]),
        _make_ek("EK-02", [{"to": "EK-01", "type": "causal"}]),
        _make_ek("EK-03", []),  # 孤立
    ]
    kos = [_make_ko("KO-1", ["EK-01", "EK-02"], rule="R2")]
    report = ka_engine.validate_ek_graph(eks, kos)
    assert "EK-03" in report["isolated_eks"]
    assert report["isolated_ratio"] > ka_engine.EK_GRAPH_GATES["max_isolated_ratio"] / 2


def test_cluster_boundary_mismatch_flagged():
    """簇边界：derivation.facts 必须等于 aggregation_rule.cluster_eks。"""
    eks = [
        _make_ek("EK-01", [{"to": "EK-02", "type": "causal"}]),
        _make_ek("EK-02", [{"to": "EK-01", "type": "causal"}]),
    ]
    # KO 声称簇是 EK-01/EK-02，但 derivation.facts 只写了 EK-01（漏支撑）
    ko = _make_ko("KO-1", ["EK-01", "EK-02"], rule="R2")
    ko["derivation"] = {"facts": ["EK-01"]}
    report = ka_engine.validate_ek_graph(eks, [ko])
    assert report["cluster_mismatches"], "簇边界不匹配应被检测"


def test_fake_aggregation_detected():
    """'同子系统'式聚合理由 → 假聚合。"""
    eks = [_make_ek("EK-01", [{"to": "EK-02", "type": "subsystem"}]) for _ in range(2)]
    eks[0]["links"] = [{"to": "EK-02", "type": "subsystem"}]
    eks[1]["links"] = [{"to": "EK-01", "type": "subsystem"}]
    ko = _make_ko("KO-1", ["EK-01", "EK-02"], rule="R2", naming="它们都属于同一个子系统")
    report = ka_engine.validate_ek_graph(eks, [ko])
    assert report["fake_aggregations"], "同子系统式假聚合应被检测"



# ---------------------------------------------------------------------------
# P-007 · Flow Sequence Truth（确定性单测）
# ---------------------------------------------------------------------------
def test_flow_sequence_without_anchors_flagged():
    """≥2 步骤的 chain 无顺序锚点 → SEQUENCE_UNVERIFIED（P-007）。"""
    chain = [
        {"node": "approval", "symbol": "a.ts:1", "role": "审批"},
        {"node": "guards", "symbol": "g.ts:2", "role": "守卫"},
    ]
    r = ka_engine.validate_flow_sequence(chain)
    assert not r["pass"], "无顺序锚点的 chain 必须被标记 SEQUENCE_UNVERIFIED"
    assert len(r["unverified"]) > 0


def test_flow_sequence_short_chain_ok():
    """单步骤/空 chain 无需顺序校验。"""
    assert ka_engine.validate_flow_sequence([])["pass"]
    assert ka_engine.validate_flow_sequence([{"node": "x"}])["pass"]


def test_flow_sequence_anchored_ok():
    """带正确顺序锚点的 chain → pass。"""
    chain = [
        {"node": "approval", "symbol": "a.ts:1", "role": "审批",
         "sequence_anchor": {"from": "step_1", "to": "step_2", "evidence": "a.ts:30"}},
        {"node": "guards", "symbol": "g.ts:2", "role": "守卫",
         "sequence_anchor": {"from": "step_2", "to": "step_3", "evidence": "g.ts:40"}},
    ]
    r = ka_engine.validate_flow_sequence(chain)
    assert r["pass"], "正确顺序锚点应通过"


def test_flow_sequence_contradiction_flagged():
    """顺序锚点 from >= to → SEQUENCE_CONTRADICTED（P-007）。"""
    chain = [
        {"node": "guards", "symbol": "g.ts:2", "role": "守卫",
         "sequence_anchor": {"from": "step_2", "to": "step_1", "evidence": "g.ts:40"}},
    ]
    r = ka_engine.validate_flow_sequence(chain)
    assert not r["pass"], "顺序颠倒的锚点必须被检测"
    assert len(r["contradictions"]) > 0


# ---------------------------------------------------------------------------
# P-009 · Abstraction Scope Boundary（确定性单测）
# ---------------------------------------------------------------------------
def test_scope_boundary_ok():
    """L4 KO 有 applies_when + does_not_apply_when → pass。"""
    ko = {"abstraction": "L4", "claim": "受限执行路径上的分层 fail-closed",
          "scope": {"applies_when": "受限执行路径", "does_not_apply_when": "非受限只读路径"}}
    assert ka_engine.validate_scope_boundary(ko)["pass"]


def test_scope_boundary_missing_does_not_apply_flagged():
    """L4 KO 缺 does_not_apply_when → detect（P-009）。"""
    ko = {"abstraction": "L4", "claim": "所有执行路径必须审批", "scope": {"applies_when": "Agent 系统"}}
    r = ka_engine.validate_scope_boundary(ko)
    assert not r["pass"], "缺 does_not_apply_when 或绝对化泛化必须被检测"
    assert len(r["issues"]) >= 1


def test_scope_boundary_not_required_for_l2():
    """L2 engineering 知识不强制 scope 双字段（只限 L3+）。"""
    ko = {"abstraction": "L2", "claim": "某实现", "scope": {}}
    assert ka_engine.validate_scope_boundary(ko)["pass"]


# ---------------------------------------------------------------------------
# 运行入口
# ---------------------------------------------------------------------------

def run() -> int:
    """用轻量 runner 执行所有 test_ 函数（无 pytest 依赖）。"""
    import inspect
    failures = 0
    passed = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                passed += 1
            except AssertionError as e:
                failures += 1
                print(f"  ❌ {name}: {e}")
            except Exception as e:  # noqa: BLE001
                failures += 1
                print(f"  ❌ {name}: 异常 {type(e).__name__}: {e}")
    print(f"Layer 2 Deterministic Unit Tests: {passed} passed, {failures} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(run())
