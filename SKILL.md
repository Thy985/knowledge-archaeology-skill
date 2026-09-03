---
name: knowledge-archaeology
version: 3.1
description: Multi-Agent Knowledge Archaeology System —— 把一个软件项目（仓库/代码/文档/ADR/测试/Issue/RUN/审计）只读"考古"成可长期复用、可升维、可落飞书知识库的知识资产。核心命题是"这个项目让我们认识到了什么"而非"这个项目有什么"。与单 Agent 顺序执行的区别：发现/提炼/升维/验证分离为相互制衡的认知角色，Agent 之间只传递结构化 Artifact（Evidence Pack / Knowledge Object），由 Orchestrator 调度、冲突裁决、质量闭环。v2 变更：①Validator 强制 Blind Reconstruction ②Abstraction Promotion Gate ③反例预算制 ④Policy Flow 第七类流 + policy-governance-analyst ⑤Flow→KO 交叉校验门。v3 变更：①**三层知识架构**（Project Layer / Engineering Knowledge / Generalized Knowledge）②新增 engineering-knowledge-miner ③"宽底座 + 窄尖顶"原则 ④knowledge_layer 字段 ⑤飞书三层交付。**v3.1 变更：①EK 不是扁平清单，是图（EK Graph）——每条 Engineering Knowledge 必须声明 links（6 类边：mechanism/subsystem/causal/dependency/constraint/contrast）②KO 不是手工挑选的 EK 列表，是 EK 图上的簇——每个 KO 必须声明 aggregation_rule（R1 机制簇 / R2 因果链簇 / R3 不变量簇 / R4 主题簇）③新增 contracts/ek-graph-schema.md 定义边类型、聚合规则、簇成立五条件、防退化质量门。**触发场景：用户要求整理项目知识、做知识库、提炼项目经验/方法论/认知模型、把项目沉淀到飞书知识空间、项目复盘升维、跨项目模式提炼、深度项目理解。
---

# Multi-Agent Knowledge Archaeology v3.1

把工程项目从"事实"升维成"认知模型"的**认知生产系统**。本 skill 由 Tafcm 考古任务迭代而来，已从"单 Agent 顺序执行"升级为"多 Agent 分工、交叉验证、冲突裁决、质量闭环"的架构。v2 由 Codex v1 Benchmark（Status: FAILED QUALITY GATE）驱动——该基准暴露了过度综合/过度升维/同源自我确认三大缺陷，v2 用 F1-F6 设计需求逐一修复。v3 由用户方法论升级驱动——知识库不能只有"升维后的知识"，原始事实、关键实现、失败案例、决策过程同样是认知资产（见 `benchmarks/codex/lessons-for-v3.md（本 skill 的基准演进记录，见 workflows/benchmark.md）`）。**v3.1 由 Codex v3 考古的 EK 退化风险驱动**——52 条 EK 只有分类（7 类）没有连接（边），KO 引用 EK 是多对多但无聚合规则，导致 EK 层退化成"模块说明"；v3.1 用 EK Graph（6 类边）+ 聚合规则（R1-R4）修复（见 `contracts/ek-graph-schema.md`）。

## 第一原则

- **仓库 = 工程事实 / 可执行资产；知识库 = 提炼的知识 / 认知资产**
- **发现 ≠ 提炼 ≠ 升维 ≠ 验证**——这四件事天然存在认知冲突，必须由不同角色承担，禁止同一角色自我确认
- **Agent 之间只传递结构化 Artifact，不传递长文本报告**——否则退化为"token 接力"，不是真协作
- **验证 = 重新做一遍再判断**（Blind Reconstruction），不是"证明这个答案没问题"
- **只读**：禁止修改代码/文档/ADR/Issue/PR/git history；飞书写入需用户授权
- 核心问题永远是：**"这个项目让我们认识到了什么？"**

## v3 核心：三层知识架构（宽底座 + 窄尖顶）

> **知识库不能只有"升维后的知识"。** 原始事实、关键实现、失败案例、决策过程同样是认知资产，只是层级和用途不同。
> **"不够抽象"绝不等于"不重要"**——底层工程知识是未来推理的原材料（有损压缩的上层 KO 需要无损底座支撑回退推导）。

