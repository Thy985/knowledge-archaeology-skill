#!/usr/bin/env python3
"""knowledge-archaeology 一键安装器（跨平台）。

把本仓库安装为可用的 Skill（复制到 skill root）。
- 默认安装"运行本体"：SKILL.md + agents/ contracts/ protocols/ references/ workflows/
- --with-ci 额外安装 5 层 CI 资产：tests/ rules/ tools/ benchmarks/ evals/ evolution/（开发/CI 用途）

用法：
    python scripts/install.py                      # 自动探测 skill root（或提示指定）
    python scripts/install.py --target <dir>       # 指定安装位置
    python scripts/install.py --with-ci            # 连同 CI 一起安装（开发）
    python scripts/install.py --self-test          # 安装后跑 Layer 1 Contract 自检（需 --with-ci）

一键（从 GitHub）：
    git clone git@github.com:Thy985/knowledge-archaeology-skill.git
    cd knowledge-archaeology-skill
    python scripts/install.py

退出码：0 = 成功；1 = 失败。
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_NAME = "knowledge-archaeology"

# 运行本体（Skill 实际运行所需）
RUNTIME_PARTS = [
    "SKILL.md",
    "agents",
    "contracts",
    "protocols",
    "references",
    "workflows",
]

# CI 资产（开发/质量门所需，默认不装）
CI_PARTS = [
    "tests",
    "rules",
    "tools",
    "benchmarks",
    "evals",
    "evolution",
    ".github",
    "README.md",
    "LICENSE",
]


def probe_skill_roots() -> list[Path]:
    """探测常见 skill root（优先级从高到低）。"""
    roots: list[Path] = []

    # 1) 环境变量
    for env in ("SKILL_ROOT", "KNOWLEDGE_ARCHAEOLOGY_SKILL_ROOT"):
        v = os.environ.get(env)
        if v:
            roots.append(Path(v))
    v = os.environ.get("SKILL_ROOTS")
    if v:
        roots.extend(Path(p) for p in v.split(os.pathsep) if p)

    # 2) 常见平台路径
    home = Path.home()
    candidates = [
        # Doubao / 豆包
        home / "AppData/Local/Doubao/User Data/Default/.doubao/agent_mode/workspace/.user_skills",
        home / "AppData/Local/Doubao/User Data/Default/.doubao/agent_mode/workspace/.skills",
        home / "Doubao/skills",
        # 通用 .agents
        home / ".agents/skills",
        home / ".doubao/agent_mode/workspace/.user_skills",
        home / ".doubao/agent_mode/workspace/.skills",
    ]
    for c in candidates:
        # 只保留"看起来存在"或"父级存在"的候选（存在一个真实 skill 的根）
        if c.exists() and any(p.is_dir() for p in c.iterdir()):
            roots.append(c)

    # 去重（保留顺序）
    seen: set[str] = set()
    out: list[Path] = []
    for r in roots:
        key = str(r).lower()
        if key not in seen:
            seen.add(key)
            out.append(r)
    return out


def install(target_root: Path, with_ci: bool, parts: list[str]) -> list[Path]:
    """把 parts 复制到 target_root/SKILL_NAME/。返回已安装文件/目录绝对路径。"""
    dest = target_root / SKILL_NAME
    dest.mkdir(parents=True, exist_ok=True)
    installed: list[Path] = []
    for part in parts:
        src = REPO_ROOT / part
        if not src.exists():
            print(f"  [skip] {part}（仓库中不存在）")
            continue
        d = dest / part
        if d.exists():
            if d.is_dir():
                shutil.rmtree(d)
            else:
                d.unlink()
        if src.is_dir():
            shutil.copytree(src, d)
        else:
            shutil.copy2(src, d)
        installed.append(d)
    return installed


def run_self_test(dest: Path) -> bool:
    """安装后跑 Layer 1 Contract 自检（需要 tests/ + tools/ + rules/）。"""
    script = dest / "tools" / "run_all_tests.py"
    if not script.exists():
        print("  [self-test] 跳过：未找到 tools/run_all_tests.py（需要 --with-ci）")
        return True
    print("  [self-test] 运行 5 层 CI（可加 --layer 只跑指定层）…")
    proc = subprocess.run([sys.executable, str(script), "--layer", "1"],
                          cwd=str(dest))
    return proc.returncode == 0


def main() -> int:
    parser = argparse.ArgumentParser(description="knowledge-archaeology 一键安装器")
    parser.add_argument("--target", help="目标 skill root（默认自动探测）")
    parser.add_argument("--with-ci", action="store_true",
                        help="同时安装 5 层 CI 资产（tests/rules/tools/benchmarks/evals/evolution）")
    parser.add_argument("--self-test", action="store_true",
                        help="安装后跑 Layer 1 Contract 自检")
    args = parser.parse_args()

    print("=" * 60)
    print("knowledge-archaeology 一键安装")
    print("=" * 60)

    # 1. 确定目标 root
    target: Path | None = None
    if args.target:
        target = Path(args.target).resolve()
    else:
        roots = probe_skill_roots()
        if roots:
            target = roots[0]
            print(f"  [root] 自动探测到: {target}")
            if len(roots) > 1:
                print(f"         另有候选: {[str(r) for r in roots[1:]]}")
        else:
            print("  [root] 未探测到常见 skill root。")
            print("         请用 --target 显式指定，例如：")
            print("           python scripts/install.py --target \"<你的 skill 根目录>\"")
            return 1

    if not target.is_dir():
        target.mkdir(parents=True, exist_ok=True)
        print(f"  [root] 已创建: {target}")

    # 2. 安装
    parts = list(RUNTIME_PARTS)
    if args.with_ci:
        parts += CI_PARTS
    print(f"  [install] 目标: {target / SKILL_NAME}")
    print(f"  [install] 组件: {', '.join(RUNTIME_PARTS)}" +
          (" + CI 资产" if args.with_ci else "（运行本体；加 --with-ci 安装 CI）"))
    installed = install(target, args.with_ci, parts)
    print(f"  [install] 完成：{len(installed)} 个组件已安装")

    # 3. 自检
    dest = target / SKILL_NAME
    ok = True
    if args.self_test:
        ok = run_self_test(dest)

    # 4. 报告
    print("-" * 60)
    print("安装成功 ✅")
    print(f"  Skill 位置: {dest}")
    print(f"  SKILL.md  : {dest / 'SKILL.md'}")
    print()
    print("下一步：")
    print(f"  1) 在支持 Skill 的 Agent 环境中，把 {dest} 加入 skill root（若尚未覆盖）")
    print("  2) 触发场景：整理项目知识 / 提炼项目经验 / 项目复盘升维")
    print("  3) 快速体验可执行骨架：")
    print("       python tools/demo.py   （需在仓库根目录运行，见 README）")
    if not args.with_ci:
        print()
        print("  提示：安装 CI（测试/规则/引擎）用：python scripts/install.py --with-ci --self-test")
    print("=" * 60)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
