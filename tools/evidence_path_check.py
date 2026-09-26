#!/usr/bin/env python3
"""knowledge-archaeology-skill —— evidence 路径存在性检查（EK 可追溯性机械门）。

背景：ARCH-2026-09-23-001（E2B）考古中，EK-19 证据路径写
`packages/js-sdk/src/commands/index.ts`（实际 `sandbox/commands/`）、
EK-10 写 `src/inflight.ts`（实际 `src/api/inflight.ts`），阶段 4 Truth Auditor
抽查未捕获，直到独立验证与写入前检查才暴露。本脚本把"EK evidence 必须锚定
仓库真实路径"变成机械检查，纳入交付前自检（references/delivery.md §四）。

用法：
    python tools/evidence_path_check.py <repo_dir> <ek_file> [more_ek_files...]

逻辑：从 EK 文件中提取形如 `packages/...`（以及 `spec/...`）的路径引用，
逐一校验在 <repo_dir> 下真实存在。缺失路径按文件逐条列出。

退出码：0 = 全部证据路径存在；非 0 = 至少一个路径缺失（Quality Gate 未过）。
"""

import re
import sys
from pathlib import Path

# 覆盖 EK 证据中常见的仓库相对路径形态（不含行号后缀，如 :451）
PATH_RE = re.compile(
    r"(?<![\w./-])((?:packages|spec|tools|scripts|configs|tests)/[A-Za-z0-9_\-./]+"
    r"\.(?:ts|tsx|js|py|md|yaml|yml|proto|json|toml|cfg|sh))"
)


def extract_paths(text: str) -> set[str]:
    return {m.group(1) for m in PATH_RE.finditer(text)}


def check(repo_dir: Path, ek_file: Path) -> list[str]:
    text = ek_file.read_text(encoding="utf-8", errors="replace")
    missing = []
    for p in sorted(extract_paths(text)):
        if not (repo_dir / p).exists():
            missing.append(p)
    return missing


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    repo_dir = Path(sys.argv[1])
    ek_files = [Path(a) for a in sys.argv[2:]]
    total_missing = []
    for f in ek_files:
        missing = check(repo_dir, f)
        for p in missing:
            print(f"[FAIL] {f}: evidence path missing: {p}")
        total_missing.extend(missing)
    if total_missing:
        print(f"\n❌ {len(total_missing)} missing evidence path(s) — Quality Gate 未过，禁止交付")
        return 1
    print("✅ evidence path check PASS — 所有 EK evidence 路径在仓库中真实存在")
    return 0


if __name__ == "__main__":
    sys.exit(main())
