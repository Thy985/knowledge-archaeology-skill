"""Agent 主循环：意图分析 → 审批 → 执行。

关键设计：
- Agent 只做"判断"（意图分析），不直接拥有执行权
- 所有会改变状态的命令必须经过 PermissionGate（permission_gate.py）
- 超过 5 次失败必须请求 Human（停止条件，避免无限自旋）
"""
from permission_gate import PermissionGate, Approval


class Agent:
    def __init__(self, gate: PermissionGate):
        self.gate = gate
        self.failures = 0
        self.MAX_FAILURES = 5  # line 18: 停止条件——失败超限升级给人类

    def handle(self, command: str, executor) -> dict:
        intent = self._analyze(command)   # 只产出"意图"，不执行
        approval = self.gate.approve(intent)  # line 28: 执行权在 Gate，不在 Agent
        if approval.state == Approval.FORBIDDEN:
            self.failures += 1
            if self.failures >= self.MAX_FAILURES:
                executor.escalate_to_human(intent)  # line 33: 升级，而非硬闯
            return {"status": "forbidden"}
        return executor.run(intent)  # line 35: 只有 Gate 放行才执行

    def _analyze(self, command: str):
        return {"cmd": command.split()[0], "args": command.split()[1:]}
