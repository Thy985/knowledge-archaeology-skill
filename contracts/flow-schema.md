# Flow Schema（七类流契约）— v2

> flow-miner 的产出。每条流必须锚定真实符号，禁止概念箭头。
> 原则必须从流的重复结构中被"看见"，不是被"发明"。
> v2 新增：**Policy Flow（第七类流）**——针对 Agent/AI 系统的治理闭环。

## Flow 结构（每类流统一）

```json
{
  "flow_type": "control|state|data|evidence|authority|memory|policy",
  "question": "这条流回答什么？",
  "chain": [
    {"node": "EditorCommand", "symbol": "editor_shell.dart:120", "role": "产生"},
    {"node": "Handler._dispatch", "symbol": "command_handler.dart:80", "role": "守卫"},
    {"node": "TransactionBuilder", "symbol": "transaction_builder.dart:45", "role": "执行"},
    {"node": "History.push", "symbol": "editor_history.dart:90", "role": "记录"}
  ],
  "gates": [
    {"name": "契约 Gate", "logic": "无 Capability Contract 则验证无从谈起", "symbol": "contract.py"}
  ],
  "states": ["Committed", "Live", "Validating"],
  "conservation_points": ["round-trip 不动点：parse→serialize 恒等"],
  "data_forms": ["String → List<DocumentElement>"],
  "bugs": ["P0 ErrorSnapshotter 默认 null 静默失效"],
  "evidence": ["EV-001", "ADR-0008"]
}
```

## 七类流定义速查

| 流 | 回答 | 关注 |
|----|------|------|
| Control | 谁决定下一步？ | 决策点/分支/Gate/升级/回滚 |
| State | 状态如何变化？ | 状态容器/生命周期/可逆性/状态机 |
| Data | 数据从哪到哪？ | 转换边界/数据形态/守恒点/单一真相源 |
| Evidence | 声明如何变可证明？ | 证据生产链/Gate/分级/时效 |
| Authority | 每一步谁有执行权？ | 权限归属/执行边界/审计/bypass |
| Memory | 记忆如何沉淀？ | 分层上下文/状态指针/证据落盘 |
| **Policy** | **系统如何改变自己"下一步"的规则？** | **决策→审批→策略固化→执行→未来决策（治理闭环）** |

## Policy Flow 详解（v2 新增）

**为什么需要**：Control Flow 回答"下一步做什么"；Policy Flow 回答"系统如何改变自己对'下一步'的规则"。它是 **Feedback Loop（系统自我修正）** 的载体，与普通单向执行流本质不同——这是 v1 对"治理/自我约束机制"不敏感的根因。

**标准链**：

```
Decision → Approval → Policy → Enforcement → Future Decision
```

| 阶段 | 含义 | 代码实例（Codex） |
|------|------|------------------|
| Decision | 产生一次判断 | 用户/Guardian 批准一条命令 |
| Approval | 判断生效为授权 | ExecApprovalRequirement → allow |
| Policy | 授权固化为持久规则 | proposed_execpolicy_amendment → blocking_append_allow_prefix_rule 落盘 |
| Enforcement | 规则约束后续行为 | ExecPolicyManager 对后续命令匹配 rules |
| Future Decision | 规则改变未来判断 | 同类命令免审 / 危险命令拒绝 |

**必须锚定真实符号**：policy 文件路径、rule 追加函数、enforcement 匹配点、future 决策消费点。

**调查清单**（policy-miner 视角）：
- 系统把一次性决策固化为持久策略的地方（审批→规则落盘）
- 系统治理自身上下文/资源/执行的规则（上下文硬限制、并发限制、预算）
- 规则文档/guard/policy 文件如何约束 Agent 行为
- 策略变更的审计与回滚（策略本身如何被治理）

## 重复结构归纳（pattern-miner 的输入）

- flow-miner 只负责把流画准，不负责归纳原则
- 归纳由 pattern-miner 做：把多条流骨架并排，标记重复结构
- 例：`产生→验证→授权→执行→记录` 在多条流反复出现 → 报告为 `Observed repeated structure`
- 例：`Decision→Approval→Policy→Enforcement→Future` 在 exec_policy/权限升级/上下文治理中重复 → 报告为 Policy Flow 重复结构
- **不得**自行宣布"这是普遍原则"——那是 Synthesizer + Abstraction Auditor 的职责

## P-007 增补 · Sequence Truth（顺序锚点）— 候选 v3.3
> deepseek-harness F-05 教训：approval/guards 位置颠倒，symbol 都存在、condition 都对，flow-auditor 仍判 VERIFIED。
> **chain 的顺序与 chain 的内容同等重要**——顺序错误是 Flow 最隐蔽的 False Acceptance 源。

**新增字段**：
- 每个 chain 步骤可选 `sequence_anchor: {from, to, evidence}`（单数，声明本步骤与相邻步骤的先后关系 + 证据）
- chain 步骤可带 `sequence_anchors: [{from, to, evidence}]`（复数，显式相邻顺序证据）

**强制规则**：
- ≥2 步骤的 chain：**必须**至少一个步骤带 `sequence_anchor` 或 `sequence_anchors`；否则 `SEQUENCE_UNVERIFIED`（flow-auditor 判定，blocker）
- 显式 `sequence_anchor.from` 的索引必须 `< to` 的索引；违反 → `SEQUENCE_CONTRADICTED`（INCORRECT，blocker）

**判定函数**：`ka_engine.validate_flow_sequence(chain)`（Layer 2 单测 + Layer 5 mutation 已覆盖）。
