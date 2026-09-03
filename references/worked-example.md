# Worked Example（Tafcm 真实案例示范）

> 本文件用一次真实考古任务（Tafcm，Flutter 块级 WYSIWYG Markdown 数学文档编辑器）展示全部概念。**强烈建议先读本文件再动手**——用具体例子理解抽象方法论。

## 一、任务的输入与输出

- 输入：一个开发很久的 Flutter 仓库（30+ ADR、8 份 audits、31 份 runs、4 份 spikes、手写 Markdown 解析器、公式渲染链路、Agent 验证工具链）
- 输出（第一阶段）：44 知识对象（20 A / 21 B / 3 C）、9 决策模式、9 失败模式、12 证据链、统一模型（元原则 Trust Engineering + P1~P7）
- 最终形态：飞书知识空间「Tafcm 项目知识库」（首页 + Project Layer + Knowledge Layer：Flow Atlas 七类流 + Core Engineering 四篇 + P1~P7 + Candidates）

## 二、五层阶梯完整示范

### 示范 A：Evidence Loop → P1（声明 ≠ 证据）

- **L1**：RUN-007（2026-08-17）：ADI validate 从 `before=unknown→after=pass` 改为 `before=reproduced→after=not_reproduced`，F1-F7 七段闭环（failure observed → before replay reproduced → production patch git diff 可审计 → fresh runtime → after not_reproduced → invariants → capability regression）；RUN-010：target_failure 差集判定（before_failed − historical）修复"整体状态误报"；RUN-013：evidence_strength 收紧为 synthetic < test_runtime < production_runtime < virtual_device_runtime < physical_device_runtime < visual < human_confirmed，Emulator PASS ≠ release gate PASS
- **L2**：为什么 before 必须 reproduced——before=unknown 是无效证据（无法证明你修的就是那个坏）
- **L3**：复现驱动修复模式（同类：TDD red→green 必须先看到 red、bug 报告必须"可复现"）
- **L4**：**声明 ≠ 证据；信任 = 证据链的完整性与真实性**
- **L5**：每次修复必须绑定 reproduced 证据；未复现不承认修复；不同动作允许不同证据强度

### 示范 B：Untrusted Analyzer → P2（Intelligence ≠ Authority）

- **L1**：Tafcm 的 Agent 不直接读 .md、不直接改码、不直接跑 CI；一切经受控工具（ffx capability verify/diagnose/repair-verify、adi latest-error/trace-show/replay/validate）；repair-verify 是 read-only 重新证明不自己修码（DOGFOOD-RUN-005）；issue-triage.yml 把 PR 未解决评论自动转 Issue；AGENTS.md 定义权限矩阵 + 停止条件（>5 次失败请 Human）
- **L2**：因为 Agent 判断不可靠（RUN-010 曾误报）；一个错误判断 = 一次未授权变更
- **L3**：职责分离 / 最小权限 / 受控接口在 Agent 系统的实例
- **L4**：**Intelligence ≠ Authority** —— 判断力与执行权是两个独立维度
- **L5**：Agent 影响状态的动作必须受控接口化；证明与执行分离；权限按可逆性×影响授予；即使 AI 全错也可回滚可验证可恢复

## 三、七类流完整示范（Evidence Flow，Tafcm 最重要）

```
Claim（Agent 声明"已修复 X"）
  ↓ Capability Contract（assembly_finite 等硬约束）
  ↓ Test（capability_regression 每 RUN 自检）
  ↓ Runtime 验证（RUN：before=reproduced → production patch → after=not_reproduced）
  │   ★ Gate：F1-F7 七段闭环（RUN-007）
  ↓ Evidence（带 evidence_strength 分级）
  │   synthetic < ... < human_confirmed（RUN-013）
  ↓ Release Gate（证据强度是否达该动作门槛）
  │   ★ Gate：Emulator PASS ≠ release gate PASS
  │   ★ Gate：target_failure 差集判定（RUN-010）
  ↓ （通过）→ 合并/发布；（不通过）→ 打回 Agent 重新诊断
```

认知模型：系统从"代码存在"到"功能成立"之间有一条证据生产链，每跳可审计（git diff / RUN 记录 / evidence_strength），信任 = 链条的完整性与真实性。

## 四、重复结构归纳示范

核心工程四条流 + Agent 三条流 + 记忆层并排后，发现重复结构：

```
产生 → 验证 → 授权 → 执行 → 记录
```

出现在：编辑器命令链（Command→Handler→Transaction）、Markdown 链（parse→serialize→roundtrip_fuzz）、公式链（extract→render→plan）、导出链（AST→投影→消费端验证）、Agent 执行链（Analyzer→Validator→Policy）、证据流（Claim→Contract→Gate）、权限流（Intent→Request→Check→Audit）、记忆层（指针≠记录≠证据）。

**归纳**：P2（产生者不拥有验证与执行权）、P5（验证者从不是执行者）、P1（声明≠证据）——不是想出来的，是从八处重复结构中归纳出来的。

## 五、质量演变（三轮用户批评 → 教训）

| 版本 | 做法 | 用户判定 | 教训 |
|------|------|---------|------|
| V1 抽象归纳 | 精读 14/31 ADR，archive 只看开头，代码只看目录名，直接给抽象原则 | "一点价值都没有，完全没吃透" | 没读透代码就抽象 = 空壳 |
| V2 深度版 | 30/30 ADR、全部 audits/runs/spikes、代码核对、git 演化，每篇从事件讲起 | "跳过前 3 步，直接进行认知模型 = 臆想" | 即使证据充分，结构不是五层递进仍不合格 |
| V3 五层阶梯 | 每篇 L1 事实→L2 知识→L3 模式→L4 模型→L5 方法论 | 认可方法，但指出过度提取 Agent | 项目本体（Markdown/公式/编辑器）才是核心工程 |
| V4 双域平衡 | 新增 Core Engineering 四篇 | 指出 Flow 是理解系统的中间层 | 原则应"从流的重复结构看见"而非"想出来" |
| V5 Flow Atlas | 七类流从真实代码导出 | 批判 Data/State Flow 是"画的架构图"非"从代码导出的流" | 每条流必须锚定真实符号 + 数据形态 + 守恒点 + bug 落点 |
| V6 重做 | Data/State/Memory Flow 从真实代码逐行导出 | 认可 | 画得好的流 = 读透的代码 |

**核心教训链**：读透代码 → 五层递进 → 本体优先 → 从流看见原则 → 每条流锚定真实符号。这正是本 skill 工作流 Step 1-5 的由来。
