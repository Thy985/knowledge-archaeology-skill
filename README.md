# knowledge-archaeology

**Multi-Agent Knowledge Archaeology System** —— 把一个软件项目（仓库/代码/文档/ADR/测试/Issue/RUN/审计）只读"考古"成可长期复用、可升维、可落飞书知识库的知识资产。

核心命题：**"这个项目让我们认识到了什么"而非"这个项目有什么"**。

## 版本

- **v3.2**（当前）：5 层 CI 质量门系统。Skill 从"文档仓库"升级为"可测试、可基准评估、可回归、可自动进化的软件系统"。CI 不测代码编译，测**知识质量有没有变差**。
- **v3.1**：EK Graph + 聚合规则。52 条 EK 通过 6 类边（mechanism/subsystem/causal/dependency/constraint/contrast）连成图，KO 从图上按 R1-R4 聚合规则生成簇，防止 EK 层退化成"模块说明"。
- v3：三层知识架构（Project Layer / Engineering Knowledge / Generalized Knowledge），"宽底座 + 窄尖顶"。
- v2：Validator 强制 Blind Reconstruction、Abstraction Promotion Gate、反例预算制、Policy Flow 第七类流。
- v1：多 Agent 分工、交叉验证、冲突裁决、质量闭环的初始架构。

## 5 层 CI（Skill 质量门系统）

CI 测试的不是"代码有没有编译过"，而是**"Skill 这个知识生产系统改完之后，知识质量有没有变差"**。

| 层 | 名称 | 验证什么 |
|----|------|---------|
| Layer 1 | Contract Tests | Skill 结构完整性（目录/文件/枚举/铁律） |
| Layer 2 | Deterministic Unit Tests | Epistemic Promotion / 聚合规则确定性逻辑 |
| Layer 2.1 | Ruleset + PR Risk | 规则集合法性 + 自动合并风险自动分级 |
| Layer 3 | Knowledge Regression Tests | Codex Gold Records——过去犯过的错误永久不能再现 |
| Layer 4 | Benchmark Tests | Quality Gates（硬门槛，Promotion Gate） |
| Layer 5 | Mutation / Adversarial Tests | 系统能否识别自己的错误（坏知识检测） |

**权威规则集（`rules/*.json`）**：所有阈值集中于此，CI 与引擎统一加载，禁止代码硬编码。
- `quality-gates.json` — Promotion Gate 硬门槛
- `promotion-rules.json` — Epistemic Promotion 晋升规则
- `ek-graph-rules.json` — EK Graph 质量规则 + 三层配比
- `risk-paths.json` — 自动合并风险分级路径

**Quality Gate**：5 层全 PASS 才允许合并——不是"CI 通过就无条件合并"，而是"通过一组严格 Knowledge Quality Gates 才允许自动合并到生产 Skill"。

**硬门槛（Promotion Gate）**：regression pass / critical_coverage ≥ 0.90 / fidelity ≥ 0.95 / abstraction_validity ≥ 0.90 / false_acceptance ≤ 0.10 / critical_regressions = 0。即使总分 +10%，只要 Critical Coverage -4% → FAIL。

**Progressive Autonomy（`rules/risk-paths.json` 自动分级，不依赖人工 label）**：
- **Low**（tests/benchmarks/evals/evolution/docs）→ Quality Gate PASS → 自动合并
- **Medium**（references/）→ 人工审
- **High**（agents/workflows/contracts 核心/protocols/rules/ka_engine）→ **永不自动合并**，必须 Human Gate

本地跑：`python tools/run_all_tests.py`；PR 风险判定：`python tools/evaluate_pr_risk.py <changed_files...>`

## 目录结构

```
├── SKILL.md                 # 入口：版本、架构、核心机制、角色清单
├── agents/                  # 21 个角色定义（发现/挖掘/合成/验证/治理）
├── contracts/               # 结构化 Artifact schema（evidence/knowledge/flow/ek-graph/validation）
├── protocols/               # 协作协议（盲重建/晋升门/交接/冲突/升级）
├── references/              # 方法论参考（五层阶梯/三层架构/七类流/飞书落地）
├── workflows/               # 主流程（考古/验证/基准测试）
├── rules/                   # ★ 权威规则集（quality-gates / promotion-rules / ek-graph-rules / risk-paths）
├── tests/                   # 5 层 CI 测试
│   ├── contract/            # Layer 1
│   ├── unit/                # Layer 2 + 2.1（规则集/PR 风险）
│   ├── regression/          # Layer 3（Codex Gold Records）
│   ├── benchmark/           # Layer 4（Quality Gates）
│   └── mutation/            # Layer 5（坏知识检测）
├── benchmarks/              # 项目基准（codex/…）：Gold Records + Critical Findings
├── evals/                   # 评分数据（fidelity/coverage/abstraction/flow/epistemic）
├── evolution/               # 进化记录（failures/proposals/promotion）
├── tools/                   # ka_engine.py（规则驱动引擎）+ evaluate_pr_risk.py（风险分级）+ run_all_tests.py
└── .github/workflows/       # skill-quality-gates.yml（5 层 CI + Progressive Autonomy）
```

## 设计原则

1. **发现 ≠ 提炼 ≠ 升维 ≠ 验证** —— 认知冲突由不同角色承担，禁止同源自我确认
2. **Agent 之间只传递结构化 Artifact**，不传递长文本报告
3. **验证 = 重新做一遍再判断**（Blind Reconstruction），不是"证明这个答案没问题"
4. **宽底座 + 窄尖顶** —— 底层工程知识是推理原材料（无损底座），只有少量内容升维成跨项目认知
5. **EK 是图的节点，KO 是图上的簇** —— 工程知识必须通过边连接，KO 必须通过聚合规则生成
6. **知识质量可测试** —— 每次 Skill 变更都必须过 5 层 CI；过去犯过的错误永久变成 Regression/Mutation 用例

## 触发场景

用户要求整理项目知识、做知识库、提炼项目经验/方法论/认知模型、把项目沉淀到飞书知识空间、项目复盘升维、跨项目模式提炼、深度项目理解。

## License

MIT
