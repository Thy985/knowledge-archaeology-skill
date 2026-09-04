---
proposal_id: P-009
title: "Abstraction Scope 反例 Gate —— 每个 L3+ KO 必须经受 scope 边界反例攻击"
priority: P0
risk: High
changed_paths:
  - "agents/abstraction-auditor.md"
  - "agents/counterexample-hunter.md"
  - "contracts/knowledge-schema.md"
  - "tests/mutation/test_mutation.py"
why: "KO-03 fail-closed 族 claim 泛化到'全部权限面'，实际仅适用受限执行路径（plan-mode 等非受限路径不适用）。abstraction-auditor 判 OK，独立验证 DOWNGRADED——Abstraction Promotion Gate 检查层级过高与聚合规则，但不检查 scope 边界是否被夸大。与 v1 F-002 同族变体（层级未超但范围夸大）。"
validation:
  - "Layer 5 mutation: scope 泛化 KO mutation（claim 覆盖范围夸大）→ detect=true"
  - "Layer 3 regression: KO-03 scope 收紧 gold record"
  - "Layer 4 benchmark: 现有 gate 不回退"
status: "pending_human_gate"  # CI 全 PASS；HIGH/Medium 风险 → 治理阻止自动合并，待 Owner 审查
---

## 变更内容
1. **contracts/knowledge-schema.md**：L3+ KO 的 `scope` 必须同时声明 `applies_when` 与 `does_not_apply_when`；缺任一 → schema 不合格。
2. **agents/abstraction-auditor.md**：对每个 L3+ KO 强制"scope 反例攻击"——主动寻找该 claim 不适用的实例（非受限路径 / 例外 / bypass）；找不到 must 记录搜索路径（searched_paths）。
3. **agents/counterexample-hunter.md**：反例预算新增"每个 L3+ ≥1 个 scope 边界反例"。
4. **tests/mutation**：新增 mutation：真实受限路径 claim → 变异为全路径泛化 → detect=true。

## 自动化 Regression Case
- ✅ 可自动化：`scope_泛化_mutation`（detect）+ `ko03_scope_收紧`（gold record：fail-closed 族必须限定受限执行路径）。

## 风险分析
- 影响面：contracts（knowledge-schema）+ abstraction-auditor（核心验证）+ counterexample-hunter → **High**（永不自动 merge）。
- 回退风险：scope 字段在 knowledge-schema 已存在（applies_when/does_not_apply_when），本次仅强制"必须有 + 反例审计"，向后兼容。