```
                    Codex Knowledge Base
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
       Project Layer                Knowledge Layer
              │                           │
              ▼                    ┌──────┴──────┐
   Engineering Facts         Engineering     Generalized
   / Decisions /             Knowledge       Knowledge
   Mechanisms /              (L1/L2)         (L3/L4/L5)
   Failures / Tests                          └→ KO-01~07
```

| 层 | 回答 | 内容 | 价值 |
|----|------|------|------|
| **Project Layer** | Codex 到底是什么，怎么运行 | 架构/模块/关键组件/配置/生命周期/依赖/入口（项目地图） | 项目事实底座 |
| **Engineering Knowledge** | 具体怎么解决工程问题 | 核心机制/关键实现/关键决策/失败与修复/测试揭示的行为/重要配置/边界与例外 | **推理原材料（无损底座）** |
| **Generalized Knowledge** | 可迁移的模式/模型/原则 | L3 Pattern / L4 Cognitive Model / L5 Methodology | 压缩后的可检索认知 |

### 三层的纵向知识链（每一条都必须成立）

```
Engineering Fact（Weak<Session> 防止循环引用 —— L1）
    ↓
Engineering Knowledge（代理层拦截 + 控制面动态决策 + 生命周期保守降级 —— L2）
    ↓
Pattern（代理层回调 + 控制面决策 + 生命周期降级 是可复用模式 —— L3）
    ↓
Cognitive Model（执行面与决策面解耦，控制面生命周期影响执行面安全降级 —— L4）
```

**关键**：不需要每条 Engineering Fact 都升到 L4。**每一种知识都存在它最合适的抽象层。** 升维是特例不是默认——只有少量内容真正值得提升为跨项目认知。

### 宽底座 + 窄尖顶（v3 目标形态）

```
                L5                     ▲
               ▲                       │
              / \                      │ 窄尖顶：
             / L4\                     │ 只有 7~12 Core KO
            /─────\                    │ 真正值得跨项目升维
           /  L3   \                   │
          /─────────\                  │
         / L2        \                 │
        /─────────────\                │
       / L1 / Engineering\             │ 宽底座：
      /───────────────────\            │ 40~60 Engineering Knowledge
     Repository Evidence              ▼ 100+ Facts
```

**理想数量配比**：100+ Evidence/Facts → 40~60 Engineering Knowledge → 15~25 Patterns → 7~12 Core KO。

**为什么必须分层**：
- 高层 Knowledge 是压缩后的可检索认知；底层 Engineering Knowledge 是推理所需的原材料
- 抽象错了 → 可以回到底层重新推导；只保存 KO → KO 错了甚至不知道它是怎么得出来的
- 未来 Agent 遇到新问题（如"如何设计不会悬挂回调的网络审批代理"），需要的是底层事实（Weak<Session> / ActiveNetworkApproval / cancellation_token / ask("not_allowed")），Agent 可以据此重新推理出模式——**不是**直接查一个 L4 结论

## v3.1 核心：EK Graph + 聚合规则（防 EK 退化成模块说明）

> **v3 只解决了"保留工程知识"，但没解决"工程知识如何组织"。** 52 条 EK 如果只是 7 类扁平清单，就会退化成"模块说明"（每个模块写一段）。
> **v3.1 的答案**：EK 不是孤立的条目，是**图的节点**；KO 不是手工挑选的 EK 列表，是**图上的簇**。详见 `contracts/ek-graph-schema.md`。

### EK 六类边（links）——EK 如何互相连接

每条 Engineering Knowledge 必须声明 `links`（≥1 条边），否则它是模块说明（需重写）或项目局部事实（标 D 级）：

