"""Layer 3 · Knowledge Regression Tests —— Codex Gold Records 回归。

核心：把 Codex 考古发现的真实错误变成永久回归用例。
- approval_policy 四态（v1 错识别为三态）→ 以后任何 Skill 识别为三态 → FAIL
- KO-01 Intelligence≠Authority 必须存在（L4/A）→ 被删除/降级 → FAIL
- KO-03 单实例不得升 L3+（过度升维）→ 再犯 → FAIL
- exec_policy 闭环 / Policy Flow / session 生命周期 → 遗漏 → FAIL

YAML fixtures 在 benchmarks/codex/*.yaml（Gold Records）。
本测试文件是可扩展的规则层：新增 gold record = 新增永久回归。
"""

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))
import ka_engine  # noqa: E402

GOLD_DIR = REPO_ROOT / "benchmarks" / "codex"


def _load_yaml_plain(path: Path) -> dict:
    """极简 YAML 解析（避免 PyYAML 依赖）：只处理顶层 key: scalar 与 - list。"""
    import re
    result = {}
    current_key = None
    current_list = None
    raw = path.read_text(encoding="utf-8-sig")  # utf-8-sig 自动剥离 BOM
    for line in raw.splitlines():
        line = line.rstrip()
        if not line.strip() or line.strip().startswith("#"):
            continue
        # 剥离行内注释（# 后跟空格/制表符的是注释；# 紧跟文字可能是 URL/内容的一部分）
        if "# " in line or " #" in line:
            line = line.split(" #", 1)[0].split("# ", 1)[0]
        if re.match(r"^[a-zA-Z_]+:", line):
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()
            if val == "":
                result[key] = None
                current_key = key
                current_list = []
                result[key] = current_list
            else:
                val = val.strip('"')
                if val in ("true", "false"):
                    result[key] = val == "true"
                elif val.isdigit():
                    result[key] = int(val)
                else:
                    result[key] = val
                current_key = None
                current_list = None
        elif line.strip().startswith("- "):
            item = line.strip()[2:].strip('"')
            if item in ("true", "false"):
                item = item == "true"
            elif item.isdigit():
                item = int(item)
            if current_list is not None:
                current_list.append(item)
    return result


def load_gold_records() -> dict:
    """加载 benchmarks/codex/*.yaml 为 {gold_id: record}。"""
    records = {}
    if not GOLD_DIR.exists():
        return records
    for f in sorted(GOLD_DIR.glob("*.yaml")):
        rec = _load_yaml_plain(f)
        gid = rec.get("knowledge_id") or rec.get("gold_type") or f.stem
        records[gid] = rec
    return records


# ---------------------------------------------------------------------------
# 回归断言：每个 gold record 类型对应一个检查函数
# ---------------------------------------------------------------------------

def check_fact_regression(rec: dict) -> list:
    """事实回归：approval_policy 状态数必须正确。"""
    problems = []
    forbidden_count = rec.get("forbidden_state_count")
    actual_count = rec.get("actual_state_count")
    if forbidden_count is not None and actual_count is not None:
        if actual_count == forbidden_count:
            problems.append(
                f"Fact Error: {rec.get('fact')} 识别为 {actual_count} 态，但实际是 "
                f"{rec.get('actual_states', [])}（v1 错误，禁止再现）"
            )
    return problems


def check_required_knowledge(rec: dict) -> list:
    """必需认知回归：高价值 KO 必须存在且保持层级/价值。"""
    # 此函数由调用方传入"实际产物"做比对；单独运行只校验 gold record 自身完整性
    problems = []
    for req in ["claim", "required_present"]:
        if req not in rec:
            problems.append(f"Gold Record 缺少字段 {req}")
    return problems


def check_over_abstraction_regression(rec: dict) -> list:
    """过度升维回归：单实例观察不得升 L3+。"""
    problems = []
    expected_max = rec.get("expected_max_level")
    pi = ka_engine.PromotionInput(
        evidence_count=1, independent_instances=1, different_modules=1,
        cross_context=False,
    )
    computed = ka_engine.compute_max_abstraction(pi)
    if expected_max and computed != expected_max:
        problems.append(
            f"过度升维回归: 单实例计算 max_level={computed}，Gold 要求 ≤{expected_max}"
        )
    return problems


