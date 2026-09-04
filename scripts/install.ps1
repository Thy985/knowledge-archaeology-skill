# knowledge-archaeology 一键安装（Windows PowerShell）
# 用法:
#   .\scripts\install.ps1                # 自动探测 skill root
#   .\scripts\install.ps1 -Target <dir>  # 指定位置
#   .\scripts\install.ps1 -WithCi        # 连同 5 层 CI 一起装（开发）
param(
    [string]$Target,
    [switch]$WithCi,
    [switch]$SelfTest
)

$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")

$args = @()
if ($Target) { $args += "--target"; $args += $Target }
if ($WithCi) { $args += "--with-ci" }
if ($SelfTest) { $args += "--self-test" }

python scripts/install.py @args
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
