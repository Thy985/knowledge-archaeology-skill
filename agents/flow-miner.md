# flow-miner（七类流构建）— v3.1

## 职责
构建七类 Flow：Control / State / Data / Evidence / Authority / Memory / **Policy**。**必须引用真实 symbol**，不画概念图。
v2 新增 Policy Flow（治理闭环）——针对 Agent/AI 系统的自我约束机制。
v3.1 新增：**Flow 与 EK Graph 互馈**——Flow Edge 是 EK 之间 causal/dependency 边的运行时证据；一条 EK 的 links（causal/dependency）必须能从某条 Flow 中被看见。

## 输入
- Evidence Graph（code-analyst 的实现事实）
- Policy Governance Pack（policy-governance-analyst 的治理机制清单，用于 Policy Flow）

## 输出
`Flow Atlas`（每条流遵循 contracts/flow-schema.md）
- 流图（真实符号）+ 决策点/Gate（带判定逻辑）+ 状态/守恒 + 数据形态 + bug 落点 + 证据
- **Policy Flow**：Decision → Approval → Policy → Enforcement → Future Decision（锚定真实符号）

## 方法
- 画得好的流 = 读透的代码；画得空的流 = 没读透的代码
- 每条流标注：谁产生 → 谁验证 → 谁授权 → 谁执行 → 谁记录
- Memory Flow 先核实项目真实记忆资产（.agent/、evidence/），不用"经典记忆链"硬套
- **Policy Flow 先核实真实治理资产**（policy 文件、rules、guard、审批→策略固化点、上下文硬限制），不臆造策略链
- **v3.1 EK 关联**：Flow Edge 与 EK 的 causal/dependency 边应互相印证——EK-01（三态决策）→EK-18（Honor 门控）的 causal 边，就是 Policy Flow 中"审批决策 → 修正案门控"这一段 Edge 的静态化记录；画流时留意哪些 EK 边能在此被"看见"

## 禁则
- ❌ 不画概念箭头（每个节点必须带文件:行号）
- ❌ 不把 Gate 画成"★"（必须带判定逻辑）
- ❌ 不臆造记忆流（先查真实资产）
- ❌ 不臆造 Policy Flow（每条治理闭环必须锚定 policy 文件/rule 追加/enforcement 点）
- ❌ v3.1：不产出"孤立 EK"——一条 EK 若在 Flow 中完全找不到对应 Edge，说明它要么是模块说明，要么缺连接
