# Promotion（晋升协议）— v2 · Abstraction Promotion Gate

> L1→L5 逐级晋升，每级过 Validator。禁止一次生成 L5。
> v2 强化：**每次晋升都是独立的 Gate 判定，不是 Synthesizer 的自我声明。**
> 背景：Codex v1 Benchmark 发现 KO-03（递归模型）属于"证据正确 → Pattern 过度泛化"——
> 问题不在证据，而在晋升时缺少独立判定。因此 v2 把晋升从"流程"升级为"Gate"。

## 晋升链（Gate 化）

```
L1 Candidate → L1 Gate → L2 Deriver → L2 Gate → L3 Pattern Miner → L3 Gate
→ L4 Model Builder → L4 Gate → L5 Methodology Candidate → L5 Gate
```

每级 Gate 由 **abstraction-auditor** 独立判定（不读 Synthesizer 的自我论证）。

## 每次晋升必须证明（三条件 + 显式论证块）

晋升候选必须产出**显式论证块**（写入 KO 的 `derivation`），逐条回答：

```
晋升目标: L2 → L3
论证块:
 1. New explanatory power
    - 新增解释了什么机制/现象？【不能只说"更抽象了"】
    - 新层级能否解释 ≥1 个此前无法解释的观察？
 2. Supporting evidence
    - 哪些独立证据（EV-xxx）支撑这一层？
    - 至少 ≥2 独立实例（否则只能标 Observed Structure，不得标 Pattern）
 3. Scope validity
    - 解释范围从哪扩大到哪？（单模块 → 项目 → 通用）
    - 跨项目推广是否已验证？未验证必须标 pending
```

**不产出论证块 = 不晋升。** 默认停留在当前层级。

## 降级（Gate 的核心价值）

```
L4 candidate
  → abstraction-auditor 独立判定：解释范围未扩大 / 只解释一个模块 / 无 ≥2 实例
  → demote（L4→L3 / L3→L2 / L5→L4）
  → 降级必须记录原因（供 benchmark 统计 over-generalization 被阻止次数）
```

## 各层 Gate 判定要点

| 层 | 晋升判据 | 不满足则 |
|----|---------|---------|
| L1→L2 | 解释了 Why 而非复述 What（禁止同义反复：L2_INVALID_TAUTOLOGICAL） | 保持 L1 |
| L2→L3 | ≥2 独立实例的 Observed repeated structure | 标 Observed Structure（不得升 Pattern） |
| L3→L4 | 认知模型解释 ≥2 个不同机制（否则 L4_OVERREACH） | 降回 L3 |
| L4→L5 | 跨上下文适用性 + 已知例外清单 + 多项目证据（否则标 pending） | 标 Cross-project validation pending，不升 L5 |

## 与 Counterexample Hunter 的联动

- 升维候选先经 counterexample-hunter 反例压力测试（反例预算 ≥3 个/高价值 KO）
- 反例推翻 → 不晋升，或条件化后晋升
- 反例只是边界化 → 晋升但 claim 必须写入例外

## 禁则

- ❌ 不跨级（L1 直接跳 L5）
- ❌ 不因"内容复杂"晋升（要看解释范围，不是复杂度）
- ❌ 不因"写得很专业/引用了证据"晋升（v1 教训：形式完整 ≠ 晋升有效）
- ❌ 单一项目证据不升 L5 成"方法论"（需跨项目，否则标 pending）
- ❌ Synthesizer 不得自我判定自己的晋升（必须由 abstraction-auditor 独立执行）
