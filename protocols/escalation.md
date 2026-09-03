# Escalation（升级协议）

> 当某个环节信息不足、冲突无法化解、或发现需要新角色时，由 Orchestrator 决定升级。

## 触发条件

1. **信息不足**：某条流/某个维度证据不够 → 启动对应 Analyst 补证据
   ```
   发现 security boundary 信息不足
     → Orchestrator
     → 启动 Security Analyst
   ```
2. **反例触发降级**：Counterexample Hunter 发现原 L5 Principle 不成立
   ```
   Counterexample Hunter 发现 2 个 execution bypass
     → 要求 Synthesizer 降级
     → L5 → L4（或加条件化）
   ```
3. **冲突无法化解**：事实冲突且证据相当 → 标 CONDITIONAL 或升级到人类
4. **盲区发现**：Coverage Auditor 报新盲区 → 启动新 Investigation Task

## 升级路径

```
Orchestrator ←→ 角色
    │
    ├─ 补证据（启动/复用一个 Analyst）
    ├─ 降级/条件化（Synthesizer 修正）
    ├─ 新 Investigation Task（coverage 触发）
    └─ 人类裁决（冲突不可解 / 架构级分歧）
```

## 规则

- Orchestrator 只做调度决策，不亲自分析
- 每次升级必须记录原因（为什么升、结果是什么）
- 升级循环有上限（避免无限重跑）——达到上限标 INCONCLUSIVE 或请求人类
