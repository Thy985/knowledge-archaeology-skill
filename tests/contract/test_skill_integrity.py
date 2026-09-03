"""Layer 1 · Contract Tests —— 校验 Skill 自身结构完整性（Skill Integrity）。

CI 测试的不是"代码有没有编译过"，而是"Skill 这个知识生产系统有没有结构性损坏"。

检查：
- SKILL.md frontmatter 版本合法
- agents/ 20 个角色文件齐全
- contracts/ 6 个 schema 文件齐全
- protocols/ workflows/ references/ 目录完整
- 各契约文件中的枚举合法（L1-L5、epistemic status、flow types、edge types、aggregation rules）
- 角色文件引用的角色名合法
- 文档中"高危跃迁"声明（禁止 Fact→Principle 等）存在
"""

import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))
import ka_engine  # noqa: E402

SKILL_ROOT = REPO_ROOT

# 期望的目录/文件清单（与 SKILL.md 目录导航一致）
EXPECTED_DIRS = ["agents", "contracts", "protocols", "references", "workflows"]
EXPECTED_CONTRACTS = [
    "ek-graph-schema.md", "epistemic-status.md", "evidence-schema.md",
    "flow-schema.md", "knowledge-schema.md", "validation-schema.md",
]
EXPECTED_AGENTS = [
    "repository-mapper", "code-analyst", "doc-analyst", "test-analyst",
    "failure-analyst", "authority-analyst", "policy-governance-analyst",
    "problem-miner", "decision-miner", "pattern-miner", "flow-miner",
    "engineering-knowledge-miner", "knowledge-synthesizer",
    "truth-auditor", "coverage-auditor", "flow-auditor",
    "abstraction-auditor", "counterexample-hunter", "epistemic-auditor",
    "reconciler",
]
EXPECTED_PROTOCOLS = [
    "agent-handoff.md", "blind-reconstruction.md", "disagreement.md",
    "escalation.md", "evidence-provenance.md", "promotion.md",
]
EXPECTED_WORKFLOWS = ["archaeology.md", "benchmark.md", "validation.md"]
EXPECTED_REFERENCES = [
    "code-comprehension.md", "feishu-delivery.md", "five-layer-ladder.md",
    "flow-atlas.md", "knowledge-classification.md", "worked-example.md",
]


