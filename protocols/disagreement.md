# Disagreement（分歧协议）

> 多个 Agent 产生冲突时，先判断：是事实冲突，还是层面冲突？
> 层面冲突是产出条件化知识的机会，不是失败。

## 三步裁决

### 1. 分类

| 类型 | 例子 | 处理 |
|------|------|------|
| 事实冲突 | code-analyst 说 A，test-analyst 说 B | 查证据，谁是 source 更强 |
| 层面冲突 | design 说应 X，implementation 是 Y | 不选边，分层记录（Reconciler） |
| 证据缺失 | 双方都无法证明 | 标 INCONCLUSIVE，路由到补证据 |

### 2. 分层（Reconciler 使用）

```
Design Intent     ≠   Implementation Reality
                  ≠   Tested Behavior
                  ≠   Runtime Observation
```

### 3. 输出

- 事实冲突 → 依据证据强弱裁决，弱方保留 `contested_by` 记录
- 层面冲突 → 产出 `CONDITIONAL` 状态知识（不粗暴 PASS）
- 证据缺失 → `INCONCLUSIVE`，不写入 Knowledge Package

## 反例

```
❌ 粗暴 PASS（忽略 bypass）
✅ CONDITIONAL：默认路径需授权；高权限路径存在 bypass（design true / impl partial / tested true）
```
