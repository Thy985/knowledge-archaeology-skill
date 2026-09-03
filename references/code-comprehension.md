# 开源项目代码理解清单（Code Comprehension Checklist）

> 用于 Step 1：在识别知识对象之前，先用这份清单建立对项目的系统心智模型。
> 原则：**知识考古的前提是真正读懂项目怎么运作**。不读懂系统，后面所有"认知模型"都是臆想。
> 本清单同时承担"证据预收集"职责——每个视角的发现，直接流向后续的 Flow Atlas / 决策模式 / 失败模式。

## 一、阅读代码顺序（不随机打开文件）

```
README → Architecture Docs → 目录结构 → 入口文件 → 核心数据结构 → 核心流程 → 扩展机制 → 测试 → 细节实现
```

- 不要随机打开一个文件 → 陷入函数细节 → 失去整体理解
- 每读一步，先回答"这个项目怎么运作"，再进细节
- Tafcm 示范顺序：README/AGENTS.md → docs/ARCHITECTURE.md + ADR INDEX → 顶层目录 → main.dart → document.dart（sealed 块模型）→ parser/transaction/history → tools/ffx → tests

## 二、12 个理解视角

### 1. 项目定位
- 类型判断：应用 / 框架 / SDK / 基础设施 / 工具链 / Agent 系统 / 数据平台
- 核心痛点：解决什么真正的问题？（用户 / 工程 / 架构 / Agent / 验证 / 协作）
- 一句话模板：**"这个项目通过 X 技术解决 Y 场景中的 Z 问题"**
- Tafcm 例：通过 Flutter 块级 WYSIWYG + 手写 Markdown 解析器，解决移动端专业数学写作中的"所见即所得 + 公式渲染 + 跨平台导出"问题

### 2. 整体架构
- 看：README / ARCHITECTURE.md / docs / examples / 目录结构
- 分析：核心模块（core/runtime/plugins/cli/api/storage/ui）、每模块职责
- 画：输入 → 处理流程 → 核心逻辑 → 输出
- 关注：依赖方向、分层边界、谁依赖谁

### 3. 数据流（Data Flow）
- 数据从哪里进入？数据结构是什么？谁创建？谁修改？谁消费？
- 关注：转换边界（危险区）、单一真相源
- 流向：→ 00.3 Data Flow

### 4. 核心抽象（Core Abstraction）
> 优秀项目最重要的就是抽象。抽象 = 作者认为的稳定边界。
- 找：interface / abstract class / protocol / schema / model
- 例：Kubernetes = Desired State + Controller Loop + Resource Object；Git = Commit + Tree + Blob；Agent 系统 = Task + Agent + Tool + Memory + Runtime Event
- 流向：→ L4 认知模型（抽象是稳定关系的载体）

### 5. 生命周期（Lifecycle）
> 系统是状态机。
- 例：Agent: Created → Registered → Running → Waiting → Failed → Recovered → Completed；任务: Created → Planned → Executing → Validated → Finished
- 重点：**状态保存位置 / 变化触发者**
- 流向：→ 00.2 State Flow

### 6. 调度和控制逻辑（谁决定下一步？）
- 例：Agent: User → Planner → Scheduler → Executor；K8s: Controller → Scheduler → Kubelet；工作流: DAG Engine → Node Executor
- **决定系统智能程度**：决策点分布 = 控制权结构
- 流向：→ 00.1 Control Flow

### 7. 扩展机制
- 看：plugin / adapter / hook / middleware / provider
- 例：VS Code Extension API；Claude Code Skill/Tool/MCP Server；K8s CRD/Controller/Webhook
- 重点：**作者把哪些设计成稳定，哪些设计成变化**——这正是"设计边界"的决策证据
- 流向：→ Decision Patterns

### 8. 权限、安全、隔离
- Agent / 云平台 / 运行时重点：权限模型、sandbox、authentication、authorization、resource limit
- 每一步谁拥有执行权？执行边界在哪？
- 流向：→ 00.5 Authority Flow

### 9. 错误处理和可靠性
> 生产级 vs Demo 的关键区别。
- 错误分类：NetworkError / RuntimeError / ValidationError / PermissionError
- 恢复机制：Failure → Retry → Rollback → Recovery
- 可观测性：logging / tracing / metrics / audit
- 流向：→ Failure Patterns

### 10. 测试体系
> 测试暴露作者认为的重要边界。
- unit / integration / e2e / benchmark
- 单元测试覆盖什么？E2E 测什么？有无 golden test / regression test？
- 流向：→ Evidence 体系（capability contract / regression / evidence）

### 11. 技术选型原因
- 不要只看"用了 TypeScript"，要问为什么
- Node.js：插件生态 / 前后端统一语言 / 异步 IO；Rust：高性能 / 内存安全 / 系统级部署；Python：AI 生态 / 科研库丰富
- 流向：→ Decision Patterns（为什么 A 不是 B）

### 12. 模块职责与分层
- 每个模块职责、依赖方向、边界约束（谁不允许 import 谁）
- 流向：→ 架构知识对象

## 三、与考古流程的证据衔接

| 代码理解视角 | 考古去向 |
|-------------|---------|
| 项目定位 / 核心痛点 | Q1（解决什么问题）、产品知识对象 |
| 整体架构 / 模块职责 | 架构知识对象 |
| 数据流 | 00.3 Data Flow |
| 生命周期 | 00.2 State Flow |
| 调度与控制逻辑 | 00.1 Control Flow |
| 权限 / 安全 / 隔离 | 00.5 Authority Flow |
| 核心抽象 | L4 认知模型（稳定边界） |
| 扩展机制 | Decision Patterns（稳定 vs 变化） |
| 错误处理 / 可靠性 | Failure Patterns |
| 测试体系 | Evidence 体系 |
| 技术选型 | Decision Patterns |

**操作要点**：Step 1 读代码时把发现记入对应的"考古去向"，后续 Step 4-6 直接使用，避免回头重读。这就是把"代码理解"变成"知识考古"的衔接点。
