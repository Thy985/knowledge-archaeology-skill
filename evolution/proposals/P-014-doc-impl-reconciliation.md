---
proposal_id: P-014
title: "doc-vs-impl reconciliation —— validator 强制对账设计文档形式化声称与实现"
priority: P1
risk: High
changed_paths:
  - "agents/truth-auditor.md"
  - "agents/epistemic-auditor.md"
why: "SkillFortify 考古（ARCH-2026-09-05-001）暴露 C-01：Formal-Foundations.md 声称能力推断 'without over-approximation'，实现（engine.py）明确是 'conservative over-approximation'——矛盾由 Auditor 主动发现，skill 的 truth-auditor/epistemic-auditor 无强制对账检查点。形式化工具若把'文档声称'升维为'实现事实'，是典型 epistemic 混淆；此类工具（带 formal claims）跨项目复现概率高。"
validation:
  - "Layer 3 regression: doc-vs-impl 对账 gold record（文档声称性质 vs 实现注释不一致必须产出 CONTRADICTED 或标注）"
  - "Layer 4 benchmark: 现有 gate 不回退"
  - "Layer 5 mutation: 对账缺失的假阳性检查"
status: "proposed"
---

## 变更内容
1. **agents/truth-auditor.md**：对含"形式化性质声称"的设计文档（如 formal foundations / proofs / guarantees），强制与实现注释/测试逐句对账；不一致必须产出 CONTRADICTED 或标 NEEDS_HUMAN_REVIEW，不得静默采用文档表述。
2. **agents/epistemic-auditor.md**：文档声称（Obs）与实现事实（Fact）分裂时必须显式标注来源层级；"文档说 X 且实现做 X"才可升维，"文档说 X 实现做 Y"只能进 Candidates。

## 自动化 Regression Case
- ✅ 可自动化：`doc_impl_reconciliation` gold record（文档声称性质 vs 实现注释矛盾必须被捕获）。

## 风险分析
- 影响面：agents 提示词（validator 角色）→ **High**（agents/**，永不自动合并）。
- 回退风险：纯审计检查点强化，无引擎逻辑变更。
