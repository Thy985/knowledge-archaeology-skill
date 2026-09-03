# Failures —— 已发现的 Skill 缺陷

> 每次考古发现的 Skill 缺陷在此登记，并转化为永久 Regression/Mutation 用例。
> **铁律：过去犯过的错误，以后永久不能再次发生。**

## F-001 · Fact hallucination（事实幻觉）

- **发现**：v1 考古把 approval_policy 识别为三态，实际四态（Never/OnRequest/Granular/UnlessTrusted）
- **根因**：Synthesizer 依据训练记忆推断，未 Source Truth Gate 核对真实枚举
- **修复**：Layer 3 Regression（approval_policy_states.yaml）+ Source Truth Gate
- **状态**：✅ 已封锁

## F-002 · Over-abstraction（过度升维）

- **发现**：v1 把单实例"递归模型"包装成高阶 Pattern；实际只是"环境隐式契约"
- **根因**：Synthesis 阶段缺乏独立晋升判定；Validator 读取同一份证据无法独立制衡
- **修复**：Abstraction Promotion Gate（L1→L5 逐级独立判定）+ Observed Structure ≠ Pattern 规则
- **状态**：✅ 已封锁

## F-003 · Discovery omission（覆盖遗漏）

- **发现**：v1 遗漏 3 大机制（exec_policy 策略系统 / 模型可见上下文治理 / 审批→策略固化闭环）
- **根因**：Discovery 对"显式结构"敏感，对"系统通过什么机制持续约束自己"（Policy/Governance）不敏感
- **修复**：policy-governance-analyst + Policy Flow（第七类流）+ Coverage Auditor 独立重搜
- **状态**：✅ 已封锁

## F-004 · Same-source validation（同源验证失效）

- **发现**：v1 False Acceptance ≈43%——Validator 读取 Archaeologist 产生的同一份证据，变成"请证明这个答案没问题"
- **根因**：Validator 未做 Blind Reconstruction
- **修复**：所有 Validator 必须先 Blind Reconstruction 再审
- **状态**：✅ 已封锁

## F-005 · Weak contradiction discovery（反例发现薄弱）

- **发现**：v1 声称 7/7 PASS、0 反例、0 冲突；独立审计 Counterexample Detection 仅 30/100
- **根因**：没有主动"杀死"知识的角色
- **修复**：counterexample-hunter 反例预算制（≥3 定向攻击/高价值 KO）
- **状态**：✅ 已封锁

## F-006 · 知识库过度压缩（只有升维后的 KO）

- **发现**：曾倾向只保留抽象后的 KO，丢弃底层工程事实
- **根因**：误解"抽象 = 高级"；把 L1/L2 当"未升维的 KO"
- **修复**：三层架构（Project / Engineering / Generalized）+ "宽底座 + 窄尖顶"配比 + 铁律"不够抽象绝不等于不重要"
- **状态**：✅ 已封锁

> E2E 验证记录：本行用于验证 Progressive Autonomy 低风险自动合并闭环（2026-09-03）。

---
## F-007 · Discovery omission — authority/policy 子组件（deepseek-harness 考古，ARCH-2026-09-03-001）

- **发现**：authority-analyst / policy-governance-analyst 遗漏 approval 策略解析链路（config.policy 默认层 / session override / **delegation 委派继承**）、PTC collapse 前置拒绝契约、guard 家族第二成员（repeat-tool-reminder）、settings seam。
- **根因**：Discovery 对"显式接口"（approval.request）敏感，对"策略模型的隐藏契约 / 委派路径 / 同机制家族的第二实例"不敏感；没有强制"机制家族全实例枚举"。
- **修复（候选）**：P0-2 Coverage 同构家族枚举 Gate；authority-analyst 强制枚举 approval 策略解析链路。
- **状态**：🟡 独立验证发现（M-1/M-2/M-5/M-6），候选修复中

## F-008 · Evidence failure — 只记存在性不记顺序（F-05 Authority 顺序错位）

- **发现**：F-05 / EK-07 把 approval 放在 guards **之后**，真实顺序是 `collapse-check → pre-execute → approval(ask) → guards → execute`（`tools/index.ts:1367,1400,1468-1493`）。
- **根因**：Evidence Assembly 只记录了"存在 approval 与 guards 两类节点"，未记录它们的**相对顺序**；flow-miner 据架构印象补了顺序。
- **修复（候选）**：P0-1 Flow Sequence Truth Gate（每条 chain 必须带相邻顺序证据）。
- **状态**：🟡 独立验证发现（IF-01），候选修复中

## F-009 · Coverage failure — 同构机制家族未枚举（反复发生，v1 F-003 同族）

