"""Layer 5 · Mutation / Adversarial Tests —— 坏知识检测（系统能否识别自己的错误）。

核心逻辑：自动生成"看似合理但错误"的知识（mutation），要求 validator 引擎 detect=true。
如果系统不能识别自己的错误 → 它生产的知识不可信。

Mutation 源（来自 Codex 审计真实教训）：
1. 过度升维：真实"A 模块有审批机制" → Mutation"整个系统所有执行都必须审批"
2. 事实错误：approval_policy 四态 → Mutation 三态
3. 反例忽略：真实"某路径存在 bypass" → Mutation"所有路径都有 Gate"
4. 悬空升维：generalized 无 derivation.facts 底座
5. 假聚合：同子系统式聚合理由
6. 状态造假：Fact → Principle 无中间推导
"""

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))
import ka_engine  # noqa: E402


# ---------------------------------------------------------------------------
# Mutation 定义：每个 mutation 包含一个"坏知识"构造 + 期望 detect=true
# ---------------------------------------------------------------------------

def mutation_over_abstraction() -> dict:
    """Mutation 1：单实例观察被包装成 L5 普遍原则。"""
    pi = ka_engine.PromotionInput(
        evidence_count=1, independent_instances=1, different_modules=1,
        cross_context=False, cross_project=False,
    )
    result = ka_engine.check_promotion_legitimacy(pi, "L5")
    # 期望：detect（不允许 L5）
    return {"name": "over_abstraction", "detected": not result["allowed"],
            "max_allowed": result["max_allowed"]}


def mutation_over_abstraction_l4() -> dict:
    """Mutation 1b：单实例 + 单模块 + 跨上下文 被声称 L4（仍应检测）。"""
    pi = ka_engine.PromotionInput(
        evidence_count=1, independent_instances=1, different_modules=1,
        cross_context=True, runtime_validated=False,
    )
    result = ka_engine.check_promotion_legitimacy(pi, "L4")
    return {"name": "over_abstraction_l4", "detected": not result["allowed"],
            "max_allowed": result["max_allowed"]}


def mutation_counterexample_ignored() -> dict:
    """Mutation 2：存在反例仍声称 L3+（反例被忽略）。"""
    pi = ka_engine.PromotionInput(
        evidence_count=5, independent_instances=4, different_modules=4,
        cross_context=True, runtime_validated=True, counterexamples_found=1,
    )
    result = ka_engine.check_promotion_legitimacy(pi, "L3")
    return {"name": "counterexample_ignored", "detected": not result["allowed"],
            "max_allowed": result["max_allowed"]}


def mutation_fact_state_error() -> dict:
    """Mutation 3：approval_policy 事实错误（四态 → 三态）。

    用 ka_engine 无法直接测"代码事实"，但可以测 schema 校验：
    把 mutation 写成 knowledge object，检查它是否被 validate_knowledge_object 拦截。
    实际事实校验由 Layer 3 的 approval_policy_states.yaml 承担。
    此处验证：schema 校验不放过自相矛盾的 KO。
    """
    ko = {
        "knowledge_layer": "generalized",
        "claim": "approval_policy 是三态",
        "category": "AGENT",
        "abstraction": "L4",  # 声称 L4 但没有 promotion arguments → 应被拦
        "value": "A",
        "epistemic_status": "Validated Pattern",
        "derivation": {"facts": ["EK-01"], "promotion_arguments": []},
        "evidence": {"supporting": []},
        "scope": {},
        "confidence": "high",
        "aggregation_rule": {"rule": "R2", "cluster_eks": ["EK-01"], "naming": "机制", "scope_expansion": ""},
    }
    issues = ka_engine.validate_knowledge_object(ko)
    # 至少应该拦截：L4 无 promotion arguments；epistemic 状态无支撑
    detected = any("promotion_arguments" in i.message for i in issues)
    return {"name": "fact_state_error", "detected": detected, "issues": len(issues)}


def mutation_no_grounding() -> dict:
    """Mutation 4：generalized 无 derivation.facts 底座（悬空升维）。"""
    ko = {
        "knowledge_layer": "generalized",
        "claim": "某普遍原则",
        "category": "PRINCIPLE",
        "abstraction": "L4",
        "value": "A",
        "epistemic_status": "Principle",
        "derivation": {"facts": [], "promotion_arguments": ["..."]},
        "evidence": {"supporting": []},
        "scope": {},
        "confidence": "high",
        "aggregation_rule": {"rule": "R2", "cluster_eks": [], "naming": "机制", "scope_expansion": ""},
    }
    issues = ka_engine.validate_knowledge_object(ko)
    detected = any("回溯到 engineering 底座" in i.message for i in issues)
    return {"name": "no_grounding", "detected": detected, "issues": len(issues)}


