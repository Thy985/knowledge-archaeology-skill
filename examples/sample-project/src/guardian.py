"""守护进程：fail-closed（失败即拒绝）。

与"默认放行"相反：任何不确定/超时/解析错误都拒绝执行（line 18 / 25）。
这是 AI 系统安全默认值——宁可多拒绝，不可错放行。
"""
import time


class Guardian:
    TIMEOUT_S = 90  # line 18: 超时 → TimedOut（不继续等）

    def guard(self, run_fn, *args):
        started = time.time()
        try:
            result = run_fn(*args)
            if time.time() - started > self.TIMEOUT_S:
                return {"status": "timed_out"}  # line 18
            return result
        except (ValueError, KeyError) as e:
            return {"status": "denied", "reason": f"parse_error: {e}"}  # line 25
        except Exception:
            return {"status": "denied", "reason": "unexpected_failure"}  # fail-closed