- **发现**：guard 家族只发现 timeout-policy，遗漏 repeat-tool-reminder；Capability Seam 家族只发现 llm/sandbox/credentials/subagent，遗漏 settings；approval 策略层只发现 config 一层，遗漏 override/delegation。
- **根因**：coverage-auditor 的"强制子系统覆盖"以**子系统**为粒度，未强制**机制家族全实例枚举**（找到一个实例就宣布覆盖）。
- **修复（候选）**：P0-2 Coverage 同构家族枚举 Gate。
- **状态**：🟡 独立验证发现（M-1/M-4/M-5），候选修复中

## F-010 · Synthesis failure — 策略/协作模型过度简化

- **发现**：approval 模型被简化为单层，遗漏 `effectivePolicy = overrideOf(session) ?? config.policy ?? 'ask'` 两层解析与 delegation 播种；plan-mode 未识别为 per-agent 协作状态（projection 折叠/恢复）。
- **根因**：synthesizer 基于不完整证据合成；EK 未覆盖到子组件层。
- **修复（候选）**：P1-1 时序盲重建（强制从代码重建模型结构）；P0-2 家族枚举。
- **状态**：🟡 独立验证发现（IF-03/IF-05），候选修复中

## F-011 · Abstraction failure — scope 泛化未被拦截（v1 F-002 同族变体）

- **发现**：KO-03 fail-closed 族 claim 泛化到"全部权限面"，实际仅适用**受限执行路径**（plan-mode 等非受限路径不适用）；abstraction-auditor 判 OK，独立验证 DOWNGRADED 并收紧 scope。
- **根因**：Abstraction Promotion Gate 检查"层级是否过高"（L3/L4/L5）与聚合规则，但**不强制对 L3+ KO 的 scope 边界做反例攻击**（找 does_not_apply 实例）。
- **修复（候选）**：P0-3 Abstraction Scope 反例 Gate。
- **状态**：🟡 独立验证发现（KO-03 DOWNGRADED），候选修复中

## F-012 · Flow failure — Flow chain 顺序错位（flow-auditor 未拦截）

- **发现**：F-05 chain 顺序错位（approval 在 guards 后）且遗漏 collapse 前置门；flow-auditor 判 VERIFIED。flow-schema 的 chain 只有 node/symbol/role，**无顺序锚点强制校验**——symbol 存在、condition 正确但位置颠倒仍判 VERIFIED。
- **根因**：flow-schema 未要求"相邻步骤的真实调用顺序证据"；flow-auditor 逐 Edge 验证存在性，不验证时序。
- **修复（候选）**：P0-1 Flow Sequence Truth Gate。
- **状态**：🟡 独立验证发现（IF-01），候选修复中

## F-013 · Validation failure — 6 Validator 全 PASS 仍漏顺序错误 + 7 项遗漏（v1 F-004 同族变体）

- **发现**：原始 6 类 Validator 全 PASS + Blind Reconstruction 8/8 无推翻，但仍漏 F-05 顺序错误、7 项 MISSING、KO-03 scope 泛化；第二个独立 Auditor（盲重建）才发现。
- **根因**：Blind Reconstruction 的"重建"覆盖**知识存在性**（claim 是否可追溯），不覆盖**时序正确性**（顺序是否真实）与**枚举完整性**（同构家族是否漏项）；truth-auditor 只验证"有证据支持"。
- **修复（候选）**：P1-1 时序盲重建（validator 盲阶段强制重建关键时序与家族枚举）。
- **状态**：🟡 独立验证发现，候选修复中

## F-014 · Orchestration failure — Flow/Authority 无强制交叉核对 + 反例预算未覆盖 scope 泛化

- **发现**：flow-miner 产出 F-05 与 authority-analyst 的权限证据无强制交叉核对；counterexample-hunter 对 KO-03 做了 3 个反例（C-06..C-08）但未覆盖"scope 泛化"类反例（非受限路径）。
- **根因**：Orchestrator 只在 Flow→KO 交叉校验门强制，未强制 Flow↔Authority 证据交叉；反例预算未要求"每个 L3+ 至少一个 scope 边界反例"。
- **修复（候选）**：P0-3 的 scope 反例并入反例预算；P1-1 时序盲重建。
- **状态**：🟡 独立验证发现，候选修复中

> 以上 F-007..F-014 来自 deepseek-harness 考古（ARCH-2026-09-03-001）+ 独立验证（07-independent-validation-report.md）。
> 全部"已封锁"的旧缺陷（F-001..F-006）仍保持绿；本次为**新发现的缺陷族**，尚未封锁，进入候选修复。
