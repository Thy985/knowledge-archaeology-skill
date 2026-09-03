# Evolution —— Skill 进化记录

> 本目录记录 knowledge-archaeology 的进化历史：失败、提案、晋升。
> 每一次 Skill 变更都必须回答：**知识质量有没有变差？**

## 目录

| 目录 | 用途 |
|------|------|
| `failures/` | 已发现的 Skill 缺陷（Failure Modes）——每次考古发现的缺陷都记录于此，并转化为 Regression/Mutation 用例 |
| `proposals/` | Skill 变更提案（含风险分级：Low/Medium/High） |
| `promotion/` | 晋升记录——新 Skill 版本对比旧版本的 Benchmark 指标 |

## Progressive Autonomy（渐进自治）

| Phase | 规则 | 状态 |
|-------|------|------|
| Phase 1 | CI PASS → Agent 建 PR → Human 审 | 默认（当前） |
| Phase 2 | CI + historical benchmark PASS → low-risk auto merge | CI 已支持（label: auto-merge-low-risk） |
| Phase 3 | 连续 N 次成功 → 自动 Promotion | 待启用 |
| Phase 4 | 重大 Skill 架构改变 → 永远人工 Gate | CI 已强制（high-risk paths） |

## 风险分级

| 风险 | 变更类型 | 自动合并 |
|------|---------|---------|
| Low | prompt clarification / metadata / new detector | ✅（Phase 2 起） |
| Medium | new analysis rule | 人工审 |
| High | epistemic promotion / validation policy / agent orchestration | 🛑 永不自动 |

## v1 → v2 基准（Codex 实验）

| 指标 | v1 | v2/v3 | 结论 |
|------|----|-------|------|
| False Acceptance | 43% | ~8% | Abstraction Gate + Independent Auditor 生效 |
| Critical Coverage | 缺 3 大机制 | 补全 6 项遗漏 | Policy/Governance Analyst 生效 |
| Fact Error | 1（三态/四态） | 0 | Source Truth Gate 生效 |
| Over-generalization | 1（递归模型） | 0 | Observed Structure ≠ Pattern 规则生效 |
