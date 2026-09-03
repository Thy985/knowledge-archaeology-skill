---
proposal_id: P-008
title: "Coverage 同构家族枚举 Gate —— 机制家族必须全实例枚举"
priority: P0
risk: High
changed_paths:
  - "agents/coverage-auditor.md"
  - "agents/engineering-knowledge-miner.md"
  - "workflows/archaeology.md"
  - "tests/regression/test_codex_regression.py"
  - "benchmarks/deepseek-harness/*.yaml"
why: "deepseek-harness 的 guard 家族只发现 timeout-policy 遗漏 repeat-tool-reminder；Capability Seam 家族只发现 4 个遗漏 settings；approval 策略层只发现一层遗漏 override/delegation。coverage-auditor 的强制覆盖以'子系统'为粒度，未强制'机制家族全实例枚举'。这与 v1 F-003（exec_policy 遗漏）同族反复。"
validation:
  - "Layer 3 regression: 新增 deepseek-harness 家族枚举 gold records（guard/seam/approval-policy-layer）"
  - "Layer 4 benchmark: 现有 gate 不回退"
  - "Layer 5 mutation: 家族遗漏 mutation → detect=true"
status: "pending_human_gate"  # CI 全 PASS；HIGH/Medium 风险 → 治理阻止自动合并，待 Owner 审查
---

## 变更内容
1. **agents/coverage-auditor.md**：新增"同构家族枚举"步骤——识别机制家族（guard/seam/policy-provider/approval-layer…），对每个家族强制枚举全部实例（从依赖图/目录/注册表扫描），缺任一实例 → `CRITICAL FAMILY MISSING`。
2. **agents/engineering-knowledge-miner.md**：EK 提炼时对机制家族成员必须逐一评估，禁止"一个代表即覆盖"。
3. **workflows/archaeology.md**：覆盖矩阵增加"家族枚举"列。
4. **tests/regression**：新增家族枚举 checker（gold record 声明家族实例清单，考古结果缺失任一 → FAIL）。
5. **benchmarks/deepseek-harness/**：新增 guard 家族、seam 家族、approval 策略层 gold records。

## 自动化 Regression Case
- ✅ 可自动化：`required_family_instances`（家族实例枚举 gold record）+ mutation（家族漏项 detect）。

## 风险分析
- 影响面：coverage-auditor / engineering-knowledge-miner / archaeology workflow → **High**（永不自动 merge）。
- 回退风险：新增"家族枚举"为新增检查，不影响既有子系统覆盖逻辑；gold records 为新增 fixture。
