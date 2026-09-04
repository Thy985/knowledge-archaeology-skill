# sample-agent-runtime（示例项目）

> 这是 `tools/demo.py` 使用的**微型示例项目**——模拟一个"Agent 执行运行时"，用于 5 分钟跑出
> 第一个 Knowledge Archaeology 结果。它刻意浓缩了 Agent 系统最常见的 4 个工程问题：
> 权限分离 / 策略固化 / 失败关闭 / 状态三分离。

## 它是什么

一个极简的命令执行代理：用户发命令 → Agent 分析意图 → 权限门审批 → 沙箱执行 → 记录证据。

```
User Request
   ↓
Agent（分析意图，不拥有执行权）
   ↓
PermissionGate（三态审批：Skip / NeedsApproval / Forbidden）
   ↓
Guardian（fail-closed：超时即拒绝）
   ↓
Executor（在沙箱中执行）
   ↓
EvidenceLog（记录结果，供审计）
```

## 目录

```
src/
├── agent.py               # Agent 主循环：意图分析 → 审批 → 执行（第 40 行有停止条件）
├── permission_gate.py     # 三态审批门（第 22 行：Forbidden 不携带修正案 = "拒绝不可学习"）
├── exec_policy.py         # 策略固化（第 30 行：批准后 append allow 前缀规则，未来免审）
├── guardian.py            # 守护进程（第 18 行：超时→TimedOut；第 25 行：解析错误→Deny）
tests/
└── test_gate.py           # 测试：验证"绕过权限门"路径被 Guardian 拒绝（第 15 行）
docs/decisions/
└── ADR-0001-authority-separation.md   # 决策：判断力与执行权分离（第 9 行：被放弃方案）
```

## 为什么用它做示例

这 4 个问题（Intelligence ≠ Authority / 审批→策略固化 / Fail Closed / 状态三分离）正是
Codex 考古中验证过的高价值模式。demo.py 会在 5 分钟内走完
"仓库 → 事实 → EK → KO → 质量门"的**可执行骨架**，让你看到这个 Skill 的完整产出形态。
