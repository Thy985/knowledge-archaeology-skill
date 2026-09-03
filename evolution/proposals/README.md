# Proposals —— Skill 变更提案

> 每个提案包含：变更内容、风险分级（Low/Medium/High）、验证方式。
> High Risk 提案即使 CI PASS 也必须 Human Gate。

## 提案模板

```yaml
proposal_id: P-XXX
title: ""
risk: "Low|Medium|High"
changed_paths:
  - ""
why: ""
validation:  # 如何证明知识质量没变差
  - "Layer 3 regression: ..."
  - "Layer 5 mutation: ..."
  - "Benchmark: ..."
status: "proposed|approved|merged|rejected"
```

## 风险分级速查

| 风险 | 变更类型 | 自动合并 |
|------|---------|---------|
| Low | prompt clarification / metadata / new detector | ✅（Phase 2 起） |
| Medium | new analysis rule | 人工审 |
| High | epistemic promotion / validation policy / agent orchestration | 🛑 永不自动 |
