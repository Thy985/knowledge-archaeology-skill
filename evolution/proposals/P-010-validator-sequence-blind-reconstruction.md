---
proposal_id: P-010
title: "Validator 时序盲重建 —— Blind Reconstruction 强制重建关键时序与家族枚举"
priority: P1
risk: High
changed_paths:
  - "protocols/blind-reconstruction.md"
  - "agents/truth-auditor.md"
why: "6 Validator 全 PASS + Blind Reconstruction 8/8 无推翻，仍漏 F-05 顺序错误、7 项 MISSING、KO-03 scope 泛化——盲重建覆盖'知识存在性'，不覆盖'时序正确性'与'家族枚举完整性'。v1 F-004（False Acceptance）同族变体。"
validation:
  - "Layer 5 mutation: 存在性正确但时序错误的 claim → validator 必须 detect"
  - "Layer 3 regression: deepseek-harness 时序盲重建 gold record"
status: "proposed"
---

## 变更内容
1. **protocols/blind-reconstruction.md**：盲阶段（阶段 A）新增强制输出——`rebuilt_sequence`（从代码重建的关键时序）+ `rebuilt_family_inventory`（从代码重建的机制家族实例清单）；阶段 B 对比时缺失任一 → 未通过。
2. **agents/truth-auditor.md**：truth 判定从"claim 有证据支持"扩展为"claim 有证据支持 且 时序/枚举完整"（sequence_truth + enumeration_truth）。

## 自动化 Regression Case
- ✅ 可自动化：`sequence_truth_mutation`（存在性正确、顺序错误的 claim → validator detect）+ `family_enumeration_truth_mutation`。

## 风险分析
- 影响面：protocols（blind-reconstruction 核心协议）+ truth-auditor → **High**（永不自动 merge）。
- 回退风险：盲重建是既有协议，新增输出字段为增量；已有测试不受影响。