def mutation_fake_aggregation() -> dict:
    """Mutation 5：同子系统式假聚合。"""
    ko = {
        "knowledge_layer": "generalized",
        "claim": "某模式",
        "category": "PATTERN",
        "abstraction": "L3",
        "value": "B",
        "epistemic_status": "Validated Pattern",
        "derivation": {"facts": ["EK-01", "EK-02"], "promotion_arguments": ["..."]},
        "evidence": {"supporting": []},
        "scope": {},
        "confidence": "medium",
        "aggregation_rule": {"rule": "R1", "cluster_eks": ["EK-01", "EK-02"],
                             "naming": "因为它们都属于同一个子系统", "scope_expansion": ""},
    }
    issues = ka_engine.validate_knowledge_object(ko)
    detected = any("同子系统" in i.message for i in issues)
    return {"name": "fake_aggregation", "detected": detected, "issues": len(issues)}


def mutation_fact_to_principle() -> dict:
    """Mutation 6：Fact → Principle 无中间推导（状态造假）。"""
    ko = {
        "knowledge_layer": "generalized",
        "claim": "单个事实被宣布为普遍原则",
        "category": "PRINCIPLE",
        "abstraction": "L4",
        "value": "A",
        "epistemic_status": "Principle",  # 直接 Fact 变 Principle
        "derivation": {"facts": ["EV-001"], "promotion_arguments": []},
        "evidence": {"supporting": ["EV-001"], "contradicting": []},
        "scope": {},
        "confidence": "high",
        "aggregation_rule": {"rule": "R2", "cluster_eks": ["EK-01"], "naming": "机制", "scope_expansion": ""},
    }
    issues = ka_engine.validate_knowledge_object(ko)
    # L4 必须由 promotion_arguments 支撑；单 EV-001 单实例无法支撑 L4
    detected = any("promotion_arguments" in i.message for i in issues)
    return {"name": "fact_to_principle", "detected": detected, "issues": len(issues)}


def mutation_law_without_cross_project() -> dict:
    """Mutation 7：单项目自称 Law（普遍定律，需要 S8 跨项目验证）。"""
    ko = {
        "knowledge_layer": "generalized",
        "claim": "这是软件工程的普遍定律",
        "category": "PRINCIPLE",
        "abstraction": "L5",
        "value": "A",
        "epistemic_status": "Law",  # 单项目不能自称 Law
        "derivation": {"facts": ["EK-01"], "promotion_arguments": ["..."],
                       "observations": [], "patterns": [], "models": []},
        "evidence": {"supporting": ["EV-001"], "contradicting": []},
        "scope": {},
        "confidence": "high",
        "aggregation_rule": {"rule": "R2", "cluster_eks": ["EK-01"], "naming": "机制", "scope_expansion": ""},
    }
    issues = ka_engine.validate_knowledge_object(ko)
    # 至少应警告 Law 需要跨项目验证；L5 也应被检查
    detected = any("Law" in i.message for i in issues)
    return {"name": "law_without_cross_project", "detected": detected, "issues": len(issues)}


def mutation_engineering_l3() -> dict:
    """Mutation 8：engineering 层对象被标 L3（层-抽象级冲突）。"""
    ko = {
        "knowledge_layer": "engineering",
        "claim": "某实现机制",
        "category": "ENGINEERING",
        "abstraction": "L3",
        "value": "B",
        "epistemic_status": "Fact",
        "derivation": {"facts": ["EK-01"]},
        "evidence": {"supporting": []},
        "scope": {},
        "confidence": "medium",
        "links": [{"to": "EK-02", "type": "causal"}],
    }
    issues = ka_engine.validate_knowledge_object(ko)
    detected = any("engineering 层不允许 L3+" in i.message for i in issues)
    return {"name": "engineering_l3", "detected": detected, "issues": len(issues)}


