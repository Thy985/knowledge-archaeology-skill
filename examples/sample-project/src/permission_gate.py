"""权限门：三态审批（Skip / NeedsApproval / Forbidden）。

安全不变量（line 22）：
- Skip / NeedsApproval 会携带 proposed_amendment（批准后可固化为策略）
- Forbidden 不携带修正案——"拒绝不可学习"，被拒的命令不能被 Agent 悄悄转为规则
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Approval(Enum):
    SKIP = "skip"                 # 命中已固化 allow 规则 → 免审
    NEEDS_APPROVAL = "needs"      # 危险命令 → 需要人工/策略确认
    FORBIDDEN = "forbidden"       # 命中 ban 前缀 → 直接拒绝


@dataclass
class ApprovalResult:
    state: Approval
    proposed_amendment: Optional[str] = None  # line 22: 仅非 Forbidden 可携带


class PermissionGate:
    def __init__(self, policy):
        self.policy = policy

    def approve(self, intent: dict) -> ApprovalResult:
        verdict = self.policy.check(intent["cmd"])
        if verdict == "allow":
            return ApprovalResult(Approval.SKIP)
        if verdict == "ban":
            return ApprovalResult(Approval.FORBIDDEN)  # 无修正案
        return ApprovalResult(Approval.NEEDS_APPROVAL,
                              proposed_amendment=f"allow:{intent['cmd']}")  # line 36
