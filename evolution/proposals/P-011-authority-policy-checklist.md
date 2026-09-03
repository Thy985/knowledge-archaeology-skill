---
proposal_id: P-011
title: "authority/policy 分析清单 —— approval 策略解析链路与 collapse 前置门强制枚举"
priority: P1
risk: Medium
changed_paths:
  - "agents/authority-analyst.md"
  - "agents/policy-governance-analyst.md"
why: "authority-analyst 未枚举 approval 策略解析链路（config 默认层 / session override / delegation 委派继承）与 PTC collapse 前置拒绝契约。approval 策略层是 Agent 权限系统的关键结构，漏一层即漏一种安全语义。"
validation:
  - "Layer 3 regression: 新增 approval 策略层枚举 gold record"
  - "Layer 4 benchmark: 现有 gate 不回退"
status: "proposed"
---

## 变更内容
1. **agents/authority-analyst.md**：审批/权限分析必须枚举完整解析链路——`effectivePolicy = overrideOf(session) ?? config.policy ?? 'ask'`、委派播种（delegation override）、collapse 前置拒绝、guard 家族（enforcer/advisory 两类）。
2. **agents/policy-governance-analyst.md**：策略治理闭环分析必须覆盖策略来源（config/override/delegation）三层与跨子会话传递。

## 自动化 Regression Case
- ✅ 可自动化：`approval_policy_layer_enumeration` gold record（三层解析链路 + delegation + collapse 必须被考古）。

## 风险分析
- 影响面：agents 提示词（分析角色）→ **Medium**（需人工审）。
- 回退风险：纯提示词强化，无引擎逻辑变更。
