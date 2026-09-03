# Archaeology Workflow（考古主流程）— v3.1

> 完整执行路径。Orchestrator 按此调度，角色按 agents/ 定义工作。
> v2 变更：①新增 policy-governance-analyst ②flow-miner 构建七类流（+Policy）③Synthesis 加 Flow→KO 门 ④Validation 先 Blind Reconstruction。
> v3 变更：①新增 engineering-knowledge-miner ②Synthesis 产出**两层**（Engineering Knowledge 宽底座 + Generalized KO 窄尖顶）③三层知识架构贯穿 ④Project Layer 由 repository-mapper 明确产出。
> v3.1 变更：①engineering-knowledge-miner 必须为每条 EK 声明 **links**（6 类边，EK 是图的节点）②Synthesis 阶段 KO 必须声明 **aggregation_rule**（R1-R4 聚合规则，EK→KO 从图上的簇生成，禁止拍脑袋分组）③阶段 8 交付 EK Graph + 聚合规则说明。
> v3.2 变更：④**默认交付 = push 到 `knowledge-archaeology-corpus` 仓库**（每项目顶级目录 `<project>/`）⑤**飞书落盘需用户显式授权，默认不做**（交付决策见 `references/delivery.md`）。

## 阶段 0 · 准备

1. **边界声明**：只读、不改仓库；**默认交付 = push 到 `knowledge-archaeology-corpus` 仓库**；**飞书写入需用户显式授权（默认不做）**
2. **角色激活**（Orchestrator 按 SKILL.md 裁剪规则决定哪些角色上场）
3. 启动 `repository-mapper` 建仓库地图 + **Project Layer**（项目地图：架构/模块/配置/生命周期/依赖/入口）

## 阶段 1 · Discovery（多视角独立观察）

并行启动激活的 Discovery Agent，每个从不同 epistemic lens 独立观察：

```
code-analyst    → 实现事实
doc-analyst     → 设计意图（≠ 实现事实）
test-analyst    → 可执行知识（系统重视什么）
failure-analyst → 认知成本（修复/回退/绕过/异常）
authority-analyst → 权限/信任边界/bypass（Agent/runtime 项目）
policy-governance-analyst → 治理闭环/自我约束/策略固化（v2，Agent/治理密集项目）
```

产出：多个 Evidence Pack（结构化，非长文）。

## 阶段 2 · Evidence Fusion

`evidence-assembler` 把多源证据融合成 Evidence Graph：
- ≥2 独立源 = Supported Fact
- 单源 = Unverified Observation（不进入下游）
- 冲突证据保留（标 contradicts）

## 阶段 3 · Mining（分别提炼不同东西）

```
problem-miner   → Problem Graph（问题/约束/痛点/根因）
decision-miner  → Decision Graph（决策/权衡/放弃方案）
pattern-miner   → Pattern Graph（只报重复结构，不宣布原则）
flow-miner      → Flow Atlas（七类流，锚定真实符号，含 Policy Flow）
engineering-knowledge-miner → Engineering Knowledge 层（L1/L2，v3）
                              每条 EK 必须声明 links（6 类边，v3.1）
```

**v3 注意**：engineering-knowledge-miner 与其余 Miner **并行**进行，产出的 Engineering Knowledge 是**正式交付物**，不是中间品。
**v3.1 注意**：EK 不是孤立条目——每条 EK 产出时必须思考并声明它与哪些 EK 相关（共享机制 / 同子系统 / 因果触发 / 依赖保证 / 约束边界 / 互为对照），形成 **EK Graph**。孤立 EK（无边）要么重写为知识，要么标 D 级项目局部知识。

## 阶段 4 · Synthesis（产出两层 + 聚合规则）

`knowledge-synthesizer` 在 Graph + Flow Atlas + **EK Graph** 上做五层合成（L1→L5），产出**两层**知识对象（contracts/knowledge-schema.md）：

```
Engineering Knowledge 层（宽底座）：核心机制/关键实现/决策/失败/配置/边界（L1/L2）
Generalized Knowledge 层（窄尖顶）：L3 Pattern / L4 Model / L5 Methodology
```