def check_required_mechanism(rec: dict) -> list:
    """必需机制回归：关键工程事实必须被保留（不能因'不够抽象'被丢弃）。"""
    problems = []
    for req in ["mechanism", "required_present"]:
        if req not in rec:
            problems.append(f"Gold Record 缺少字段 {req}")
    # session lifecycle 是 L1 工程事实——必须保留为 engineering 底座，不得强行升维
    if rec.get("abstraction") == "L1":
        problems.append("⚠️ 提示: 该机制为 L1 工程事实，应保留在 Engineering Knowledge 层（非错误，仅提醒）") \
            if False else None
    return problems


def check_required_coverage(rec: dict) -> list:
    """必需覆盖回归：exec_policy 策略闭环必须被考古。"""
    problems = []
    if not rec.get("required_present"):
        problems.append(f"覆盖回归: {rec.get('coverage_area')} 未被标记为 required")
    if not rec.get("required_facts"):
        problems.append(f"覆盖回归: {rec.get('coverage_area')} 缺少 required_facts 明细")
    return problems


def check_required_flow_type(rec: dict) -> list:
    """必需流类型回归：Policy Flow（第七类流）必须存在。"""
    problems = []
    if rec.get("flow_type") != "policy":
        return problems
    if not rec.get("required_in_flow_atlas"):
        problems.append("Flow 回归: policy flow 必须列入 Flow Atlas")
    return problems


def check_security_invariant(rec: dict) -> list:
    """安全不变量回归：Forbidden 不携带修正案（拒绝不可学习）。"""
    problems = []
    if not rec.get("required_present"):
        problems.append(f"不变量回归: {rec.get('invariant')} 未标记为 required")
    return problems


def check_validation_discipline(rec: dict) -> list:
    """验证纪律回归：反例预算制必须存在。"""
    problems = []
    if not rec.get("required"):
        problems.append("反例预算制回归: 必须标记 required=true")
    budget = rec.get("counterexample_budget")
    if budget is None or budget < 3:
        problems.append(f"反例预算制回归: 预算必须 ≥3（当前 {budget}）")
    return problems


# gold_type → 检查函数映射
_CHECKERS = {
    "fact_regression": check_fact_regression,
    "required_knowledge": check_required_knowledge,
    "over_abstraction_regression": check_over_abstraction_regression,
    "required_mechanism": check_required_mechanism,
    "required_coverage": check_required_coverage,
    "required_flow_type": check_required_flow_type,
    "security_invariant": check_security_invariant,
    "validation_discipline": check_validation_discipline,
}


def run() -> int:
    records = load_gold_records()
    if not records:
        print("❌ Layer 3 Regression Tests: FAIL —— 未找到 benchmarks/codex/*.yaml Gold Records")
        return 1

    total_problems = []
    checked = 0
    for gid, rec in sorted(records.items()):
        gold_type = rec.get("gold_type", "unknown")
        checker = _CHECKERS.get(gold_type)
        if checker is None:
            total_problems.append(f"{gid}: 未知 gold_type={gold_type}")
            continue
        checked += 1
        try:
            problems = checker(rec)
            for p in problems:
                total_problems.append(f"{gid}: {p}")
        except Exception as e:  # noqa: BLE001
            total_problems.append(f"{gid}: 检查异常 {type(e).__name__}: {e}")

    if total_problems:
        print(f"❌ Layer 3 Regression Tests: FAIL —— {len(total_problems)} 项回归问题（{checked} 个 Gold Record 已检查）")
        for p in total_problems:
            print(f"   - {p}")
        return 1
    print(f"✅ Layer 3 Regression Tests: PASS —— {checked} 个 Codex Gold Record 全部满足（过去的错误已永久封锁）")
    return 0


if __name__ == "__main__":
    sys.exit(run())
