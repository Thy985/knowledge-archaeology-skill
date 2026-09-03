"""PR 风险自动分级（Progressive Autonomy 核心）——替代手动 label。

给定 PR 变更文件列表，按 rules/risk-paths.json 自动判定风险等级：
- High   ：即使 Quality Gate PASS 也永不自动合并（epistemic promotion / validation policy / agent orchestration）
- Medium ：需人工审
- Low    ：Quality Gate PASS 自动合并

优先级：任一 High 路径命中 → High；否则任一 Medium → Medium；否则全 Low → Low。
"""

from __future__ import annotations

import fnmatch
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))
import ka_engine  # noqa: E402

RISK_ORDER = ["low", "medium", "high"]


def match_path(path: str, patterns: list) -> bool:
    """fnmatch 匹配（支持 ** 通配）。路径统一正斜杠。"""
    path = path.replace("\\", "/")
    for pat in patterns:
        p = pat.replace("\\", "/")
        if fnmatch.fnmatch(path, p):
            return True
        # 兼容目录通配：'agents/**' 也匹配 'agents/xxx.md'
        if p.endswith("/**") and path.startswith(p[:-3]):
            return True
    return False


def evaluate_risk(changed_files: list[str]) -> dict:
    """评估 PR 风险等级。

    返回:
      {
        "risk": "low|medium|high",
        "auto_merge_allowed": bool,
        "matched": {"high": [...], "medium": [...], "low": [...]},
      }
    """
    risk_rules = ka_engine.get_risk_rules()
    levels = risk_rules.get("risk_levels", {})
    auto_merge_cfg = risk_rules.get("auto_merge", {})

    matched = {"high": [], "medium": [], "low": []}
    for f in changed_files:
        placed = False
        # 按优先级：先检查 high，再 medium，再 low
        for level in ["high", "medium", "low"]:
            pats = levels.get(level, {}).get("paths", [])
            if match_path(f, pats):
                matched[level].append(f)
                placed = True
                break
        if not placed:
            # 未匹配任何规则的文件 → 保守视为 medium（未知变更 = 需人审）
            matched["medium"].append(f)

    if matched["high"]:
        risk = "high"
    elif matched["medium"]:
        risk = "medium"
    else:
        risk = "low"

    # 自动合并条件：auto_merge.enabled && risk == low（Phase 2 默认只合并低风险）
    auto_merge_allowed = (
        auto_merge_cfg.get("enabled", True)
        and risk == "low"
        and auto_merge_cfg.get("require_quality_gate", True)
    )

    return {
        "risk": risk,
        "auto_merge_allowed": auto_merge_allowed,
        "phase": auto_merge_cfg.get("phase", 2),
        "matched": matched,
    }


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print(__doc__)
        print("用法: python tools/evaluate_pr_risk.py <changed_file> [<changed_file> ...]")
        return 2
    result = evaluate_risk(argv)
    print(f"Risk level: {result['risk'].upper()}")
    print(f"Auto-merge allowed: {result['auto_merge_allowed']} (phase {result['phase']})")
    for level in ["high", "medium", "low"]:
        files = result["matched"][level]
        if files:
            print(f"  [{level}] {len(files)} file(s): {', '.join(files[:5])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