def mutation_flow_sequence_error() -> dict:
    """Mutation 9（P-007）：Flow chain 顺序颠倒/无顺序锚点（deepseek-harness F-05 教训）。

    真实：collapse-check → pre-execute → approval → guards → execute
    Mutation：approval 被放到 guards 之后（顺序颠倒）且无顺序锚点 → 必须 detect。
    """
    chain_wrong = [
        {"node": "collapse-check", "symbol": "tools/index.ts:1367", "role": "前置拒绝"},
        {"node": "pre-execute", "symbol": "tools/index.ts:144", "role": "pre"},
        {"node": "guards", "symbol": "tools/index.ts:697", "role": "守卫"},
        {"node": "approval", "symbol": "user-approval/index.ts:207", "role": "审批"},  # 位置颠倒
        {"node": "execute", "symbol": "tools/index.ts:227", "role": "执行"},
    ]
    # 无任何顺序锚点 → SEQUENCE_UNVERIFIED
    r1 = ka_engine.validate_flow_sequence(chain_wrong)
    detect_no_anchor = not r1["pass"] and len(r1["unverified"]) > 0
    # 带显式锚点但顺序颠倒 → SEQUENCE_CONTRADICTED
    chain_anchored = [
        {"node": "guards", "symbol": "tools/index.ts:697", "role": "守卫",
         "sequence_anchor": {"from": "step_3", "to": "step_4", "evidence": "tools/index.ts:1468"}},
        {"node": "approval", "symbol": "user-approval/index.ts:207", "role": "审批",
         "sequence_anchor": {"from": "step_4", "to": "step_3", "evidence": "tools/index.ts:1400"}},  # 颠倒
    ]
    r2 = ka_engine.validate_flow_sequence(chain_anchored)
    detect_contradiction = not r2["pass"] and len(r2["contradictions"]) > 0
    return {"name": "flow_sequence_error", "detected": detect_no_anchor or detect_contradiction,
            "unverified": len(r1["unverified"]), "contradictions": len(r2["contradictions"])}


def mutation_scope_overgeneralization() -> dict:
    """Mutation 10（P-009）：L4 KO scope 泛化（deepseek-harness KO-03 教训）。

    真实：fail-closed 族仅适用受限执行路径（有 does_not_apply_when: 非受限只读路径）。
    Mutation：claim 声称覆盖"全部权限面/所有执行"，scope 无 does_not_apply_when → 必须 detect。
    """
    ko = {
        "knowledge_layer": "generalized",
        "claim": "所有执行路径都必须经过 fail-closed 权限族审批",
        "category": "PERMISSION",
        "abstraction": "L4",
        "value": "A",
        "epistemic_status": "Principle",
        "derivation": {"facts": ["EK-10", "EK-09", "EK-07"], "promotion_arguments": ["..."]},
        "evidence": {"supporting": []},
        "scope": {"applies_when": "Agent 系统"},  # 缺 does_not_apply_when
        "confidence": "high",
        "aggregation_rule": {"rule": "R3", "cluster_eks": ["EK-10", "EK-09", "EK-07"], "naming": "不变量簇", "scope_expansion": ""},
    }
    issues = ka_engine.validate_scope_boundary(ko)["issues"]
    detected = any("does_not_apply_when" in i or "绝对化泛化" in i for i in issues)
    return {"name": "scope_overgeneralization", "detected": detected, "issues": len(issues)}


MUTATIONS = [
    mutation_over_abstraction,
    mutation_over_abstraction_l4,
    mutation_counterexample_ignored,
    mutation_fact_state_error,
    mutation_no_grounding,
    mutation_fake_aggregation,
    mutation_fact_to_principle,
    mutation_law_without_cross_project,
    mutation_engineering_l3,
    mutation_flow_sequence_error,
    mutation_scope_overgeneralization,
]


def run() -> int:
    failures = 0
    detected_count = 0
    for fn in MUTATIONS:
        result = fn()
        name = result["name"]
        if result["detected"]:
            detected_count += 1
            print(f"  ✅ Mutation [{name}]: 已检测")
        else:
            failures += 1
            print(f"  ❌ Mutation [{name}]: 未被检测（系统无法识别自己的错误）")
            print(f"     detail: { {k: v for k, v in result.items() if k != 'detected'} }")
    total = len(MUTATIONS)
    if failures:
        print(f"❌ Layer 5 Mutation Tests: FAIL —— {detected_count}/{total} 坏知识被识别")
        return 1
    print(f"✅ Layer 5 Mutation Tests: PASS —— {detected_count}/{total} 坏知识全部被识别（系统能识别自己的错误）")
    return 0


if __name__ == "__main__":
    sys.exit(run())
