# knowledge-archaeology

**Multi-Agent Knowledge Archaeology System** —— 把一个软件项目（仓库/代码/文档/ADR/测试/Issue/RUN/审计）只读"考古"成可长期复用、可升维、可落飞书知识库的知识资产。

核心命题：**"这个项目让我们认识到了什么"而非"这个项目有什么"**。

## 版本

- **v3.1**（当前）：EK Graph + 聚合规则。52 条 EK 通过 6 类边（mechanism/subsystem/causal/dependency/constraint/contrast）连成图，KO 从图上按 R1-R4 聚合规则生成簇，防止 EK 层退化成"模块说明"。
- v3：三层知识架构（Project Layer / Engineering Knowledge / Generalized Knowledge），"宽底座 + 窄尖顶"。
- v2：Validator 强制 Blind Reconstruction、Abstraction Promotion Gate、反例预算制、Policy Flow 第七类流。
- v1：多 Agent 分工、交叉验证、冲突裁决、质量闭环的初始架构。

## 目录结构

```
├── SKILL.md                 # 入口：版本、架构、核心机制、角色清单
├── agents/                  # 21 个角色定义（发现/挖掘/合成/验证/治理）
├── contracts/               # 结构化 Artifact schema（evidence/knowledge/flow/ek-graph/validation）
├── protocols/               # 协作协议（盲重建/晋升门/交接/冲突/升级）
├── references/              # 方法论参考（五层阶梯/三层架构/七类流/飞书落地）
└── workflows/               # 主流程（考古/验证/基准测试）
```

## 设计原则

1. **发现 ≠ 提炼 ≠ 升维 ≠ 验证** —— 认知冲突由不同角色承担，禁止同源自我确认
2. **Agent 之间只传递结构化 Artifact**，不传递长文本报告
3. **验证 = 重新做一遍再判断**（Blind Reconstruction），不是"证明这个答案没问题"
4. **宽底座 + 窄尖顶** —— 底层工程知识是推理原材料（无损底座），只有少量内容升维成跨项目认知
5. **EK 是图的节点，KO 是图上的簇** —— 工程知识必须通过边连接，KO 必须通过聚合规则生成

## 触发场景

用户要求整理项目知识、做知识库、提炼项目经验/方法论/认知模型、把项目沉淀到飞书知识空间、项目复盘升维、跨项目模式提炼、深度项目理解。

## License

MIT
