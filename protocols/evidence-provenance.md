# Evidence Provenance（证据溯源协议）

> 每个 Knowledge Object 必须能回答：谁发现、谁支持、谁反对、依据什么证据。
> 没有 provenance 的 claim 不进入 Knowledge Package。

## 溯源链

```
discovered_by（谁发现）→ supported_by（谁支持）→ contested_by（谁反对）→ evidence（依据）
```

## 规则

1. **每个 EV 必须标 `discovered_by`**——多 Agent 分工下，来源必须可追溯
2. **Knowledge Object 必须标 `supported_by` / `contested_by`**——哪些角色支持、哪些角色反对
3. **证据不可删除**——即使后来被推翻，原证据保留并标记 `superseded_by`
4. **source 必须可回看**——文件:行号 / ADR-NNNN / RUN-XXX，禁止"我记得"

## 为什么重要

- 多 Agent 下"谁说的"决定可信度（code-analyst 的实现事实 > doc-analyst 的设计意图，在"实现是什么"这个问题上）
- 冲突时能定位：是证据问题，还是层面问题（交给 Reconciler）
