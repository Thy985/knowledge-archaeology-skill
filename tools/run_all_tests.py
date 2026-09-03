"""knowledge-archaeology-skill CI 统一入口（5 层测试总调度）。

用法：
    python tools/run_all_tests.py            # 跑全部 5 层
    python tools/run_all_tests.py --layer 3  # 只跑某一层

退出码：0 = 全部 PASS；非 0 = 至少一层 FAIL（Quality Gate 未过，禁止合并）。

5 层：
    Layer 1  Contract         Skill 结构完整性（目录/文件/枚举/铁律）
    Layer 2  Deterministic    Epistemic Promotion / 聚合规则确定性逻辑
    Layer 3  Regression       Codex Gold Records（过去错误永久封锁）
    Layer 4  Benchmark        Quality Gates（硬门槛，Promotion Gate）
    Layer 5  Mutation         坏知识检测（系统能否识别自己的错误）
"""

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

LAYERS = {
    1: ("Contract", ["tests", "contract", "test_skill_integrity.py"]),
    2: ("Deterministic Unit", ["tests", "unit", "test_ka_engine.py"]),
    3: ("Knowledge Regression", ["tests", "regression", "test_codex_regression.py"]),
    4: ("Benchmark", ["tests", "benchmark", "test_benchmark_gates.py"]),
    5: ("Mutation / Adversarial", ["tests", "mutation", "test_mutation.py"]),
}


def run_layer(num: int) -> tuple[bool, str]:
    name, rel = LAYERS[num]
    script = REPO_ROOT.joinpath(*rel)
    proc = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )
    output = proc.stdout + proc.stderr
    return proc.returncode == 0, f"[Layer {num} · {name}]" + (" PASS" if proc.returncode == 0 else " FAIL"), output


def main() -> int:
    parser = argparse.ArgumentParser(description="knowledge-archaeology-skill 5 层 CI 统一入口")
    parser.add_argument("--layer", type=int, choices=sorted(LAYERS), help="只跑指定层")
    args = parser.parse_args()

    layers = [args.layer] if args.layer else sorted(LAYERS)
    results = []
    for num in layers:
        ok, summary, output = run_layer(num)
        print(summary)
        if not ok:
            print(output)
        results.append((num, ok))

    failed = [num for num, ok in results if not ok]
    if failed:
        print(f"\n❌ QUALITY GATE FAILED —— 未通过层: {failed}")
        print("   任一 Quality Gate 未过 → 禁止自动合并到生产 Skill")
        return 1
    print(f"\n✅ ALL {len(results)} LAYERS PASS —— Quality Gate 通过，可进入合并/晋升流程")
    return 0


if __name__ == "__main__":
    sys.exit(main())
