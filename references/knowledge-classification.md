# Knowledge Classification（知识分类与分级）

## 〇、EK Graph：工程知识的连接与聚合（v3.1）

> **分类不是知识组织**——把 52 条 EK 分成"核心机制/实现/决策"7 类只是目录，不是连接。真正的工程知识必须通过边（links）连成图（EK Graph），KO 从图上按规则聚合（R1-R4）。详见 `contracts/ek-graph-schema.md`。

### EK 六类边

| 边类型 | 语义 | 方向 | 示例 |
|--------|------|------|------|
| `mechanism` | 共享同一实现机制/模式 | 无向 | EK-10↔EK-11（都是 Weak ref 断环） |
| `subsystem` | 同属一个子系统 | 无向 | EK-01↔EK-02↔EK-09↔EK-20（都是 exec_policy） |
| `causal` | A 触发/导致 B | 有向 A→B | EK-01→EK-18→EK-21→EK-02（决策→门控→生成→持久化） |
| `dependency` | A 依赖 B 的运行时保证 | 有向 A→B | EK-19 依赖 EK-25（fail-closed deny） |
| `constraint` | A 是 B 的边界/前置条件 | 有向 A→B | EK-33 约束 EK-16（deny-read→NoOverride） |
| `contrast` | 同一问题两种解法 | 无向 | EK-19（ask）↔EK-25（deny） |

### KO 聚合规则（R1-R4）

| 规则 | 触发条件 | 示例 |
|------|---------|------|
| R1 机制簇 | ≥2 EK 共享机制边 + 跨 ≥2 独立子系统 | EK-10/11/19/25/26 → KO-07 |
| R2 因果链簇 | EK 沿 causal 边形成完整链 | EK-01→18→21→02→20→27 → KO-02 |
| R3 不变量簇 | 多条 EK 汇聚到同一安全不变量 | EK-06/16+EK-33 → KO-08 |
| R4 主题簇 | 多条 EK 覆盖同一主题互补维度 | EK-08/22/24/36/51 → KO-05 |

**反退化铁律**：聚合理由是"都属于某子系统"→ 分类，不是知识，不合格。

## 一、知识对象分类（至少覆盖以下类别）

PRODUCT / ARCHITECTURE / ENGINEERING / DESIGN / AGENT / RUNTIME / MEMORY / CONTEXT / PERMISSION / TESTING / EVALUATION / TOOLING / WORKFLOW / DECISION / FAILURE / EXPERIMENT / PATTERN / PRINCIPLE / METHODOLOGY

可以增加，但**不要为了分类而分类**。

## 二、Knowledge Object 定义

一个真正的知识对象不能只是"XX 有一个 YYY 模块"。至少具备以下结构的大部分：

```
Problem → Observation → Root Cause → Decision → Implementation → Evidence → Lesson → Abstraction
```

优先寻找这种完整链。

## 三、抽象层级（L0-L4）与三层知识架构（v3）

| 层 | 描述 | 示例 | 价值 | 知识库层（v3） |
|----|------|------|------|---------------|
| L0 Project Fact | 仅描述事实 | Tafcm 使用 Flutter | 低 | Project Layer |
| L1 Implementation | 具体实现 | 用 Parser→Transaction→History 结构 | 中 | Engineering Knowledge |
| L2 Engineering Experience | 经验 | 某职责拆分可降低编辑器状态耦合 | 较高 | Engineering Knowledge |
| L3 General Pattern | 可迁移模式 | 编辑器应将文档状态/事务/历史解耦 | 高 | Generalized Knowledge |
| L4 Principle | 原则 | 复杂状态系统中持久状态/变更/历史不应共享职责边界 | 最高 | Generalized Knowledge |

**v3 铁律（宽底座 + 窄尖顶）：**
- **L1/L2 是独立价值的交付物，不是"未升维的 KO"**——它们是未来推理的原材料与无损底座
- **"不够抽象"绝不等于"不重要"**：底层工程知识（如 `Weak<Session> → session 释放 → ask("not_allowed")`）回答非常具体而重要的问题，设计 API Gateway / Sidecar / Callback Runtime 时可直接复用
- **升维是特例不是默认**：只有少量内容真正值得提升为跨项目认知；每种知识停留在最合适的抽象层
- **目标配比**：100+ Facts → 40~60 Engineering Knowledge → 15~25 Patterns → 7~12 Core KO

**升维铁律**：不要为了升维而升维。只有 Tafcm 单一证据 → 只能写"Tafcm 中验证的实践"，不能写"普遍成立的工程定律"。

## 四、Evidence Strength（证据强度）

| 级 | 含义 | 示例 |
|----|------|------|
| S0 | Opinion | 理论想法 |
| S1 | Discussion | 讨论 |
| S2 | Design Proposal | 设计提案 |
| S3 | Implemented | 已实现 |
| S4 | Test Validated | 自动化测试通过 |
| S5 | Runtime Validated | 真实运行验证 |
| S6 | Physical/Visual Validated | 物理/视觉验证 |
| S7 | Human Confirmed | 人工真实使用确认 |
| S8 | Repeated/Cross-project | Tafcm + 其他项目都验证 |

**证据越强，结论越可升维。** "理论上可以" S0-S2；"已实现" S3；"测试通过" S4；"真实运行" S5；"人工使用" S7；"跨项目" S8。

## 五、Knowledge Value（价值评级）

- A 极高价值 / B 高价值 / C 一般 / D 项目局部 / E 不进知识库

评价维度：可迁移性 / 独特性 / 验证程度 / 长期有效性 / 认知增量 / 是否能指导未来决策。
**不要因为内容复杂就给 A。**

## 六、Epistemic Status（认知状态）

每个知识对象必须明确处于哪个认知状态：

```
Fact → Observation → Hypothesis → Validated Pattern → Principle → Law
```

- 未跨项目验证的原则 = `Principle (Cross-project validation pending)`，不是 Law
- 未验证的假设 = Hypothesis，进 Candidates，不写成知识

## 七、五问判断标准（每个候选知识强制问）

1. **如果这个项目明天不存在了，这个知识还有价值吗？** 没有 → Project Fact；有 → Candidate Knowledge
2. **它能否改变未来某个工程决策？** 不能 → 价值低；能 → 高价值
3. **这个结论是"我认为"还是"项目证据证明"？** 必须明确区分
4. **它有没有可能在另一个项目再次出现？** 有 → Cross-project Candidate
5. **这个经验是偶然还是结构性问题？** 重点找结构性问题
