# Codex Regression Gold Records

> 本目录是 knowledge-archaeology skill 的**知识回归基准（Gold Records）**。
> 每次 skill 改动后，CI 会用这些真实案例回归验证——过去犯过的错误，以后永久不能再次发生。
>
> 来源：Codex v1 考古 + 独立对抗审计（benchmarks/codex/）
> 版本：v3.1 时点

## 如何生成回归用例

每个 gold record 描述一个"曾经犯过的错误"（或"必须保持的正确认知"），
CI（tests/regression/codex/）据此断言：
- 错误被禁止再现（如 approval_policy 识别为三态 → FAIL）
- 正确认知被保持（如 KO-01 Intelligence≠Authority 必须存在）

## Gold Records 清单

| 文件 | 类型 | 防止的错误 |
|------|------|-----------|
| ko_01_intelligence_authority.yaml | 正确认知 | 防止该高价值 KO 被删除/降级 |
| ko_03_recursive_model_abstraction.yaml | 过度升维 | 防止单实例被包装成高阶 Pattern |
| approval_policy_states.yaml | 事实错误 | 防止 approval_policy 被识别为三态（实际四态） |
| session_lifecycle.yaml | 正确机制 | 防止 Weak<Session> 生命周期降级机制被误读 |
| exec_policy_closure.yaml | 遗漏 | 防止 exec_policy 策略固化闭环被遗漏 |
| missing_policy_flow.yaml | 遗漏 | 防止 Policy Flow（第七类流）缺失 |
| forbidden_no_learning.yaml | 安全不变量 | 防止"Forbidden 不携带修正案"不变量被破坏 |
| counterexample_budget.yaml | 验证纪律 | 防止反例预算制被绕过 |

## 说明

- 每个 record 的 `expected` 字段是 CI 断言的 Gold 值
- `epistemic_status` 必须诚实：Codex 单项目证据 → Principle (Cross-project validation pending)
