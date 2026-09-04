---
proposal_id: P-015
title: "self-defense 维度补强 —— 核对失效路径必须显式报告（over-declaration / unparsable）"
priority: P1
risk: High
changed_paths:
  - "agents/coverage-auditor.md"
why: "SkillFortify 考古（ARCH-2026-09-05-001）暴露 IF-1：over-declaration 防护（声明 ADMIN>=3 或通配 -> HIGH A6）+ unparsable 声明 fail-safe（LOW）在考古包中 MISSING，仅独立 Auditor 发现。P-013（已合入）的 self-defense 维度聚焦输入通道/信任边界/bypass，但未覆盖'核对失效路径'——安全系统在'核对无法进行'时如何显式报告而非静默放行。此为 P-013 的补强。"
validation:
  - "Layer 3 regression: self-defense 核对失效 gold record（声明过宽/unparsable 必须被考古为'显式报告'机制）"
  - "Layer 4 benchmark: 现有 gate 不回退"
status: "proposed"
---

## 变更内容
1. **agents/coverage-auditor.md**（P-013 补强）：self-defense 维度增加"核对失效路径"子项——安全/验证系统遇到（a）输入过宽导致无法约束（over-declaration/wildcard）、（b）无法解析的声明/配置、（c）近似盲区时，是否显式报告（HIGH/LOW finding）而非静默 PASS。缺失则报 coverage MISSING。

## 自动化 Regression Case
- ✅ 可自动化：`self_defense_check_failure_paths` gold record（核对失效显式报告必须被考古）。

## 风险分析
- 影响面：agents 提示词（coverage-auditor）→ **High**（agents/**，永不自动合并）。
- 回退风险：纯提示词强化，无引擎逻辑变更。
