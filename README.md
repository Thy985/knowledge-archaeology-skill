# knowledge-archaeology

**Multi-Agent Knowledge Archaeology System** —— 把任何一个软件项目（代码 / 文档 / ADR / 测试 / 失败记录 / 审计）只读"考古"成可复用、可升维、可验证的知识资产。

```
代码/文档/ADR/测试/失败记录
        ↓
   工程事实(L1) → 工程知识(EK) → 模式(L3) → 认知模型(L4) → 方法论(L5)
        ↓
   三层知识库：项目地图 + 工程知识底座 + 可迁移认知
        ↓
   默认交付：push 到 knowledge-archaeology-corpus 仓库（飞书需授权）
```

> **核心命题**：不是"这个项目有什么"，而是 **"这个项目让我们认识到了什么"**。

---

## ✨ 30 秒看懂用途

- **它是什么**：给 AI Agent / 开发者用的"项目知识提炼系统"。像考古学家从地层里还原文明一样，从代码和工程痕迹里还原出**可迁移的工程认知**。
- **核心产出**：三层知识库（`Project Layer` 项目地图 / `Engineering Knowledge` 工程知识底座 / `Generalized Knowledge` 可迁移模式）+ 一份带证据强度的验证报告。
- **关键区别**：
  - ❌ 不是 README 复述 / 目录结构搬运 / "XX 有一个 YYY 模块"
  - ✅ 是"问题 → 实验 → 失败 → 决策 → 证据 → 经验 → 模式 → 原则"的完整提炼链
- **为什么可信**：每个结论都带**证据强度**（S0-S8）与**认知状态**（Fact→Hypothesis→Validated Pattern→Principle），未验证的假设进 Candidates，绝不冒充知识。

---

## 🚀 一键安装（30 秒）

```bash
# 方式一：从 GitHub 安装
git clone git@github.com:Thy985/knowledge-archaeology-skill.git
cd knowledge-archaeology-skill
python scripts/install.py            # 自动探测 skill root 并安装

# 指定位置 / 连 CI 一起装（开发）
python scripts/install.py --target "<你的 skill 根目录>"
python scripts/install.py --with-ci --self-test   # 装 CI + 跑自检
```

Windows PowerShell：`.\scripts\install.ps1`　｜　Linux/macOS：`./scripts/install.sh`

安装后即成为可用的 Skill：在支持 Skill 的 Agent 环境中，对它说 **"整理这个项目的知识 / 对 XX 仓库做一次知识考古"** 即可触发完整管线。

---

## ⚡ 5 分钟跑出第一个结果

```bash
cd knowledge-archaeology-skill
python tools/demo.py          # 在 examples/sample-project 上跑考古骨架
```

demo 用内置的微型 Agent-runtime 示例项目，5 分钟内走完**"仓库 → 事实 → EK → KO → 质量门"**的可执行骨架：

```
STEP 1 · 仓库地图（Project Layer）
STEP 2 · 事实层（L1，6 条 —— 全部锚定 文件:行号）
STEP 3 · 工程知识层（EK Graph，6 条 —— 每条带 links 边）
        EK Graph 质量门: ✅ PASS（平均出边 2.33 / 游离 0% / 聚合 100%）
STEP 4 · 认知层（KO-01 Intelligence≠Authority [L4|A] / KO-02 拒绝不可学习 [L3|B]）
STEP 5 · 晋升判定（无人工确认的 L4 被拦截，补 S7 后放行 —— 门在正常工作）
RESULT · Facts 6 + EK 6 + KO 2（1 A 级）+ Candidates 1
```

> 完整 Multi-Agent 考古（Discovery→Mining→Synthesis→Validation，20+ 角色）在 Agent 环境触发。

---

## 📊 真实 Benchmark（Codex 案例）

> 数据来源：`evals/`（评分）+ `benchmarks/codex/`（Gold Records）+ `evolution/`（进化记录）。
> 评估对象：对 OpenAI Codex 仓库的三轮考古（v1/v2/v3）。

### 当前评分（v3.1，2026-09-03 评估）

| 维度 | 评分 | 含义 |
|------|------|------|
| **Fidelity** | **0.96** | 声明与仓库证据的一致性 |
| **Critical Coverage** | **0.94** | 高密度子系统覆盖（exec_policy/Guardian/网络审批/上下文治理…） |
| **Flow Integrity** | **0.92** | 七类 Flow 与代码真实符号一致 |
| **Epistemic Accuracy** | **0.93** | 认知状态标注诚实（无 L5，不冒充定律） |
| **Abstraction Validity** | **0.91** | 升维合理性（v2/v3 均无 L5，Abstraction Promotion Gate 生效） |
| **Overall** | **≈93.2** | 五项平均，PROMOTION PASS |

### 进化史（为什么这个 Skill 可信）

| 版本 | 结果 | 关键改进 |
|------|------|---------|
| **v1** | ⚠️ **FAILED QUALITY GATE**：False Acceptance ≈43%、3 个 Critical Missing、1 个 Fact Error（approval_policy 误判三态）、1 个过度升维（KO-03） | 暴露"过度综合 / 过度升维 / 同源自我确认"三大缺陷 |
| **v2** | 7 KO（2 L4 + 4 L3 + 1 L2），补全 v1 全部 6 项遗漏 | Blind Reconstruction / Abstraction Promotion Gate / 反例预算制 / Policy Flow |
| **v3** | 52 EK + 8 KO + 6 Candidates，三层配比 100+:52:8 | 三层知识架构（宽底座+窄尖顶） |
| **v3.1** | 评分 0.91~0.96，Overall 93.2 | EK Graph（6 类边）+ 聚合规则（R1-R4）防退化 |

