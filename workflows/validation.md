# Validation Workflow（质量验证流程）— v3.1

> 对 Knowledge Package 做系统性质量验证。6 类 Validator 分工，Reconciler 处理冲突。
> v2 核心变更：**所有 Validator 必须先 Blind Reconstruction（独立盲重建），再对比判断。**
> 背景：v1 的 Validator 与 Miner 共享同一推理链（同源自我确认），False Acceptance ≈43%。
> v3.1 新增：**EK Graph 验证（每条 EK 的 links 是否真实）+ 聚合规则验证（每个 KO 的 aggregation_rule 是否成立、derivation.facts 是否正好等于簇内 EK）。**

## 触发

- 考古主流程（archaeology.md）阶段 5-7
- 或用户对已有知识库要求质量审查

## 验证矩阵（v3.1）

| Validator | 维度 | 关键问题 | 强制要求 |
|-----------|------|---------|------------|
| truth-auditor | 事实 | 这句话是真的吗？ | **先独立盲重建再核验**；只引用仓库证据 |
| coverage-auditor | 覆盖 | 还有什么重要东西没被发现？ | 独立重搜 + 强制子系统覆盖（high-density 清单） |
| flow-auditor | 流 | Flow Atlas 对应代码吗？ | 逐 Edge 验证（VERIFIED/PARTIAL/UNVERIFIED/INCORRECT） |
| abstraction-auditor | 升维 | L3/L4/L5 过度升维吗？**KO 聚合规则成立吗？** | **独立判定晋升 + 校验 aggregation_rule（R1-R4 + 簇边界）** |
| counterexample-hunter | 反例 | 哪里不是这样？ | **反例预算制**（≥3 攻击/高价值 KO） |
| epistemic-auditor | 状态 | 认知状态诚实吗？ | 禁止 Fact→Principle 无中间推导跃迁 |
| **EK Graph 检查（v3.1）** | **EK 边** | **每条 EK 的 links 真实吗？KO 的簇边界正确吗？** | **孤立 EK 检测 + 聚合规则成立性 + derivation.facts = 簇内 EK** |

## 逐项验证流程

**第 0 步 · Blind Reconstruction（所有 Validator 统一前置）**

每个 Validator 进入正式核验前，先独立从仓库重建相关事实（protocols/blind-reconstruction.md）：
1. 用隔离 SubAgent 或先写下"我对仓库的独立理解"（不参考任何 KO/验证报告）
2. 产出 Independent Findings
3. 再进入与已有 KO 的对比

> 未执行 Blind Reconstruction 的 Validator 结果无效。

**第 1-6 步 · 六维验证**

对每个 Knowledge Object：
1. **truth**：对照独立重建的事实 + Evidence Graph 核验 claim（判定 SUPPORTED/PARTIAL/UNSUPPORTED/CONTRADICTED）
2. **coverage**：从仓库独立确认无盲区；核对 high-density 子系统覆盖矩阵
3. **flow**：逐条验证 Flow Edge（source/target/symbol/condition/failure path/authority）
4. **abstraction**：独立检查每级升维是否满足 promotion 三条件（见 protocols/promotion.md）
5. **counterexample**：对 L3+ claim 执行反例预算（≥3 定向攻击，记录 searched_paths）
6. **epistemic**：核对状态与证据强度匹配

**第 7 步 · Flow→KO 交叉校验门**

- 每条 L1 事实回溯 Flow Edge（flow_traceability）
- KO 与 Flow 矛盾 → blocker → Revise

**第 8 步 · EK Graph 验证（v3.1）**

对每条 Engineering Knowledge：
- **孤立检测**：EK 是否声明了 ≥1 条 links？孤立 EK = 模块说明（需重写）或 D 级项目局部知识
- **边真实性**：links 指向的 EK 是否存在？边类型（mechanism/subsystem/causal/dependency/constraint/contrast）是否与代码/文档一致？

对每个 Generalized KO：
- **聚合规则成立性**：aggregation_rule 声明了 R1-R4 中哪条？簇内 EK 是否真的通过对应边连通？
- **簇边界正确性**：derivation.facts 是否**正好等于**聚合规则声明的簇内 EK？（多一个=夹带，少一个=漏支撑）
- **无分类式理由**：聚合是否基于机制共享/因果链/不变量/互补主题？"都属于某子系统"= 不合格

## 冲突处理

- 多 Validator 冲突 → reconciler（protocols/disagreement.md）
- 反例触发降级 → escalation（protocols/escalation.md）
- 冲突不可解 → CONDITIONAL 或请求人类

## 质量门（v3.1）

```
PASS 全部 → Accept
blocker 任一 → Revise → Re-analysis（反馈控制）
任一 Validator 未 Blind Reconstruction → 该结果无效，重做
EK 孤立比例 >20% → Engineering 层不合格，Revise
KO 无 aggregation_rule → Generalized 层不合格，Revise
```

## 报告

- 每个 KO 的验证结果（verdict + findings + recommendation + blind_reconstruction 记录）
- 总体质量统计（PASS / PARTIAL / FAIL / CONDITIONAL 分布）
- 剩余风险（未验证项、跨项目 pending 项）
- v2 指标（供 benchmark）：False Acceptance Rate / Critical Missing / Fact Error / Over-generalization
- v3.1 指标（供 benchmark）：EK 平均出边数 / 游离 EK 比例 / 聚合规则覆盖率 / KO 平均簇规模