**输入是 Graph + EK Graph + Engineering Knowledge 底座，不是"仓库 + 记忆"。**
**每次晋升产出显式论证块**（protocols/promotion.md），**每条 L1 事实带 flow_traceability**（Flow→KO 交叉校验门）。
**generalized 对象必须能回溯到 engineering 底座**（derivation.facts），否则为悬空升维。
**v3.1 聚合纪律**：每个 KO 必须声明 `aggregation_rule`（R1 机制簇 / R2 因果链簇 / R3 不变量簇 / R4 主题簇 + 簇内 EK + 通过什么边连通）。KO 从 EK 图的簇生成，聚合理由必须是机制共享/因果链/不变量/互补主题，**禁止"都属于某子系统"这种分类式理由**。簇成立须同时满足：内聚性 / 跨实例性 / 解释范围扩大 / 可命名 / 可回溯（见 contracts/ek-graph-schema.md）。

## 阶段 5 · Validation（多 Validator 交叉验证，先盲重建）

```
第 0 步: 每个 Validator 先 Blind Reconstruction（protocols/blind-reconstruction.md）
truth-auditor    → 事实核验（独立重建后对比）
coverage-auditor → 独立重搜找盲区 + 强制子系统覆盖（触发新 Investigation 或补角色）
flow-auditor     → Flow 对应代码？（逐 Edge 验证 + Flow→KO 门）
abstraction-auditor → 独立判定晋升是否过度（generalized 层重点）+ 聚合规则是否成立（v3.1）
counterexample-hunter → 反例预算制（≥3 攻击/高价值 KO）
epistemic-auditor → 认知状态诚实？
```

**v3 注意**：validation 覆盖两层——Engineering Knowledge 层验证"事实是否真、边界是否标清、**EK 边（links）是否真实存在**（v3.1）"；Generalized 层验证"升维是否过度、底座是否可回溯、**聚合规则是否成立**（v3.1）"。

任一角色可触发 Escalation（protocols/escalation.md）。

## 阶段 6 · Reconcile

`reconciler` 显式处理冲突，产出条件化知识（design/impl/tested/runtime 分层）。

## 阶段 7 · Quality Gate + 反馈控制

```
全部 Validator PASS（且均完成 Blind Reconstruction）→ Accept → Final Package
任一 blocker       → Revise → 回到对应阶段 Re-analysis
```

**这不是一次性生成报告，而是带反馈控制的认知 Runtime。**

## 阶段 8 · 交付

- **Knowledge Package（三层）**：
  - Project Layer（项目地图）
  - Engineering Knowledge 层（40~60 条，宽底座，**EK Graph：每条带 links 边**）
  - Generalized Knowledge 层（7~12 个 Core KO，窄尖顶，**每个带 aggregation_rule 聚合规则**）
  - Flow Atlas（七类流）
  - Candidates（待验证假说）
- 汇报格式（统计 / Top 高价值 / Top 跨项目模式 / Most Important Finding）
- **v2 指标**：False Acceptance / Critical Missing / Fact Error / Over-generalization（供 benchmark）
- **v3 指标**：三层配比（Facts : Engineering : Generalized）、底座可回溯率、工程层保留完整度
- **v3.1 指标**：EK 平均出边数（≥1 合格）、游离 EK 比例（<20% 合格）、聚合规则覆盖率（100%）、KO 平均簇规模（3~12 健康）

### 交付决策（v3.2，见 `references/delivery.md`）

1. **默认**：push 到 `knowledge-archaeology-corpus` 仓库 `<project>/` 目录（按目录约定整理：00-inventory / 01-project-layer / 02-engineering / 03-knowledge / 04-flow-atlas / 05-candidates / 06-validation）
2. **飞书**：**仅用户显式授权**才执行飞书落盘（读 `references/feishu-delivery.md`），默认不做
3. **仅本地**：用户只要分析不要沉淀时，只交付本地路径 + 汇报，不主动 push
4. 交付前跑一遍 `references/delivery.md` §四自检清单

## 执行约束

- 每个角色读自己的 agents/<role>.md 再执行
- 交接物遵循 protocols/agent-handoff.md
- 升维遵循 protocols/promotion.md（Abstraction Promotion Gate）
- Validator 遵循 protocols/blind-reconstruction.md
- **工程层与认知层分离**：engineering-knowledge-miner 不升维；synthesizer 升维须过 Gate；不允许"只保留 KO 丢弃工程知识"
- **EK 图与聚合（v3.1）**：每条 EK 必须有 links；每个 KO 必须有 aggregation_rule；聚合理由不能是"同子系统"
- 完整考古结束后可运行 workflows/benchmark.md 评估质量
