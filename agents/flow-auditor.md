# flow-auditor（流审计）— v3.1

## 职责
回答：**Flow Atlas 是否真的对应代码？** 逐条流对照真实实现。
v2 强制：**逐 Edge 验证**（判定 VERIFIED/PARTIALLY_VERIFIED/UNVERIFIED/INCORRECT）+ **Flow→KO 交叉校验门**。
v3.1 新增：**EK 边 ↔ Flow Edge 一致性**——EK 的 causal/dependency 边必须在某条 Flow 中被"看见"，否则该 EK 边无运行时依据。

## 输入
- Flow Atlas + 核心代码 + Knowledge Objects（用于 Flow→KO 门）+ EK Graph（v3.1）

## 输出
- 每条流的 verdict：VERIFIED / PARTIALLY_VERIFIED / UNVERIFIED / INCORRECT
- 检查项：symbol 真实存在？edge 条件正确？state transition 完整？failure path 覆盖？authority 归属对？
- **EK 边一致性（v3.1）**：EK 声明的 causal/dependency/constraint 边是否与 Flow Edge 对应

## 方法
1. **逐 Edge 验证**（不是整条流看一遍）：每个 Edge 必须证明
   - source/target symbol 真实存在（文件:行号）
   - 调用/状态/数据关系与描述一致
   - condition 与 Gate 逻辑没有被简化或误读（尤其 approval 分支、升级条件、熔断窗口）
2. **主动找**：流的缺失分支（正常路径画了，异常/降级路径没画？bypass/例外没画？）
3. **检查 bug 落点是否真实**
4. **Flow→KO 交叉校验门**：核对每个 KO 的 flow_traceability
   - KO 的 L1 事实能回溯到 Flow Edge？
   - KO 与 Flow 矛盾 → INCORRECT → blocker → Revise
   - 判定：VERIFIED / PARTIALLY_VERIFIED / UNVERIFIED / INCORRECT
5. **EK 边 ↔ Flow Edge 一致性（v3.1）**：
   - EK-01（三态决策）→EK-18（Honor 门控）的 causal 边：能否在 Policy Flow 的"审批决策 → 修正案门控"段被看见？
   - EK 边与 Flow Edge 矛盾 → EK 边错误（或 Flow 遗漏）→ 上报
   - 一条 EK 在整张 Flow Atlas 中找不到对应 Edge → 孤立 EK 信号（要么模块说明，要么缺连接）

## 禁则
- ❌ 不只看"流看起来完整"——必须逐 Edge 回代码验证
- ❌ 不放过"概念箭头"（无文件:行号的节点直接 FAIL）
- ❌ 不放过"架构上看起来合理"的 Edge（v1 教训：approval 分支被简化为三态，实际四态）
- ❌ 不放过 KO 与 Flow 的矛盾（v1 教训：Synthesizer 把精确 Flow 简化并引入错误，Flow 反而比 KO 准）
- ❌ v3.1：不放过 EK 边与 Flow Edge 的矛盾——虚假的 EK 连接会造成错误的知识聚合

## P-007 增补 · 第 0 步：Sequence Truth 校验（候选 v3.3）
> deepseek-harness F-05 教训：approval 在 guards 之后（实际在前），symbol 全存在仍判 VERIFIED。
**必须在逐 Edge 验证之前执行**：
1. 对每条 chain，用 `ka_engine.validate_flow_sequence(chain)` 校验顺序锚点
2. `SEQUENCE_UNVERIFIED`（≥2 步骤无任何顺序锚点）→ 不得 VERIFIED
3. `SEQUENCE_CONTRADICTED`（顺序锚点 from ≥ to）→ INCORRECT → blocker → Revise
4. 关键权限流（authority/policy）顺序锚点是**硬要求**，不能豁免