| 边类型 | 语义 | 方向 | Codex 实例 |
|--------|------|------|-----------|
| `mechanism` 同机制 | 共享同一实现机制/模式 | 无向 | EK-10↔EK-11（都是 Weak ref 断环） |
| `subsystem` 同子系统 | 同属一个子系统 | 无向 | EK-01↔EK-02↔EK-09↔EK-20（都是 exec_policy） |
| `causal` 因果 | A 触发/导致 B | 有向 A→B | EK-01（三态决策）→EK-18（Honor 门控）→EK-21（修正案生成）→EK-02（持久化） |
| `dependency` 依赖 | A 依赖 B 的运行时保证 | 有向 A→B | EK-19（回调降级）依赖 EK-25（fail-closed deny） |
| `constraint` 约束 | A 是 B 的边界/前置条件 | 有向 A→B | EK-33（deny-read→NoOverride）约束 EK-16（profile 同步） |
| `contrast` 对照 | 同一问题的两种解法 | 无向 | EK-19（ask 降级）↔EK-25（deny 降级） |

### KO 聚合规则（R1-R4）——EK 如何聚合成 KO

KO 必须从 EK 图上的**簇**生成，通过四种聚合路径：

- **R1 机制簇**：≥2 EK 共享机制边，且同一机制跨 ≥2 独立子系统/文件出现 → Pattern 潜质（Codex: EK-10/11/19/25/26 → KO-07）
- **R2 因果链簇**：EK 沿 causal 边形成完整链（决策→执行→记录）→ 完整机制故事（Codex: EK-01→18→21→02→20→27 → KO-02）
- **R3 不变量簇**：多条 EK 通过 constraint 边汇聚到同一安全不变量 → 原则级（Codex: EK-06/16+EK-33 → KO-08）
- **R4 主题簇**：多条 EK 围绕同一主题、覆盖互补维度 → 机制整体模型（Codex: EK-08/22/24/36/51 → KO-05）

**簇成立五条件（缺一不可）**：内聚性 / 跨实例性 / 解释范围扩大 / 可命名 / 可回溯。

**反退化铁律**：
- ❌ 聚合理由是"都属于某子系统" → 那只是**分类**，不是**知识**（子系统是 subsystem 边，不是聚合规则）
- ❌ KO 无 `aggregation_rule` → 拍脑袋分组，不通过
- ❌ 孤立 EK 直接删除 → 要么被重新连接，要么降级 D 级，不能消失

## 架构总览（认知生产管线）

```
                        Repository
                              │
                              ▼
                      Orchestrator（调度/冲突/裁决/质量门）
                              │
      ┌───────────┬───────────┼───────────┬───────────┬─────────────┬──────────────┐
      ▼           ▼           ▼           ▼           ▼             ▼              ▼
  Code      Doc/ADR    Test     Failure   Authority  Policy/Governance  repository-mapper
  Analyst   Analyst    Analyst  Analyst   Analyst    Analyst (v2)      → Project Layer
      │           │           │           │           │             │
      └───────────┴───────────┴───────────┴───────────┴─────────────┘
                              ▼
              Evidence Assembly（证据融合，非知识生成）
                              │
      ┌───────────────┬───────┴───────┬───────────────┬──────────────┐
      ▼               ▼               ▼               ▼              ▼
 Problem Miner   Decision Miner   Pattern Miner   Flow Miner   Engineering Knowledge
                                                              Miner (v3.1: EK + links)
      │               │               │               │              │
      └───────────────┼───────────────┴───────────────┴──────────────┘
                      ▼
            Knowledge Synthesizer（Flow→KO 交叉校验门 + EK→KO 聚合规则 R1-R4）
            （产出：Engineering Knowledge 层（EK Graph）+ Generalized KO 层（aggregation_rule））
                      ▼
        Abstraction Promotion Gate（L1→L5 逐级晋升，独立判定，可降级）
                      │
      ┌───────┬───────┼───────┬───────────┬──────────┐
      ▼       ▼       ▼       ▼           ▼          ▼
 Truth   Coverage  Flow   Abstraction  Counterexample Epistemic
 Auditor  Auditor  Auditor  Auditor    Hunter       Auditor
（全部先 Blind Reconstruction）
      │       │       │       │           │          │
      └───────┴───────┴───────┴───────────┴──────────┘
                      ▼
                  Reconciler（显式处理设计意图≠实现≠测试≠运行时）
                      ▼
           ┌─────── Accepted ───────┐
           ▼                         ▼
    Final Package              Revise → Re-analysis（反馈控制）
```

