"""Layer 2 扩展 · 规则集合法性 + PR 风险自动分级单测。

1. 规则集（rules/*.json）自身必须合法：
   - 文件存在、JSON 可解析
   - Promotion Gate 值在合理范围内（不能设成 0 门槛=形同虚设，也不能设成不可能达到）
   - 晋升规则阈值自洽（L3 < L4 < L5 的门槛递增）
   - 风险分级路径非空且高优先级原则正确
2. PR 风险自动分级：
   - 只改 tests/ → low（自动合并）
   - 改 agents/ → high（永不自动合并）
   - 改 references/ → medium（人工审）
   - 混合变更 → 取最高风险
   - 未知文件 → 保守 medium
"""

import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))
import ka_engine  # noqa: E402
sys.path.insert(0, str(REPO_ROOT / "tools"))
from evaluate_pr_risk import evaluate_risk, match_path  # noqa: E402

RULES_DIR = REPO_ROOT / "rules"


# ---------------------------------------------------------------------------
# 规则集合法性
# ---------------------------------------------------------------------------

def test_all_rule_files_exist_and_valid_json():
    """4 个规则文件必须存在且可解析。"""
    for name in ["quality-gates", "promotion-rules", "ek-graph-rules", "risk-paths"]:
        path = RULES_DIR / f"{name}.json"
        assert path.exists(), f"缺少规则文件 rules/{name}.json"
        data = ka_engine.load_rules_file(name)
        assert isinstance(data, dict) and data, f"rules/{name}.json 解析为空或非法"


def test_promotion_gate_values_in_sane_range():
    """Promotion Gate 硬门槛值必须合理（不能形同虚设，也不能不可能达到）。"""
    gate = ka_engine.get_promotion_gate()
    assert gate.get("regression") is True
    # 覆盖率/保真度门槛：0.5 < x <= 1.0（太松=无效，太紧=无法达成）
    for key in ["critical_coverage_min", "fidelity_min", "abstraction_validity_min"]:
        v = gate.get(key)
        assert v is not None, f"缺少 {key}"
        assert 0.5 < v <= 1.0, f"{key}={v} 超出合理范围 (0.5, 1.0]"
    # False Acceptance 上限：0 <= x < 0.5
    fa = gate.get("false_acceptance_max")
    assert fa is not None and 0 <= fa < 0.5, f"false_acceptance_max={fa} 不合理"
    # Critical Regressions 必须为 0（过去错误不允许再现）
    assert gate.get("critical_regressions_allowed") == 0


def test_promotion_rules_thresholds_monotonic():
    """晋升门槛必须递增：L3 所需 < L4 所需（跨上下文/运行时/人工逐步加强）。"""
    pr = ka_engine.get_promotion_rules()
    l3 = pr.get("l3_requires", {})
    l4 = pr.get("l4_requires", {})
    # L4 比 L3 要求更多维度（cross_context + runtime + human）
    assert l4.get("cross_context") is True, "L4 必须要求 cross_context"
    assert l4.get("runtime_validated") is True, "L4 必须要求 runtime_validated"
    # 反例压制层：必须 ≤ L2（任何反例都禁止升 L3+）
    assert pr.get("counterexample_blocks_above") == "L2"
    # Observed Structure 不得升 Pattern
    assert pr.get("observed_structure_max") == "L2"


def test_ek_graph_rules_loaded():
    """EK Graph 规则从规则文件加载（不是硬编码常量）。"""
    gates = ka_engine.get_ek_graph_rules()
    assert gates.get("min_avg_edges", 0) >= 1.0
    assert gates.get("max_isolated_ratio", 1) < 0.5
    assert gates.get("aggregation_coverage", 0) == 1.0
    assert 2 <= gates.get("ko_cluster_min", 0) <= 3
    assert gates.get("ko_cluster_max", 0) >= 10


def test_risk_rules_complete():
    """风险分级规则必须覆盖三类，且每类路径非空。"""
    rr = ka_engine.get_risk_rules()
    levels = rr.get("risk_levels", {})
    for level in ["high", "medium", "low"]:
        assert level in levels, f"缺少 risk_levels.{level}"
        assert levels[level].get("paths"), f"risk_levels.{level}.paths 为空"
    # 高优先级原则：high_wins
    assert rr.get("priority", {}).get("high_wins") is True


# ---------------------------------------------------------------------------
# PR 风险自动分级
# ---------------------------------------------------------------------------

def test_low_risk_auto_merge_allowed():
    """只改 tests/ + benchmarks/ → low → 自动合并允许。"""
    result = evaluate_risk([
        "tests/unit/test_ka_engine.py",
        "benchmarks/codex/ko_01.yaml",
        "evals/fidelity/fidelity.json",
    ])
    assert result["risk"] == "low"
    assert result["auto_merge_allowed"] is True


def test_high_risk_never_auto_merge():
    """改 agents/ 或 workflows/ 或 contracts/epistemic-status → high → 永不自动合并。"""
    for f in [
        "agents/knowledge-synthesizer.md",
        "workflows/archaeology.md",
        "contracts/epistemic-status.md",
        "protocols/promotion.md",
        "tools/ka_engine.py",
        "rules/quality-gates.json",
    ]:
        result = evaluate_risk([f])
        assert result["risk"] == "high", f"{f} 应判为 high"
        assert result["auto_merge_allowed"] is False, f"{f} 不应自动合并"


def test_medium_risk_requires_human():
    """改 references/ → medium → 人工审，不自动合并。"""
    result = evaluate_risk(["references/five-layer-ladder.md"])
    assert result["risk"] == "medium"
    assert result["auto_merge_allowed"] is False


def test_mixed_changes_take_highest_risk():
    """混合变更取最高风险：tests/ + agents/ → high。"""
    result = evaluate_risk([
        "tests/unit/test_ka_engine.py",
        "agents/reconciler.md",
    ])
    assert result["risk"] == "high"
    assert result["auto_merge_allowed"] is False


def test_unknown_file_conservative_medium():
    """未匹配任何规则的文件 → 保守 medium（未知变更需人审）。"""
    result = evaluate_risk(["some/unknown/path.py"])
    assert result["risk"] == "medium"
    assert result["auto_merge_allowed"] is False


def test_match_path_wildcards():
    assert match_path("agents/reconciler.md", ["agents/**"]) is True
    assert match_path("contracts/epistemic-status.md", ["contracts/epistemic-status*"]) is True
    assert match_path("README.md", ["README*"]) is True
    assert match_path("tests/unit/x.py", ["tests/**"]) is True
    assert match_path("docs/foo.md", ["docs/**"]) is True
    assert match_path("agents/x.md", ["README*"]) is False


# ---------------------------------------------------------------------------
# 运行入口
# ---------------------------------------------------------------------------

def run() -> int:
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
    print(f"Ruleset + PR Risk Tests: {passed} passed, {failures} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(run())