### Gold Records（过去犯过的错误，永久不能再现）

`benchmarks/codex/` 存有 8 个真实回归锚点，每次 Skill 改动 CI 都会断言：

| Gold Record | 防止的错误 |
|-------------|-----------|
| `ko_01_intelligence_authority.yaml` | 高价值认知 KO-01 被删除/降级 |
| `ko_03_recursive_model_abstraction.yaml` | 单实例被包装成高阶 Pattern（过度升维） |
| `approval_policy_states.yaml` | approval_policy 被识别为三态（实际四态） |
| `session_lifecycle.yaml` | Weak\<Session\> 生命周期降级机制被误读 |
| `exec_policy_closure.yaml` | exec_policy 策略固化闭环被遗漏 |
| `missing_policy_flow.yaml` | Policy Flow（第七类流）缺失 |
| `forbidden_no_learning.yaml` | "Forbidden 不携带修正案"安全不变量被破坏 |
| `counterexample_budget.yaml` | 反例预算制被绕过 |

### 硬门槛（Promotion Gate，不可放松）

```
regression: pass        critical_coverage ≥ 0.90    fidelity ≥ 0.95
abstraction_validity ≥ 0.90    false_acceptance ≤ 0.10    critical_regressions = 0
```

> 即使总分 +10%，只要 Critical Coverage -4% → FAIL。防止"用漂亮但错误的知识换分数"。

---

## 🏗 5 层 CI（Skill 质量门系统）

CI 测试的不是"代码有没有编译过"，而是 **"这个知识生产系统改完之后，知识质量有没有变差"**。

| 层 | 名称 | 验证什么 |
|----|------|---------|
| Layer 1 | Contract Tests | Skill 结构完整性（目录/文件/枚举/铁律） |
| Layer 2 | Deterministic Unit Tests | Epistemic Promotion / 聚合规则确定性逻辑 |
| Layer 2.1 | Ruleset + PR Risk | 规则集合法性 + 自动合并风险自动分级 |
| Layer 3 | Knowledge Regression Tests | Codex Gold Records——过去错误永久封锁 |
| Layer 4 | Benchmark Tests | Quality Gates（硬门槛，Promotion Gate） |
| Layer 5 | Mutation / Adversarial Tests | 系统能否识别自己的错误（坏知识检测） |

**权威规则集（`rules/*.json`）**：所有阈值集中于此，CI 与引擎统一加载，禁止代码硬编码。

**Progressive Autonomy（`rules/risk-paths.json` 自动分级）**：
- **Low**（tests/benchmarks/evals/evolution/docs）→ Quality Gate PASS → 自动合并
- **Medium**（references/）→ 人工审
- **High**（agents/workflows/contracts 核心/protocols/rules/ka_engine）→ **永不自动合并**，必须 Human Gate

本地跑：`python tools/run_all_tests.py`；PR 风险判定：`python tools/evaluate_pr_risk.py <changed_files...>`

---

## 目录结构

```
├── SKILL.md                 # 入口：版本、架构、核心机制、角色清单
├── agents/                  # 21 个角色定义（发现/挖掘/合成/验证/治理）
├── contracts/               # 结构化 Artifact schema（evidence/knowledge/flow/ek-graph/validation）
├── protocols/               # 协作协议（盲重建/晋升门/交接/冲突/升级）
├── references/              # 方法论参考（五层阶梯/三层架构/七类流/交付规范）
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
├── examples/sample-project/ # ★ 5 分钟快速上手示例项目
├── evolution/               # 进化记录（failures/proposals/promotion）
├── scripts/                 # ★ 一键安装（install.py / install.ps1 / install.sh）
├── tools/                   # ka_engine.py（规则引擎）+ demo.py（快速演示）+ evaluate_pr_risk.py + run_all_tests.py
└── .github/workflows/       # skill-quality-gates.yml（5 层 CI + Progressive Autonomy）
```

## 设计原则

1. **发现 ≠ 提炼 ≠ 升维 ≠ 验证** —— 认知冲突由不同角色承担，禁止同源自我确认
2. **Agent 之间只传递结构化 Artifact**，不传递长文本报告
3. **验证 = 重新做一遍再判断**（Blind Reconstruction），不是"证明这个答案没问题"
4. **宽底座 + 窄尖顶** —— 底层工程知识是推理原材料（无损底座），只有少量内容升维成跨项目认知
5. **EK 是图的节点，KO 是图上的簇** —— 工程知识必须通过边连接，KO 必须通过聚合规则生成
6. **知识质量可测试** —— 每次 Skill 变更都必须过 5 层 CI；过去犯过的错误永久变成 Regression/Mutation 用例
7. **默认交付 = corpus 仓库，飞书需授权** —— 考古结果默认 push 到 `knowledge-archaeology-corpus`，飞书落盘仅用户显式授权时执行

## 触发场景

整理项目知识、做知识库、提炼项目经验/方法论/认知模型、把项目沉淀到知识仓库、项目复盘升维、跨项目模式提炼、深度项目理解。

## License

MIT
