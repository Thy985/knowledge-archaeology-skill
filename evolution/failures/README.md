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
