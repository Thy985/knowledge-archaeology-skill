"""策略固化：把一次性审批变成持久规则。

决策 → 审批 → 策略固化 → 未来免审（Policy Flow 闭环）。
line 30: 批准后 append allow 前缀规则并持久化，同类命令下次直接 Skip。
line 38: 幂等检查——同一规则不重复写入。
"""
import threading


class ExecPolicy:
    BANNED_PREFIXES = {"rm", "mkfs", "dd"}  # 危险前缀，永不放行

    def __init__(self):
        self._allow_prefixes = set()
        self._lock = threading.Lock()  # 串行化策略更新

    def check(self, cmd: str) -> str:
        if any(cmd.startswith(b) for b in self.BANNED_PREFIXES):
            return "ban"
        if any(cmd.startswith(a) for a in self._allow_prefixes):
            return "allow"
        return "unknown"

    def adopt_amendment(self, amendment: str) -> bool:
        # amendment 形如 "allow:xxx"，仅来自审批通过
        prefix = amendment.split(":", 1)[1]
        with self._lock:
            if prefix in self._allow_prefixes:
                return False  # line 38: 幂等，已存在
            self._allow_prefixes.add(prefix)
            return True  # line 30: 固化成功 → 未来免审