**v3 关键差异**：Knowledge Synthesizer 现在产出**两层**——Engineering Knowledge（L1/L2，宽底座）与 Generalized Knowledge（L3/L4/L5，窄尖顶）。两者都是正式交付物，**Engineering Knowledge 不是"未完成的 KO"**，而是独立价值的推理原材料。

## Orchestrator（大脑，但绝不自己分析仓库）

职责只限：任务分解 / 角色调度 / 证据路由 / 冲突检测 / 重试 / 升级 / 质量门。不分析仓库。

**角色激活条件（裁剪规则，防止小项目跑不动）：**

| 角色组 | 激活条件 |
|--------|---------|
| Code / Doc / Test Analyst | 总是激活（三视角基线） |
| Failure Analyst | 仓库存在修复史 / 大量 bugfix commit / regression 目录 |
| Security/Authority Analyst | 项目含 Agent / 运行时 / 权限模型 / 沙箱 / 插件执行 |
| Policy/Governance Analyst（v2） | 项目含治理/策略/规则文档/自我约束机制（Agent 系统、有 AGENTS.md/policy 文件/governance 层） |
| **Engineering Knowledge Miner（v3）** | **总是激活**（工程知识层是三层架构的必要底座，即便小项目也至少产出核心机制） |
| Pattern / Flow Miner | 项目达到中等规模（多模块、有内核） |
| Counterexample Hunter | 已有升维候选（L3+），需要反例压力测试 |
| Epistemic Auditor | 知识库要落地（飞书/对外交付）时 |
| Security Analyst（全角色版） | 仅大型或高安全敏感项目 |

小项目（< 5k 行）裁剪为：Code + Doc + Test → Evidence Assembly → Engineering Knowledge Miner + Synthesizer → Truth + Coverage Auditor → Reconciler。

## 目录导航

