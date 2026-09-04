"""测试：权限门 + 守护进程的安全不变量。

line 15: 验证"绕过权限门直接执行"会被 Guardian 拒绝——这是系统真正重视的行为。
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from permission_gate import PermissionGate, Approval
from exec_policy import ExecPolicy
from guardian import Guardian


def test_forbidden_carries_no_amendment():
    policy = ExecPolicy()
    gate = PermissionGate(policy)
    result = gate.approve({"cmd": "rm -rf /"})
    assert result.state == Approval.FORBIDDEN
    assert result.proposed_amendment is None  # line 15: 拒绝不可学习


def test_approved_command_future_skip():
    policy = ExecPolicy()
    gate = PermissionGate(policy)
    first = gate.approve({"cmd": "cat secret"})
    assert first.state == Approval.NEEDS_APPROVAL
    policy.adopt_amendment(first.proposed_amendment)
    second = gate.approve({"cmd": "cat secret"})
    assert second.state == Approval.SKIP  # 策略固化 → 未来免审


def test_guardian_fail_closed_on_parse_error():
    guardian = Guardian()

    def broken():
        raise ValueError("bad input")

    result = guardian.guard(broken)
    assert result["status"] == "denied"  # fail-closed


if __name__ == "__main__":
    test_forbidden_carries_no_amendment()
    test_approved_command_future_skip()
    test_guardian_fail_closed_on_parse_error()
    print("sample-project: 3 tests passed")
