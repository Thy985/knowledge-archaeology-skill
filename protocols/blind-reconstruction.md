# Blind Reconstruction（独立盲重建协议）— v2 新增

> Validator 的独立制衡协议。解决 v1 的"同源自我确认"缺陷
> （Validator 与 Miner 共享同一推理链，False Acceptance ≈43%）。
> 铁律：**验证 = 重新做一遍再判断，不是"证明这个答案没问题"。**

## 核心原则

```
❌ 已有 Knowledge → 找支持它的证据 → 宣布验证通过（Same-source Confirmation）
✅ 先独立盲重建 → 再与已有 Knowledge 对比 → 判断（Blind Reconstruction）
```

## 什么时候必须 Blind Reconstruction

- **truth-auditor**：核验每个 claim 前，先独立从仓库重建该 claim 涉及的事实
- **abstraction-auditor**：判定每个 L3+ KO 前，先独立判断"我认为它应该是几层"
- **coverage-auditor**：始终独立重搜（v1 已有，强化为强制）
- **flow-auditor**：核验 Flow Edge 前，先独立从代码还原该段流

## 执行方式（epistemic 隔离）

1. **独立 SubAgent**：Blind Reconstruction 必须由**不含 Miner/Synthesizer 上下文**的独立实例执行
   - 可用隔离 SubAgent（创建时不给已有结论，只给仓库路径 + 审计规格 + claim 清单）
   - 或在同一上下文内，先写下"我对仓库的独立理解"（不参考 KO），再进入对比
2. **两阶段产出**：
   - 阶段 A（盲）：只读仓库，产出 Independent Findings（不看任何 KO/Flow/验证报告）
   - 阶段 B（对比）：拿 Independent Findings 与已有 KO 对比，逐条判定
3. **禁止**：阶段 A 中参考任何"结论性材料"（既有 KO、验证报告、README 声明、ADR 意图）

## 判定输出

对每个 claim 独立判定：

```
CONFIRMED      独立分析 + 已有 KO 一致，证据充分
PARTIALLY_CONFIRMED  核心方向对，但 scope/条件/例外不完整
DOWNGRADED     结论成立，但抽象层级过高（L4→L3）
OVER_GENERALIZED  项目局部被写成广泛原则
MISSING        独立分析发现的重要知识，已有考古未提取
CONTRADICTED   仓库存在直接反驳证据
NEEDS_HUMAN_REVIEW  证据冲突无法自动裁决
```

## 与 Evidence Graph 的关系

- 阶段 A 允许重新建 Independent Evidence（不限于 Synthesizer 用的同一 Evidence Graph）
- 两套证据对比时：若独立证据与 Evidence Graph 冲突，以仓库原始代码为准（Repository is the Source of Truth）

## 禁则

- ❌ 不读取 Miner/Synthesizer 的推理过程来"校准"自己的判断
- ❌ 不因已有 KO "写得完整/专业/有证据引用"就默认正确
- ❌ 阶段 A 不围绕任何预设结论收集证据
- ❌ 不把"大概符合项目设计"当 PASS（必须有具体 symbol 证据）
