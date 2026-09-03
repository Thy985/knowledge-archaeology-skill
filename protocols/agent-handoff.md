# Agent Handoff（交接协议）

> Agent 之间只传递结构化 Artifact，不传递自然语言长报告。否则多 Agent 退化为"token 接力"。

## 交接物（结构化）

| 阶段 → 阶段 | 交接物 | schema |
|------------|--------|--------|
| Discovery → Fusion | Evidence Packs（多个） | contracts/evidence-schema.md |
| Fusion → Mining | Evidence Graph | contracts/evidence-schema.md |
| Mining → Synthesis | Problem/Decision/Pattern/Flow Graph | contracts/flow-schema.md |
| Synthesis → Validation | Knowledge Package | contracts/knowledge-schema.md |
| Validation → Reconciler | 冲突的 verdicts + 证据 | contracts/validation-schema.md |
| Reconciler → Final | 条件化知识包 | contracts/knowledge-schema.md |

## 交接规则

1. **下游只读上游的 Artifact**，不重新翻仓库（除非是 coverage-auditor 的独立重搜）
2. **Artifact 必须完整**——缺证据的 claim 不允许进入下游
3. **冲突的 Artifact 原样保留**——不私下解决，交给 Reconciler
4. **每个 Artifact 带 provenance**——下游要知道它从哪来

## 禁止

- ❌ Agent A 写长文 → Agent B 总结 → Agent C 再总结（这是退化）
- ❌ 下游 Agent 凭"自己的理解"重写上游内容
