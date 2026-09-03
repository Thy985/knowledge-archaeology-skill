# 交付规范（Delivery）— v3.2

> **v3.2 变更核心**：默认交付从"飞书落盘"改为"上传到 `knowledge-archaeology-corpus` 仓库"。
> **飞书不再是默认动作**——必须用户显式授权才执行（默认不做）。
> 本文件是唯一权威的交付规范；`feishu-delivery.md` 仅在用户授权后作为飞书执行细则。

## 一、交付决策表（先判，再执行）

| 用户意图 | 默认动作 | 条件 |
|----------|---------|------|
| 完成考古、沉淀结果（未提飞书） | **push 到 `knowledge-archaeology-corpus` 仓库** | 无条件（默认） |
| 明确要求落飞书知识空间 | push corpus + 飞书落盘 | **必须用户显式授权**（"帮我落飞书" / "建个飞书知识库"等明确指令） |
| 只做本地分析，不要求沉淀 | 仅交付文件路径/汇报 | 默认（如用户只问"这个项目怎么样"） |

**铁律**：
- ❌ 用户未提飞书 → 禁止自动建飞书空间 / 自动写飞书文档
- ❌ 用户未提交付 → 不主动 push（先交付本地结果路径，问是否需要沉淀）
- ✅ 用户提"沉淀 / 保存 / 归档 / 整理结果"（未指定载体）→ 默认 push corpus
- ✅ 用户明确"飞书" → 授权成立，可执行飞书落盘（同时仍建议 push corpus 存档）

## 二、默认交付：knowledge-archaeology-corpus 仓库

**仓库**：`git@github.com:Thy985/knowledge-archaeology-corpus.git`
**结构**：每个已考古项目一个顶级目录 `<project>/`（如 `codex/`、`tafcm/`），仓库只保存**完成考古的结果**，不保存源码。

### 目录约定（每个 `<project>/` 下）

```
<project>/
├── README.md                  # 项目考古索引（一句话定位 + 产物清单 + 考古日期/版本）
├── 00-knowledge-inventory/    # Inventory 产物（knowledge_inventory / candidates / decision_patterns / failure_patterns / evidence_map）
├── 01-project-layer/          # Project Layer（项目地图）
├── 02-engineering-knowledge/  # Engineering Knowledge 层（EK Graph）
├── 03-knowledge-layer/        # Generalized KO 层（aggregation_rule）
├── 04-flow-atlas/             # 七类流
├── 05-candidates/             # 未验证假说
├── 06-validation/             # Validation 报告 + 反例 + Reconciliation + 质量指标
└── benchmarks/                # 供 knowledge-archaeology-skill CI 使用的 Gold Record（可选）
```

> 若考古是按 wave 分文件交付的（如 `wave1-evidence-packs` / `wave2-mining-graphs` / `wave3-knowledge-objects`），可保留 wave 命名，但要确保顶层 7 类产物可被检索。

### 推送流程

1. **本地产物**：考古完成后，结果已在本地某目录（如 `D:\Projects\Active\<project>-archaeology\`）
2. **clone / 复用 corpus 仓库**：`git clone git@github.com:Thy985/knowledge-archaeology-corpus.git`（已存在则 pull）
3. **建项目目录**：把产物整理进 `<project>/`（按上面目录约定）
4. **提交**：`git add <project>/ && git commit -m "feat(<project>): knowledge archaeology <项目名> <版本>"` + `Task scope` 标注
5. **推送**：`git push origin main`（或按仓库当前分支策略）
6. **验证**：`git ls-remote` / 网页确认新目录已入库

> 注意：corpus 仓库是**共享归档**，不要覆盖已有项目目录——新项目新增顶级目录，已有项目新增版本子目录或追加文件。

## 三、飞书落盘（仅授权后执行）

**前置**：用户显式授权（明确指令"落飞书 / 建飞书知识库 / 沉淀到飞书"）。
**执行细则**：读 `references/feishu-delivery.md`（三层结构、建空间/节点、写入、验证、清理）。
**授权后建议**：corpus push + 飞书落盘**两者都做**——corpus 是持久档案，飞书是可检索视图；互不替代。

## 四、交付前自检（对应 Archaeology Workflow 阶段 8）

- [ ] 三层配比健康：100+ Facts → 40~60 EK → 7~12 KO（小项目按比例缩放，不硬凑）
- [ ] EK Graph 合格：平均出边 ≥1、游离 EK <20%、聚合规则覆盖率 100%
- [ ] 无"同子系统=聚合理由"的假聚合
- [ ] 未验证假设标 Hypothesis（进 Candidates，不冒充知识）
- [ ] 无机械复制仓库文档；无"为凑数量制造知识点"
- [ ] 已按用户意图走对交付分支（默认 corpus / 授权飞书 / 仅本地）
