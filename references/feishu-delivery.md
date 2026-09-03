# 飞书落地（Feishu Delivery）

> **v3.2 前置门槛：本文件仅在用户显式授权后执行（"落飞书 / 建飞书知识库 / 沉淀到飞书"等明确指令）。默认不做飞书落盘——默认交付走 `delivery.md`（push 到 `knowledge-archaeology-corpus` 仓库）。**
> 授权后建议：corpus push（持久档案）+ 飞书落盘（可检索视图）两者都做。
> 先读 lark-wiki / lark-doc skill 再动手。本文件只记录本 skill 验证过的落地模式。

## 三层结构（v3 + v3.1：避免"过度压缩"与"EK 退化"）

```
知识空间「<项目> 知识库」
├── 00 首页 · Knowledge Map（三层导航 + 知识速览 + 认知状态声明）
├── 01 Project Layer                项目地图（是什么、怎么运行）
│   ├── 01.1 项目定位 / 01.2 架构 / 01.3 核心模块 / 01.4 生命周期 / 01.5 依赖与入口
├── 02 Engineering Knowledge        工程知识（宽底座 · 推理原材料）
│   ├── 02.0 EK 关系图谱（v3.1）——六类边 + 聚合规则 + 真实交叉引用（防退化成"模块说明"）
│   ├── 02.1 核心机制 / 02.2 关键实现 / 02.3 关键决策
│   ├── 02.4 失败与修复 / 02.5 测试揭示的行为 / 02.6 重要配置 / 02.7 边界与例外
├── 03 Knowledge Layer              抽象知识（窄尖顶 · 可迁移认知）
│   ├── 03.0 KO 聚合规则矩阵（v3.1）——每个 KO 声明 R1-R4 + 簇内 EK + 解释范围扩大论证
│   ├── 03.1 KO-01 ~ KO-0N（Generalized Knowledge）
│   ├── 03.2 Core Knowledge（跨对象归纳）
│   └── 03.3 Cross-project Candidates（待验证模式）
├── 04 Flow Atlas                   系统流图谱（中间层：七类流，含 Policy Flow）
├── 05 Candidates                   未完成抽象 / 待验证模式 / 跨项目假设
└── 06 Validation & Evidence        证据链 + Validators + 反例 + Reconciliation + 质量指标
```

**原则：**
- **Project Layer** = 项目地图（L0 事实）
- **Engineering Knowledge** = L1/L2 工程知识（核心机制/实现/决策/失败/配置/边界）——**必须保留，是未来 Agent 推理的无损底座**
- **Knowledge Layer** = L3~L5 抽象知识（Pattern / Model / Methodology）
- **三层不是"从低到高的淘汰"，而是"不同用途的并存"**——工程知识层不因"不够抽象"而被丢弃
- **v3.1**：02 层必须含"EK 关系图谱"（六类边 + R1-R4 聚合规则），否则 EK 退化成模块说明；03 层必须含"KO 聚合规则矩阵"（每个 KO 声明聚合规则），否则 KO 是拍脑袋分组
- P1~Pn 统一标注 `Tafcm-originated · Strongly evidenced · Cross-project validation pending`
- Candidates 保持 Hypothesis 标记，标注：L3 模式假设 / 当前证据 / 缺失证据 / 验证路径

### 三层配比检查（交付前核对）

| 层 | 目标数量 | 检查项 |
|----|---------|--------|
| Project Layer | 1 地图 | 架构/模块/配置/生命周期/依赖/入口是否齐全 |
| Engineering Knowledge | 40~60 条 | 是否覆盖核心机制/实现/决策/失败/配置/边界；**每条 EK 是否声明 links（EK Graph）**；**是否因"不够抽象"被丢弃** |
| Generalized KO | 7~12 个 | 是否全部能回溯到 engineering 底座（无悬空升维）；**每个 KO 是否声明 aggregation_rule（R1-R4）** |
| Candidates | 未验证假设 | 是否与 KO 严格区分 |

**v3.1 EK Graph 交付检查**：EK 平均出边数 ≥1；游离 EK 比例 <20%；聚合规则覆盖率 100%；KO 平均簇规模 3~12；无"同子系统=聚合理由"的假聚合。

## 建空间与节点（lark-cli）

```bash
# 列空间拿 space_id
lark-cli wiki +space-list --as user --format json

# 建空间（team/private）
lark-cli wiki +space-create --name "<项目> 项目知识库" --description "..." --as user --format json

# 建节点（返回 node_token + obj_token）
lark-cli wiki +node-create --space-id <SPACE_ID> --title "01 Project Layer" --format json
lark-cli wiki +node-create --parent-node-token <PARENT_NODE> --title "01.1 产品" --format json
```

注意：`node-create` 返回 131003 = 结构限制（节点数/深度/直属子节点数），非瞬时错误，**不要用相同参数重试**；改用更浅父节点或重组。

## 写入文档（lark-cli docs +update）

写前先 Read `lark-doc/online-doc/references/lark-doc-update.md`（本 skill 不替代该规范，仅记录验证过的可行命令）：

```bash
# 在 cwd（项目目录）下，@file 只接受相对路径
lark-cli docs +update --doc "<obj_token>" --command overwrite --doc-format markdown --content "@./_content/01_p1.md" --format json
```

- `--command overwrite`：整篇替换，会丢评论/资源（自建无评论文档安全）
- 写操作后 block ID 会变化
- Windows PowerShell：每 Bash 调用只跑一条外部命令，可用管道 `| Select-String '"result"|"revision_id"'` 过滤

## 验证写入

```bash
lark-cli docs +fetch --doc "<obj_token>" --scope keyword --keyword "<关键词>" --format json
```

- 验证关键词是否渲染（如五层阶梯的 L1/L4/L5 是否都在）
- 验证通过后再清理本地暂存目录

## 交付

用 present_files 交付首页与关键节点链接：
`https://<host>/wiki/<node_token>`

## 清理

本地暂存内容目录（如 `_lark_content/`、`_lark_content2/`）在写入验证后删除，不留垃圾。
