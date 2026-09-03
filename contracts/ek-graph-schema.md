# EK Graph Schema（工程知识关系契约）— v3.1

> 解决 v3 暴露的核心缺陷：**52 条 EK 是扁平清单，只有分类没有连接，导致 EK 层退化成"模块说明"**。
> v3.1 定义：EK 之间必须通过**显式边（links）**连接成图；KO 必须通过**聚合规则（aggregation_rule）**从 EK 图的簇中生成，而非考古者拍脑袋分组。

## 核心原则

1. **EK 不是孤立的条目，是图的节点。** 每条 EK 必须有 ≥1 条出边或入边（`links`），指向它依赖/共享/约束的其他 EK。
2. **KO 不是手工挑选的 EK 列表，是 EK 图上的簇。** 每个 KO 必须声明 `aggregation_rule`：用了哪条聚合规则、簇内 EK、通过什么边连通。
3. **聚合规则必须可判定。** 不允许"因为这几条 EK 都关于 exec_policy 所以放一起"——那只是子系统分类，不是知识聚合。

## 一、EK 边类型（Edge Types）

每条 EK 的 `links` 数组声明它与其他 EK 的关系。共 6 类边：

| 边类型 | 语义 | 方向 | Codex 实例 |
|--------|------|------|-----------|
| `mechanism` 同机制边 | 共享同一实现机制/模式（如 Weak ref、fail-closed、ArcSwap 热更新） | 无向 | EK-10↔EK-11（都是 Weak ref 断环）；EK-19↔EK-25↔EK-26（都是保守降级） |
| `subsystem` 同子系统边 | 属于同一子系统/模块（exec_policy / guardian / network_approval / context / rollout_budget / permission / agent_control / sandboxing） | 无向 | EK-01↔EK-02↔EK-09↔EK-20↔EK-27↔EK-28↔EK-37↔EK-40↔EK-49（都是 exec_policy） |
| `causal` 因果边 | A 导致/触发 B（数据流/控制流的先后依赖） | 有向 A→B | EK-01（三态决策）→EK-18（Honor 门控）→EK-21（修正案生成）→EK-02（持久化） |
| `dependency` 依赖边 | A 依赖 B 的运行时行为（A 的实现正确性依赖 B 提供的保证） | 有向 A→B | EK-19（回调降级）依赖 EK-25（fail-closed deny）保证安全性 |
| `constraint` 约束边 | A 是 B 的边界/前置条件（B 成立的前提是 A 不违反） | 有向 A→B | EK-33（deny-read→NoOverride）约束 EK-16（profile 同步） |
| `contrast` 对照边 | 同一问题的两种解法，互为对照（同一主题下不同策略） | 无向 | EK-19（ask 降级）↔EK-25（deny 降级）：同一"保守降级"主题两种策略 |

**字段结构：**
```json
{
  "links": [
    {"to": "EK-02", "type": "causal", "direction": "out", "note": "三态决策结果触发修正案持久化"},
    {"to": "EK-10", "type": "mechanism", "direction": "undirected", "note": "同为 Weak ref 断环"},
    {"to": "EK-33", "type": "constraint", "direction": "in", "note": "deny-read 限制约束 profile 同步边界"}
  ]
}
```

## 二、聚合规则（Aggregation Rules）

KO 必须由 EK 图上的**簇（cluster）**生成。四种聚合路径：

### R1 · 机制簇（Mechanism Cluster）
- **触发**：≥2 条 EK 通过 `mechanism` 边连通，且**同一机制在 ≥2 个独立子系统/文件出现**
- **判据**：跨实例（不是单个文件内的重复）→ 有 Pattern 潜质
- **Codex 实例**：EK-10/EK-11（Weak ref）+ EK-19/EK-25/EK-26（保守降级）→ KO-07 控制面生命周期保守降级

### R2 · 因果链簇（Causal Chain Cluster）
- **触发**：EK 沿 `causal` 边形成完整链（产生→验证→授权→执行→记录）
- **判据**：链完整覆盖"决策→执行→记录"全流程，每段有 EK 支撑 → 完整机制故事
- **Codex 实例**：EK-01→EK-18→EK-21→EK-02→EK-20→EK-27（三态→门控→生成→持久化→过滤→幂等）→ KO-02 策略持久化模型

### R3 · 不变量簇（Invariant Cluster）
- **触发**：多条 EK 通过 `constraint` 边汇聚到**同一安全不变量**
- **判据**：存在跨层（数据层+执行层）实现同一不变量的 EK → 原则级
- **Codex 实例**：EK-06/EK-16（数据层保留 deny-read）+ EK-33（执行层 NoOverride）→ KO-08 一致性保护的 SSOT

### R4 · 主题簇（Thematic Cluster）
- **触发**：多条 EK 围绕同一工程主题，覆盖该主题的不同方面（结构互补而非重复）
- **判据**：主题明确 + EK 覆盖互补维度 → 某机制的整体模型
- **Codex 实例**：EK-08/EK-22/EK-24/EK-36/EK-51（规则+trait+预算三层上下文）→ KO-05 上下文治理

## 三、聚合成立的必要条件（Cluster → KO）

不是所有簇都值得成 KO。**同时满足全部 5 条**才可晋升：

1. **内聚性**：簇内 EK 通过 ≥1 类边互相连通（不是孤立散点）
2. **跨实例性**：机制簇需 ≥2 独立实例；因果链需完整覆盖；不变量簇需跨层
3. **解释范围扩大**：KO 的 claim 比任一成员 EK 的解释范围大（升维的实质，不是文字更抽象）
4. **可命名**：簇能给出清晰名称（命名不出来 = 还没找到共性，不成 KO）
5. **可回溯**：KO 的 `derivation.facts` 正好等于簇内 EK，不多不少（多一个=夹带，少一个=漏支撑）

## 四、防退化检查（EK 层质量门）

每个 EK 簇/KO 生成后执行：

- [ ] **孤立检测**：所有 EK 是否都有 ≥1 条边？孤立 EK = 要么是模块说明（需重写为知识），要么是项目局部事实（标 D 级）
- [ ] **连通性**：是否所有 EK 都能通过边连到 ≥1 个 KO 簇？（游离 EK 数 = 质量指标，正常应 <20%）
- [ ] **聚合规则声明**：每个 KO 是否有 `aggregation_rule`（R1-R4 + 簇内 EK + 边类型）？
- [ ] **无拍脑袋分组**：KO 的 derivation.facts 是否与聚合规则声明的簇一致？（不一致 = 分组是随意的）

## 五、质量指标（v3.1 新增）

- EK 平均出边数（≥1 为合格）
- 游离 EK 比例（未连接任何 KO 簇的 EK 数 / 总数，<20% 为合格）
- 聚合规则覆盖率（有 aggregation_rule 的 KO 数 / KO 总数 = 100%）
- KO 平均簇规模（derivation.facts 数量，3~12 为健康，>15 说明 KO 过宽需拆）

## 铁律

- ❌ 禁止把"同子系统"当作聚合理由（那只是分类，不是知识）
- ❌ 禁止 KO 无 aggregation_rule（= 拍脑袋分组）
- ❌ 禁止为凑数量把不相干的 EK 拉进簇（污染 KO 的解释范围）
- ❌ 禁止删除孤立 EK——孤立 EK 要么被重新连接，要么降级为 D 级项目局部知识，不能消失
