# Epistemic Status（认知状态契约）

> 每个 Knowledge Object 必须明确处于哪个认知状态。未验证的假设不假装成知识。
> 升级状态 = 有新的证据/解释范围，不是"我们觉得应该升级"。

## 状态谱系

```
Fact → Observation → Hypothesis → Validated Pattern → Principle → Law
```

| 状态 | 含义 | 证据要求 | 能否升维 |
|------|------|---------|---------|
| Fact | 项目内存在的事实 | S0-S3（有来源） | 可（作为 L1） |
| Observation | 单源观察 | 至少 1 个 Evidence | 需三角印证 |
| Hypothesis | 待验证假设 | 有理由相信 + 缺证据 | 需明确 Validation Path |
| Validated Pattern | 多源印证的模式 | S4+，≥2 独立源 | 可（作为 L3/L4） |
| Principle | 本项目验证的原则 | S5+，运行时/人工确认 | 可（作为 L4/L5） |
| Law | 普遍定律 | **S8 跨项目验证** | 否则不标 |

## 跨项目规则

- 只有 Tafcm 证据 → `Tafcm-originated · Strongly evidenced · Cross-project validation pending`
- 未跨项目验证的 Principle **禁止**表述为 Law
- 每个 Principle 必须带：该项目验证证据 + 跨项目验证缺口

## 升级门禁（Epistemic Promotion Pipeline）

```
L1 Candidate → Validator → L2 Deriver → Validator → L3 Pattern Miner → Validator
→ L4 Model Builder → Validator → L5 Methodology Candidate → Validator
```

每升一级必须证明：
1. **New explanatory power**：解释范围确实扩大（不只是文字变抽象）
2. **Supporting evidence**：有证据支撑，不是臆想
3. **Scope validity**：解释范围扩大是合理的（单模块经验 → 项目 Pattern 需要论证）

若无法证明：
```
L4 candidate → cannot justify → demote to L3
```

## 诚实性规则

- 禁止把 Hypothesis 写成 Validated Pattern
- 禁止把项目内经验写成普遍定律
- 允许"未验证"存在——Candidates 就是干这个的

## 高风险跃迁清单（v2 重点，Codex 教训）

以下跃迁必须被 epistemic-auditor 拦截：

| 跃迁 | 例子（Codex v1） | 处理 |
|------|-----------------|------|
| ADR intention → implementation fact | ADR 说三态，代码是四态 | 降级为设计意图，不标实现事实 |
| single example → pattern | 一个递归模型包装成高阶 Pattern | 标 Observed Structure，不升 Pattern |
| project pattern → universal principle | 项目局部经验写成通用原则 | 标 Cross-project validation pending |
| Fact → Principle（无中间推导） | 单个事实直接宣布为原则 | 必须逐级推导，否则降级 |

> 升级状态 = 有新的证据/解释范围，不是"我们觉得应该升级"；"写得很专业/引用了证据"也不构成升级依据。
