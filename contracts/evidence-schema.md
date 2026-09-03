# Evidence Schema（证据契约）

> 所有 Discovery Agent 的产出必须是 Evidence Pack，不是自然语言报告。
> 所有下游 Agent 只能在 Evidence Graph 上推理，禁止"凭记忆整理"。

## Evidence Pack（单条证据）

```json
{
  "id": "EV-001",
  "stage": "code|doc|test|failure|authority|runtime|policy",
  "discovered_by": "code-analyst",
  "source": "flutter_app/lib/core/parser/markdown_parser.dart:326",
  "claim": "解析器在每行 try-catch 后降级为纯文本（B-5）",
  "data_form": "行级 → 块级状态机",
  "symbols": ["markdown_parser.dart", "parseLines", "inCodeBlock"],
  "strength": "S4",
  "detail": "关键原文引用",
  "timestamp": "2026-09-03"
}
```

**约束**：
- `source` 必须是可追溯路径（文件:行号 / ADR-NNNN / RUN-XXX / commit），禁止无来源断言
- `strength` 遵循 S0-S8（见 references/knowledge-classification.md）
- `claim` 只陈述观察，不做价值判断（"作者为什么这样"是 doc-analyst 的事）

## Evidence Graph（融合产物）

```
源证据（code/doc/test/failure/authority）→ 三角印证 → Supported Fact
```

- 一个 Fact 至少由 2 个独立源支撑才算 Supported（例：代码实现 + 测试断言）
- 单源 = `Unverified Observation`，不进入下游推理
- 冲突的源证据**保留在 Graph 中**（不删除），标记 `contradicts: <EV-id>`，供 Reconciler 使用

## 禁止

- ❌ 无 source 的 claim
- ❌ 把 design intent（doc 层）标成 implementation fact（code 层）
- ❌ 删除冲突证据（冲突是知识资产，交给 Reconciler）
