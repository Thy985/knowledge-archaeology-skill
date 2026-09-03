# Validation Schema（验证契约）— v2

> Validator 的产出格式。每个 Validator 独立工作，只对 Knowledge Package 的特定维度负责。
> v2 强化：①所有 Validator 必须先 Blind Reconstruction（protocols/blind-reconstruction.md）
> ②反例预算制 ③Flow→KO 交叉校验门。

## Validator 产出

```json
{
  "validator": "truth-auditor|coverage-auditor|flow-auditor|abstraction-auditor|counterexample-hunter|epistemic-auditor",
  "target": "KO-007",
  "verdict": "PASS|FAIL|PARTIAL|CONDITIONAL",
  "blind_reconstruction": {
    "performed": true,
    "independent_findings": ["对仓库的独立理解（未参考 KO）"],
    "source_truth": "SUPPORTED|PARTIALLY_SUPPORTED|UNSUPPORTED|CONTRADICTED"
  },
  "findings": [
    {
      "issue": "claim 与 EV-012 冲突",
      "evidence": "EV-012（bypass path 存在）",
      "severity": "blocker|warning|info"
    }
  ],
  "recommendation": "降级到 L3 / 修改 claim 为条件化 / 补证据 / 接受"
}
```

## Validator 职责与禁则（v2）

| Validator | 回答 | v2 强制要求 |
|-----------|------|------------|
| truth-auditor | 这句话是真的吗？ | **先 Blind Reconstruction 再核验**；只引用仓库证据；必须回答 Where/What symbol/implementation or doc |
| coverage-auditor | 还有什么没被发现？ | **从仓库独立重搜**；先建立 high-density 子系统清单，强制每个子系统 ≥1 KO 代表，缺失 → Critical Knowledge Missing |
| flow-auditor | Flow Atlas 对应代码吗？ | 逐条验证 Edge（source/target/symbol/condition/failure path）；判定 VERIFIED/PARTIALLY_VERIFIED/UNVERIFIED/INCORRECT |
| abstraction-auditor | L3/L4/L5 过度升维吗？ | **独立判定晋升**（不读 Synthesizer 自我论证）；每级证明解释范围扩大；不满足则降级 |
| counterexample-hunter | 哪里不是这样？ | **反例预算制**：每个 L3+ KO ≥3 个定向反例攻击；0 反例必须给出搜索证据 |
| epistemic-auditor | 认知状态诚实吗？ | 禁止 Fact→Principle 无中间推导跃迁；核对状态与证据强度匹配 |

## Flow→KO 交叉校验门（v2 新增）

Synthesizer 产出 KO 时，每条 L1 事实必须能回溯到 Flow Atlas 的具体 Edge：

```
KO 的 L1 事实 → 对应 Flow Edge（symbol: 文件:行号）→ 代码中存在该关系？
  ├─ 是 → 通过
  └─ 否/矛盾 → KO 不得通过（flow-auditor 判定 INCORRECT）
```

flow-auditor 发现 KO 与 Flow 矛盾 → blocker → Revise。

## 冲突处理（交给 Reconciler）

多 Validator 冲突不是失败，是产出条件化知识的机会：

```
claim: execution requires authorization
  design_intent: true        （doc-analyst）
  implementation: partial    （code-analyst）
  tested_behavior: true       （test-analyst）
  exception_path: exists      （counterexample-hunter）
status: CONDITIONAL
```

而不是粗暴 PASS/FAIL。

## 质量门（Orchestrator 执行）

- 全部 Validator PASS → Accept
- 任一 blocker → Revise → Re-analysis（反馈控制，不是一次性）
- **任一 Validator 未执行 Blind Reconstruction → 该 Validator 结果无效，必须重做**
- 冲突无法当场化解 → Escalation 到人类或标记 CONDITIONAL
