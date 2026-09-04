#!/usr/bin/env python3
"""knowledge-archaeology 快速演示 —— 5 分钟跑出第一个考古结果。

在 examples/sample-project 上走一遍"仓库 → 事实 → EK → KO → 质量门"的可执行骨架，
展示本 Skill 的完整产出形态（三层知识架构 + EK Graph + 聚合规则 + 晋升门）。

用法：
    python tools/demo.py                 # 在仓库根目录运行
    python tools/demo.py --full          # 展示全部 EK/KO 卡片

注意：demo 展示的是 Skill 的**确定性质量层**（规则引擎可执行部分）。
完整 Multi-Agent 考古（Discovery→Mining→Synthesis→Validation）需在 Agent 环境中
加载本 Skill 后运行 workflows/archaeology.md。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

import ka_engine  # noqa: E402

SAMPLE_PROJECT = REPO_ROOT / "examples" / "sample-project"
KNOWLEDGE_JSON = SAMPLE_PROJECT / "knowledge.json"


def load() -> dict:
    if not KNOWLEDGE_JSON.exists():
        print(f"未找到示例考古数据: {KNOWLEDGE_JSON}")
        print("请确认在仓库根目录运行：python tools/demo.py")
        sys.exit(1)
    return json.loads(KNOWLEDGE_JSON.read_text(encoding="utf-8"))


def show_map(data: dict) -> None:
    print("=" * 62)
    print("STEP 1 · 仓库地图（Project Layer）")
    print("=" * 62)
    print("sample-agent-runtime —— 极简命令执行代理")
    print("User → Agent(判断) → PermissionGate(三态审批) → Guardian(fail-closed) → Executor")
    print()
    print("  检测到的核心模块:")
    print("    src/agent.py             Agent 主循环（停止条件 5 次升级人类）")
    print("    src/permission_gate.py   三态审批门（Forbidden 不携带修正案）")
    print("    src/exec_policy.py       策略固化（批准→append 规则→未来免审）")
    print("    src/guardian.py          fail-closed 守护（超时/解析错误→拒绝）")
    print("    tests/test_gate.py       测试揭示的安全不变量")
    print("    docs/decisions/ADR-0001  决策：判断力与执行权分离")
    print()


def show_facts(data: dict) -> None:
    print("=" * 62)
    print("STEP 2 · 事实层（L1，6 条 —— 全部锚定 文件:行号）")
    print("=" * 62)
    for f in data["facts"]:
        print(f"  {f['id']}  {f['claim']}")
        print(f"         ↳ {f['source']}")
    print()


def show_ek_graph(data: dict) -> None:
    eks = data["eks"]
    print("=" * 62)
    print(f"STEP 3 · 工程知识层（EK Graph，{len(eks)} 条 —— 每条带 links 边）")
    print("=" * 62)
    for ek in eks:
        links = ", ".join(f"{l['type']}→{l['to']}" for l in ek.get("links", []))
        print(f"  {ek['id']} [{ek['abstraction']}] {ek['claim'][:56]}")
        print(f"         links: {links}")
    print()
    # EK Graph 质量门
    report = ka_engine.validate_ek_graph(eks, data["kos"])
    print("  —— EK Graph 质量门 ——")
    print(f"     EK 数: {report['ek_count']}   平均出边: {report['avg_edges']:.2f}   "
          f"游离比例: {report['isolated_ratio']:.0%}   "
          f"聚合覆盖率: {report['aggregation_coverage']:.0%}")
    for size in report["ko_cluster_sizes"]:
        print(f"     KO 簇规模: {size}（健康区间 [3,12]）")
    print(f"     EK Graph 质量门: {'✅ PASS' if report['pass'] else '❌ FAIL: ' + str(report.get('failures'))}")
    print()


def show_kos(data: dict, full: bool) -> None:
    print("=" * 62)
    print("STEP 4 · 认知层（Generalized KO —— 窄尖顶）")
    print("=" * 62)
    for ko in data["kos"]:
        ar = ko["aggregation_rule"]
        print(f"  ★ {ko['id']}  [{ko['abstraction']} | {ko['value']} | {ko['epistemic_status']}]")
        print(f"    claim: {ko['claim']}")
        print(f"    聚合规则: {ar['rule']}（簇: {', '.join(ar['cluster_eks'])}）")
        print(f"    naming: {ar['naming'][:80]}")
        if full:
            print(f"    追溯到底座: {', '.join(ko['derivation']['facts'])}")
            print(f"    flow_traceability: {', '.join(ko.get('flow_traceability', []))}")
            print(f"    scope 适用: {', '.join(ko['scope']['applies_when'])}")
        print()
    # KO schema 验证
    print("  —— KO Schema 校验（ka_engine.validate_knowledge_object）——")
    for ko in data["kos"]:
        issues = ka_engine.validate_knowledge_object(ko, ko["id"])
        status = "✅ 通过" if not issues else f"❌ {len(issues)} 个问题"
        print(f"     {ko['id']}: {status}")
        for i in issues:
            print(f"        - {i.message}")
    print()


def show_promotion(data: dict) -> None:
    print("=" * 62)
    print("STEP 5 · 晋升判定演示（Abstraction Promotion Gate —— 确定性规则）")
    print("=" * 62)
    cases = [
        ("单实例观察", ka_engine.PromotionInput(evidence_count=1, independent_instances=1, different_modules=1)),
        ("跨 2 模块重复结构", ka_engine.PromotionInput(evidence_count=3, independent_instances=2, different_modules=2)),
        ("跨上下文 + 运行时验证 + 人工确认", ka_engine.PromotionInput(
            evidence_count=5, independent_instances=3, different_modules=3,
            cross_context=True, runtime_validated=True, human_confirmed=True)),
        ("存在反例", ka_engine.PromotionInput(
            evidence_count=5, independent_instances=3, different_modules=3,
            cross_context=True, runtime_validated=True, counterexamples_found=1)),
    ]
    for name, pi in cases:
        max_lvl = ka_engine.compute_max_abstraction(pi)
        print(f"  {name:<28} → 允许最高 {max_lvl}")
    # 演示晋升门：拦截 vs 放行（KO-01 声称 L4）
    print()
    ko1 = next(k for k in data["kos"] if k["id"] == "KO-01")
    # 场景 A：缺人工确认（sample-project 当前证据）
    pi_a = ka_engine.PromotionInput(
        evidence_count=6, independent_instances=3, different_modules=3,
        cross_context=True, runtime_validated=True, human_confirmed=False,
        counterexamples_found=0)
    v_a = ka_engine.check_promotion_legitimacy(pi_a, ko1["abstraction"])
    # 场景 B：补上 S7 人工确认
    pi_b = ka_engine.PromotionInput(
        evidence_count=6, independent_instances=3, different_modules=3,
        cross_context=True, runtime_validated=True, human_confirmed=True,
        counterexamples_found=0)
    v_b = ka_engine.check_promotion_legitimacy(pi_b, ko1["abstraction"])
    print(f"  KO-01 声称 {ko1['abstraction']}（跨 3 模块 + 运行时验证）")
    print(f"    ├─ 缺 S7 人工确认 → {v_a['max_allowed']} → {'✅ 放行' if v_a['allowed'] else '❌ 拦截（证据不足须降级）'}")
    print(f"    └─ 补 S7 人工确认 → {v_b['max_allowed']} → {'✅ 放行' if v_b['allowed'] else '❌ 拦截'}")
    print()
    print("  ▲ Abstraction Promotion Gate 在正常工作：")
    print("    无人工确认的 L4 声称会被拦截——这正是'禁止把未验证假设写成原则'的机器化。")
    print()


def show_summary(data: dict) -> None:
    print("=" * 62)
    print("RESULT · 一次考古的可执行骨架（约 5 分钟）")
    print("=" * 62)
    eks, kos, facts, cands = data["eks"], data["kos"], data["facts"], data["candidates"]
    a = sum(1 for k in kos if k["value"] == "A")
    print(f"  Facts(事实底座): {len(facts)}    EK(工程知识): {len(eks)}    "
          f"KO(认知): {len(kos)}（{a} 个 A 级）    Candidates: {len(cands)}")
    print()
    print("  Most Important Finding:")
    print("  > 这个项目让我们认识到：当执行权与判断力分离，并由'拒绝不可学习'+'fail-closed'")
    print("  > 两条不变量兜底时，即使 Agent 全错，系统仍可控、可验证、可恢复。")
    print()
    print("  下一步（在 Agent 环境做完整考古）：")
    print("    1) 把本仓库安装为 Skill（python scripts/install.py）")
    print("    2) 触发场景：'整理这个项目的知识' / '对 <你的仓库> 做一次知识考古'")
    print("    3) Skill 会运行 workflows/archaeology.md 的完整 Multi-Agent 管线")
    print("    4) 默认交付：push 到 knowledge-archaeology-corpus 仓库；飞书需授权")
    print("=" * 62)


def main() -> int:
    parser = argparse.ArgumentParser(description="knowledge-archaeology 快速演示")
    parser.add_argument("--full", action="store_true", help="展示完整 EK/KO 卡片")
    args = parser.parse_args()

    data = load()
    show_map(data)
    show_facts(data)
    show_ek_graph(data)
    show_kos(data, full=args.full)
    show_promotion(data)
    show_summary(data)
    return 0


if __name__ == "__main__":
    sys.exit(main())