def _failures() -> list:
    """收集所有结构性问题，汇总返回。"""
    problems = []

    def check(cond: bool, msg: str) -> None:
        if not cond:
            problems.append(msg)

    # ---- 1. 顶层文件 ----
    check((SKILL_ROOT / "SKILL.md").exists(), "缺少 SKILL.md")
    check((SKILL_ROOT / "README.md").exists(), "缺少 README.md")
    check((SKILL_ROOT / "LICENSE").exists(), "缺少 LICENSE")

    # ---- 2. 目录完整性 ----
    for d in EXPECTED_DIRS:
        check((SKILL_ROOT / d).is_dir(), f"缺少目录 {d}/")

    # ---- 3. contracts 完整性 ----
    for c in EXPECTED_CONTRACTS:
        check((SKILL_ROOT / "contracts" / c).exists(), f"缺少契约文件 contracts/{c}")

    # ---- 4. agents 完整性 ----
    for a in EXPECTED_AGENTS:
        check((SKILL_ROOT / "agents" / f"{a}.md").exists(), f"缺少角色文件 agents/{a}.md")

    # ---- 5. protocols 完整性 ----
    for p in EXPECTED_PROTOCOLS:
        check((SKILL_ROOT / "protocols" / p).exists(), f"缺少协议文件 protocols/{p}")

    # ---- 6. workflows 完整性 ----
    for w in EXPECTED_WORKFLOWS:
        check((SKILL_ROOT / "workflows" / w).exists(), f"缺少工作流文件 workflows/{w}")

    # ---- 7. references 完整性 ----
    for r in EXPECTED_REFERENCES:
        check((SKILL_ROOT / "references" / r).exists(), f"缺少参考文件 references/{r}")

    # ---- 8. SKILL.md frontmatter ----
    skill_md = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
    m = re.search(r"^version:\s*(\S+)", skill_md, re.MULTILINE)
    check(m is not None, "SKILL.md frontmatter 缺少 version")
    if m:
        ver = m.group(1)
        check(re.match(r"^\d+\.\d+(\.\d+)?$", ver), f"SKILL.md version 非法: {ver}")
    check("knowledge-archaeology" in skill_md[:200], "SKILL.md frontmatter name 缺失")
    m_desc = re.search(r"^description:\s*(.+)", skill_md, re.MULTILINE)
    check(m_desc is not None, "SKILL.md frontmatter 缺少 description")

    # ---- 9. 契约文件中的枚举合法性 ----
    # knowledge-schema.md 应声明合法 abstraction levels
    ks = (SKILL_ROOT / "contracts" / "knowledge-schema.md").read_text(encoding="utf-8")
    check('"abstraction": "L0|L1|L2|L3|L4"' in ks or "L0|L1|L2|L3|L4" in ks,
          "knowledge-schema.md 缺少 abstraction 枚举声明")
    check("engineering|generalized" in ks, "knowledge-schema.md 缺少 knowledge_layer 枚举声明")
    check("R1" in ks and "R4" in ks, "knowledge-schema.md 缺少聚合规则 R1-R4 声明")

    # ek-graph-schema.md 应声明 6 类边
    if (SKILL_ROOT / "contracts" / "ek-graph-schema.md").exists():
        eg = (SKILL_ROOT / "contracts" / "ek-graph-schema.md").read_text(encoding="utf-8")
        for edge in ["mechanism", "subsystem", "causal", "dependency", "constraint", "contrast"]:
            check(edge in eg, f"ek-graph-schema.md 缺少边类型 {edge}")

    # epistemic-status.md 应声明状态谱系
    es = (SKILL_ROOT / "contracts" / "epistemic-status.md").read_text(encoding="utf-8")
    check("Fact" in es and "Law" in es, "epistemic-status.md 缺少认知状态谱系")
    check("Hypothesis" in es and "Principle" in es, "epistemic-status.md 缺少中间状态")

    # flow-schema.md 应有七类流
    if (SKILL_ROOT / "contracts" / "flow-schema.md").exists():
        fs = (SKILL_ROOT / "contracts" / "flow-schema.md").read_text(encoding="utf-8")
        for ft in ["control", "state", "data", "evidence", "authority", "memory", "policy"]:
            check(ft in fs, f"flow-schema.md 缺少流类型 {ft}")

    # ---- 10. 高危跃迁声明（v2 教训：过度升维必须被文档拦截） ----
    high_risk_docs = ["epistemic-status.md", "references/five-layer-ladder.md"]
    for doc in high_risk_docs:
        p = SKILL_ROOT / doc
        if p.exists():
            content = p.read_text(encoding="utf-8")
            # 无中间推导禁令（不同文档措辞不同：five-layer-ladder 用"跳过前 3 步/直接认知模型"，
            # epistemic-status 用"Fact → Principle / 无中间推导 / 逐级推导"）
            no_jump = any(kw in content for kw in [
                "Fact → Principle", "Fact→Principle", "无中间推导", "逐级推导",
                "跳过前 3 步", "直接进行认知模型", "直接升 L", "Fact→Principle 无中间推导",
            ])
            check(no_jump, f"{doc} 缺少'禁止无中间推导跳级'禁令声明")
            check("Cross-project validation pending" in content or "跨项目验证" in content,
                  f"{doc} 缺少'跨项目验证 pending'规则")

    # ---- 11. v3.1 防退化铁律在 SKILL.md 中声明 ----
    check("EK Graph" in skill_md or "EK 不是扁平清单" in skill_md,
          "SKILL.md 缺少 v3.1 EK Graph 核心章节")
    check("aggregation_rule" in skill_md or "聚合规则" in skill_md,
          "SKILL.md 缺少 v3.1 聚合规则声明")

    # ---- 12. 理想配比声明（宽底座 + 窄尖顶） ----
    check("宽底座" in skill_md and "窄尖顶" in skill_md,
          "SKILL.md 缺少'宽底座 + 窄尖顶'三层架构声明")

    return problems


def run() -> int:
    problems = _failures()
    if problems:
        print(f"❌ Layer 1 Contract Tests: FAIL ({len(problems)} 项问题)")
        for p in problems:
            print(f"   - {p}")
        return 1
    print(f"✅ Layer 1 Contract Tests: PASS（目录/文件/枚举/铁律全部完整）")
    return 0


if __name__ == "__main__":
    sys.exit(run())
