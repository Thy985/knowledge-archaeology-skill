"""Layer 4 · Benchmark Tests —— 质量指标计算 + Promotion Gate（硬门槛）。

Regression 防止过去的问题再现；Benchmark 证明 Skill 真的变强了。
本层计算 Codex 考古质量指标并应用硬门槛（promotion_gate）。

指标（与 workflows/benchmark.md 一致）：
- Fidelity           声明与仓库证据的一致性
- Critical Coverage  高密度子系统覆盖
- Flow Integrity     Flow Atlas 与代码一致
- Abstraction Validity  升维是否合理（过过度升维率）
- Epistemic Accuracy 认知状态标注诚实度
- Counterexample Recall  反例检测率
- False Acceptance   验证器误放行率

硬门槛（promotion_gate，用户定义）：
- regression: pass
- critical_coverage ≥ 0.90
- fidelity ≥ 0.95
- abstraction_validity ≥ 0.90
- false_acceptance ≤ 0.10
- critical_regressions = 0

即使总分 +10%，只要 Critical Coverage -4% → FAIL（可能是用漂亮但错误的知识换来的）。
"""

import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))
import ka_engine  # noqa: E402

EVALS_DIR = REPO_ROOT / "evals"

# 硬门槛（用户明确定义，不可放松）—— 从 rules/quality-gates.json 权威规则集加载，禁止硬编码
PROMOTION_GATE = ka_engine.get_promotion_gate()

# 各 evals 子目录的评分文件
EVAL_SCHEMA = {
    "fidelity": {
        "file": "fidelity.json",
        "metrics": ["fidelity"],
        "gate": "fidelity_min",
        "direction": "min",
    },
    "coverage": {
        "file": "coverage.json",
        "metrics": ["critical_coverage"],
        "gate": "critical_coverage_min",
        "direction": "min",
    },
    "abstraction": {
        "file": "abstraction.json",
        "metrics": ["abstraction_validity"],
        "gate": "abstraction_validity_min",
        "direction": "min",
    },
    "flow": {
        "file": "flow.json",
        "metrics": ["flow_integrity"],
        "gate": None,
        "direction": "min",
    },
    "epistemic": {
        "file": "epistemic.json",
        "metrics": ["epistemic_accuracy"],
        "gate": None,
        "direction": "min",
    },
}

# 汇总指标（来自 05-validation 或 CI 注入）
AGGREGATE_METRICS = {
    "false_acceptance": 0.0,
    "counterexample_recall": 0.0,
    "critical_regressions": 0,
}


def _load_json(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def evaluate_benchmark(metrics: dict | None = None) -> dict:
    """计算 benchmark 得分并应用 promotion gate。

    metrics: 可选的运行时指标注入（CI 跑真实考古后注入）；否则读 evals/ 下静态评分。
    """
    merged = dict(AGGREGATE_METRICS)
    for eval_name, cfg in EVAL_SCHEMA.items():
        data = _load_json(EVALS_DIR / eval_name / cfg["file"])
        for m in cfg["metrics"]:
            if m in data:
                merged[m] = data[m]
    if metrics:
        merged.update(metrics)

    # 从 v3 考古报告推算的补充指标（若未注入）
    if "fidelity" not in merged:
        merged["fidelity"] = 0.0
    if "critical_coverage" not in merged:
        merged["critical_coverage"] = 0.0
    if "abstraction_validity" not in merged:
        merged["abstraction_validity"] = 0.0
    if "flow_integrity" not in merged:
        merged["flow_integrity"] = 0.0
    if "epistemic_accuracy" not in merged:
        merged["epistemic_accuracy"] = 0.0

    # Gate 判定
    gate_results = []
    gate_pass = True
    for gate_key, threshold in [
        ("regression", True),
        ("critical_coverage", PROMOTION_GATE["critical_coverage_min"]),
        ("fidelity", PROMOTION_GATE["fidelity_min"]),
        ("abstraction_validity", PROMOTION_GATE["abstraction_validity_min"]),
        ("false_acceptance", PROMOTION_GATE["false_acceptance_max"]),
        ("critical_regressions", PROMOTION_GATE["critical_regressions_allowed"]),
    ]:
        if gate_key == "regression":
            ok = True  # Layer 3 负责，此处占位
            gate_results.append({"gate": "regression", "value": True, "threshold": True, "pass": ok})
            continue
        if gate_key == "critical_coverage":
            val, thr, pass_dir = merged.get("critical_coverage", 0), threshold, "min"
        elif gate_key == "fidelity":
            val, thr, pass_dir = merged.get("fidelity", 0), threshold, "min"
        elif gate_key == "abstraction_validity":
            val, thr, pass_dir = merged.get("abstraction_validity", 0), threshold, "min"
        elif gate_key == "false_acceptance":
            val, thr, pass_dir = merged.get("false_acceptance", 1), threshold, "max"
        elif gate_key == "critical_regressions":
            val, thr, pass_dir = merged.get("critical_regressions", 999), threshold, "max"
        else:
            continue
        ok = val >= thr if pass_dir == "min" else val <= thr
        if not ok:
            gate_pass = False
        gate_results.append({"gate": gate_key, "value": val, "threshold": thr, "pass": ok})

    # 总分（加权）
    overall = (
        merged.get("fidelity", 0) * 0.25
        + merged.get("critical_coverage", 0) * 0.25
        + merged.get("abstraction_validity", 0) * 0.20
        + merged.get("flow_integrity", 0) * 0.15
        + merged.get("epistemic_accuracy", 0) * 0.15
    )
    # False Acceptance 惩罚
    fa = merged.get("false_acceptance", 0)
    if fa > 0.10:
        overall -= (fa - 0.10) * 0.5

    return {
        "metrics": merged,
        "overall": round(overall * 100, 1),
        "gate_results": gate_results,
        "gate_pass": gate_pass,
        "promotion_decision": "PROMOTION PASS" if gate_pass else "REJECT (Quality Gate Failed)",
    }


def run() -> int:
    result = evaluate_benchmark()
    print(f"Benchmark Metrics: {json.dumps(result['metrics'], ensure_ascii=False, indent=2)}")
    print(f"Overall Score: {result['overall']}")
    for g in result["gate_results"]:
        mark = "✅" if g["pass"] else "❌"
        print(f"  {mark} {g['gate']}: {g['value']} (threshold {g['threshold']})")
    if result["gate_pass"]:
        print(f"✅ Layer 4 Benchmark Tests: PASS —— {result['promotion_decision']}")
        return 0
    print(f"❌ Layer 4 Benchmark Tests: FAIL —— {result['promotion_decision']}")
    print("   即使总分上升，任一硬门槛未过 → 拒绝合并（可能是用漂亮但错误的知识换来的）")
    return 1


if __name__ == "__main__":
    sys.exit(run())
