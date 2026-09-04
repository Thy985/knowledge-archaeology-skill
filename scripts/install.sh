#!/usr/bin/env bash
# knowledge-archaeology 一键安装（Linux / macOS）
# 用法:
#   ./scripts/install.sh                 # 自动探测 skill root
#   ./scripts/install.sh --target <dir>  # 指定位置
#   ./scripts/install.sh --with-ci       # 连同 5 层 CI 一起装（开发）
set -euo pipefail

cd "$(dirname "$0")/.."

if ! command -v python3 >/dev/null 2>&1; then
  echo "需要 python3，未找到。" >&2
  exit 1
fi

python3 scripts/install.py "$@"
