---
proposal_id: P-007
title: "Flow Sequence Truth Gate —— 强制 Flow chain 顺序的真实性校验"
priority: P0
risk: High
changed_paths:
  - "contracts/flow-schema.md"
  - "agents/flow-auditor.md"
  - "workflows/validation.md"
  - "tests/mutation/test_mutation.py"
why: "deepseek-harness F-05 Authority 顺序错位（approval 在 guards 后）被 flow-auditor 判 VERIFIED——flow-schema 的 chain 只有 node/symbol/role，无顺序锚点；symbol 存在、condition 正确但位置颠倒仍通过。顺序错误是 Flow 类最隐蔽的 False Acceptance 源，影响所有项目的 Flow Atlas。"
validation:
  - "Layer 5 mutation: 新增顺序颠倒的 flow mutation → 必须 detect=true"
  - "Layer 3 regression: 新增 deepseek-harness F-05 顺序 gold record"
  - "Layer 2 unit: ka_engine 新增 sequence_ok() 确定性判定"
  - "Layer 4 benchmark: 现有 gate 不回退"
status: "pending_human_gate"  # CI 全 PASS；HIGH/Medium 风险 → 治理阻止自动合并，待 Owner 审查
---

## 变更内容
1. **contracts/flow-schema.md**：chain 数组新增 `sequence_anchors` 契约——每条相邻 Edge 必须给出"前序 Edge 调用的证据"（`{from: step_i, to: step_{i+1}, evidence: "file:line"}`）；无法证明相邻顺序的 chain 判定 `SEQUENCE_UNVERIFIED`。
2. **agents/flow-auditor.md**：方法新增"第 0 步 Sequence Truth 校验"——对每条 chain 逐相邻对验证真实调用顺序；顺序颠倒 → `INCORRECT`（blocker）。
3. **workflows/validation.md**：flow-auditor 输出必须包含 sequence verdict。
4. **tests/mutation**：新增 mutation：真实"approval 在 guards 前" → 变异为"approval 在 guards 后" → detect=true。
5. **tests/unit + ka_engine**：新增确定性函数 `sequence_ok(chain)`。

## 自动化 Regression Case
- ✅ 可自动化：`flow_sequence_mutation`（顺序颠倒 detect）+ `deepseek-harness_f05_sequence`（真实 F-05 顺序 gold record，防止再犯）。

## 风险分析
- 影响面：contracts（schema 变更）+ flow-auditor（核心验证角色）+ validation workflow → **High**（永不自动 merge，必须 Human Gate）。
- 回退风险：现有 6 层 CI 必须保持绿；新增字段向后兼容（chain 缺 sequence_anchors 时降级警告而非硬失败，避免存量 Flow 被误杀）。
