---
proposal_id: P-012
title: "新增 deepseek-harness Regression / Benchmark Gold Records（B-1..B-5 + 家族枚举）"
priority: P2
risk: Low
changed_paths:
  - "benchmarks/deepseek-harness/*.yaml"
  - "tests/regression/test_codex_regression.py"
why: "独立验证提出 5 个可作 CI Gold Record 的 Benchmark/Regression case（never 不可绕过 / 守卫单调性 / collapse 先于策略 / plan-mode 恢复 / legacy 拒绝）+ 家族枚举与 approval 策略层。这些来自真实项目的可复算安全行为，应永久纳入回归，防止未来 skill 版本退化。"
validation:
  - "Layer 3 regression: 新增 gold records 全部通过"
  - "Layer 4 benchmark: 现有 gate 不回退"
status: "proposed"
---

## 变更内容
1. **benchmarks/deepseek-harness/**：新增 Gold Records：
   - `b1_never_unbypassable.yaml`（required_knowledge：never 策略不可绕过）
   - `b2_guard_monotonicity.yaml`（security_invariant：守卫单调性，force allow 不能 bypass guard）
   - `b3_collapse_before_policy.yaml`（required_mechanism：collapse 先于策略管线）
   - `b4_plan_mode_recovery.yaml`（required_mechanism：plan-mode projection 折叠/恢复）
   - `b5_legacy_hard_reject.yaml`（required_mechanism：legacy 格式硬拒绝）
   - `family_enumeration.yaml`（required_coverage：guard/seam/approval-layer 家族全实例）
   - `approval_policy_layers.yaml`（required_coverage：config/override/delegation 三层 + collapse）
2. **tests/regression/test_codex_regression.py**：新增 `required_family_instances` 与 `required_sequence_fact` checker 类型（若 P-007/P-008 未合并则此处为独立实现）。

## 自动化 Regression Case
- ✅ 全部可自动化（YAML fixture + checker）。

## 风险分析
- 影响面：benchmarks/** + tests/regression → **Low**（Quality Gate PASS 可自动合并，Phase 2）。
- 回退风险：仅新增 fixture 与 checker，不动既有逻辑。