| 目录 | 内容 | 何时读 |
|------|------|--------|
| `agents/` | 18 个角色定义（职责/输入/输出/禁则） | 调度到某角色时读对应文件 |
| `contracts/` | 结构化 Artifact schema（evidence/knowledge/flow/epistemic-status/validation/**ek-graph**） | 任何角色产出/消费 Artifact 前必读 |
| `protocols/` | 协作协议（provenance/handoff/disagreement/escalation/promotion/blind-reconstruction） | 跨角色交接/冲突/晋升/盲重建时 |
| `workflows/` | 主流程（archaeology/validation/benchmark） | 进入对应阶段时 |
| `references/` | 方法论参考（五层阶梯/三层架构/七类流/分类/飞书落地/工作示例） | 各角色执行时 |

## 核心机制（v2 + v3 关键差异）

1. **Epistemic Promotion Pipeline → Abstraction Promotion Gate**：L1→L5 逐级晋升，每级由 abstraction-auditor **独立判定**（不读 Synthesizer 自我论证），须产出显式论证块；无法证明解释范围扩大 → 降级（`protocols/promotion.md`）
2. **Blind Reconstruction（v2）**：所有 Validator 先独立盲重建再对比，杜绝同源自我确认（`protocols/blind-reconstruction.md`）
3. **Evidence Graph 而非记忆**：所有 Miner/Synthesizer 在 Evidence Graph 上推理，不"凭记忆整理"（`contracts/evidence-schema.md`）
4. **Counterexample 优先 + 反例预算制**：升维候选先找"哪里不是这样"；每个 L3+ KO ≥3 个定向反例攻击，0 反例必须给出搜索证据（`agents/counterexample-hunter.md`）
5. **Policy Flow 第七类流（v2）**：治理闭环 Decision→Approval→Policy→Enforcement→Future Decision，由 policy-governance-analyst 调查（`contracts/flow-schema.md`）
6. **Flow→KO 交叉校验门（v2）**：每条 L1 事实必须回溯 Flow Edge（flow_traceability），KO 与 Flow 矛盾不得通过
7. **条件化知识**：Reconciler 显式分离 design_intent / implementation / tested_behavior / runtime_observation，产出 CONDITIONAL 状态而非粗暴 PASS（`protocols/disagreement.md`）
8. **反馈控制**：Revise → Re-analysis，不是一次性生成（`workflows/archaeology.md`）
9. **三层知识架构（v3）**：Synthesizer 产出两层（Engineering Knowledge 宽底座 + Generalized KO 窄尖顶），knowledge-schema 用 `knowledge_layer` 区分；工程知识层不参与升维竞争，独立保留（`agents/engineering-knowledge-miner.md`）
10. **宽底座 / 窄尖顶数量纪律（v3）**：不允许"只保留 7 个 KO 丢掉 100 条事实"；不允许"把 40 条工程知识全升维"——每种知识停留在最合适的抽象层（`references/five-layer-ladder.md` §三层映射）
11. **EK Graph（v3.1）**：每条 Engineering Knowledge 必须声明 `links`（6 类边：mechanism/subsystem/causal/dependency/constraint/contrast）；孤立 EK 要么重写为知识要么降 D 级，不能退化成"模块说明"（`contracts/ek-graph-schema.md`）
12. **聚合规则（v3.1）**：每个 KO 必须声明 `aggregation_rule`（R1 机制簇 / R2 因果链簇 / R3 不变量簇 / R4 主题簇 + 簇内 EK + 边类型）；聚合理由禁止"都属于某子系统"（那是分类不是知识）；簇成立须满足内聚性/跨实例性/解释范围扩大/可命名/可回溯（`contracts/ek-graph-schema.md`）

## 角色清单速览（18 角色）

| 阶段 | 角色 | 一句话职责 |
|------|------|-----------|
| Discovery | repository-mapper | 建立仓库地图 + Project Layer（项目地图） |
| Discovery | code-analyst | 从代码提取架构/控制流/状态/抽象/边界证据 |
| Discovery | doc-analyst | 从文档/ADR 提取设计意图（但不能当实现事实） |
| Discovery | test-analyst | 测试 = 可执行知识，提取系统真正重视的行为 |
| Discovery | failure-analyst | 找系统付出认知成本的地方（修复/回退/绕过/异常） |
| Discovery | authority-analyst | 权限/信任边界/执行权威/沙箱（Agent/runtime 项目） |
| Discovery | policy-governance-analyst（v2） | 治理闭环/自我约束/策略固化/上下文治理 |
| Fusion | evidence-assembler | 把多源证据融合成 Evidence Graph |
| Mining | problem-miner | 找 Problem/Constraint/Pain/RootCause |
| Mining | decision-miner | 找 Decision/Alternative/Trade-off/Rejected |
| Mining | pattern-miner | 只找重复结构，不得自行宣布原则 |
| Mining | flow-miner | 构建七类 Flow（Control/State/Data/Evidence/Authority/Memory/Policy） |
| Mining | **engineering-knowledge-miner（v3/v3.1）** | **提炼 L1/L2 工程知识层 + 声明 EK 边（links）——EK 是图的节点不是孤立条目** |
| Synthesis | knowledge-synthesizer | 在 Graph 上做 L1-L5 合成 + Flow→KO 交叉校验 + **EK→KO 聚合规则（R1-R4）**；产出 Engineering + Generalized 两层 |
| Validation | truth-auditor | 这句话是真的吗？（先盲重建，只引用仓库证据） |
| Validation | coverage-auditor | 还有什么重要东西没发现？（独立重搜 + 强制子系统覆盖） |
| Validation | flow-auditor | Flow Atlas 是否真的对应代码？（symbol/edge/failure path） |
| Validation | abstraction-auditor | 独立判定 L3/L4/L5 是否过度升维（可降级） |
| Validation | counterexample-hunter | 专门找"哪里不是这样"（反例预算制） |
| Validation | epistemic-auditor | 认知状态标注是否诚实（Hypothesis≠Validated≠Principle） |
| Governance | reconciler | 显式处理多 Agent 冲突（设计/实现/测试/运行时分层） |

## 执行入口

- 完整考古：读 `workflows/archaeology.md`
- 质量验证：读 `workflows/validation.md`
- 基准测试（用已完成项目验证 skill，v3 以 Codex v2 基线为锚）：读 `workflows/benchmark.md`
- 三层架构方法论：读 `references/five-layer-ladder.md` §三层映射 + `references/feishu-delivery.md`
