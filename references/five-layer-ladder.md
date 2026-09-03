# Five-Layer Knowledge Ladder（五层知识阶梯）

## 核心

每个知识对象必须按五层完整递进。**判断标准：关键不是"文字越来越抽象"，而是"解释范围越来越大"。** 每一层确实建立在前一层之上。**跳过前 3 步直接进行认知模型 = 臆想**（用户原话："这种直接跳过前 3 步整理提取出来的无疑是不好用或者臆想的"）。

```
L1 工程事实   发生了什么      → 具体的、可溯源的（RUN/ADR/commit/代码行/文件名）
L2 工程知识   为什么这样做    → 因果解释
L3 工程模式   这类问题怎么解  → 可复用模板 + 同类对照（lint/CI/CQRS/…）
L4 认知模型   背后的稳定关系  → 一句话稳定关系
L5 方法论     如何行动        → 可操作准则
```

## 三层知识架构 × 五层阶梯（v3 映射）

> 五层阶梯描述"单条知识的纵向演化"；三层架构描述"知识库的横向分层"。二者是正交关系，映射如下：

```
L1/L2  →  Engineering Knowledge 层（宽底座 · 推理原材料）
           核心机制 / 关键实现 / 关键决策 / 失败与修复 / 测试揭示的行为 / 重要配置 / 边界与例外
L3/L4/L5 → Generalized Knowledge 层（窄尖顶 · 可迁移认知）
           Pattern / Cognitive Model / Methodology
```

**铁律（v3）**：
- **"不够抽象"绝不等于"不重要"**——L1/L2 的工程知识（如 `Weak<Session> → session 释放 → ask("not_allowed")`）回答非常具体而重要的问题，是未来推理的原材料，独立保留
- **升维是特例不是默认**：不是每条工程知识都要爬到 L4；每一种知识都存在它最合适的抽象层
- **宽底座 + 窄尖顶**：知识库目标配比 100+ Facts → 40~60 Engineering Knowledge → 15~25 Patterns → 7~12 Core KO。不允许"只保留 7 个 KO 丢掉 100 条事实"（过度压缩），也不允许"把 40 条工程知识全升维"（过度抽象）
- **抽象错了可回到底层重新推导**：generalized 对象必须能回溯到 engineering 底座；只保存 KO 会让"KO 错了连它是怎么得出来的都不知道"

### 纵向知识链示例（Codex 验证过）

```
Engineering Fact（Weak<Session> 防止循环引用 —— L1，engineering 层）
    ↓
Engineering Knowledge（代理层拦截 + 控制面动态决策 + 生命周期保守降级 —— L2，engineering 层）
    ↓
Pattern（代理层回调 + 控制面决策 + 生命周期降级 是可复用模式 —— L3，generalized 层）
    ↓
Cognitive Model（执行面与决策面解耦，控制面生命周期影响执行面安全降级 —— L4，generalized 层）
```

**关键**：L1/L2 的工程知识**不需要**为升维而存在——它本身就值得保存为 Engineering Mechanism。

## 五层判据表

| 层级 | 核心问题 | 写法要求 | 反例（不合格） |
|------|---------|---------|---------------|
| L1 工程事实 | 发生了什么？ | 具体可溯源，带符号 | "Tafcm 有 Untrusted Analyzer"（无来源） |
| L2 工程知识 | 为什么这样做？ | 因果解释 | "因为这样设计更好" |
| L3 工程模式 | 这类问题通常怎么解？ | 通用解法 + 同类对照 | 只描述本项目 |
| L4 认知模型 | 背后的稳定关系？ | 一句话稳定关系 | 复杂绕口的理论 |
| L5 方法论 | 如何行动？ | 可操作准则（能做） | 抽象口号 |

## 用户验证过的示范（Untrusted Analyzer → P2）

- L1 工程事实：Tafcm 的 Agent 不直接读 .md、不直接改代码、不直接跑 CI；一切经受控工具（ffx capability verify / diagnose / repair-verify、adi latest-error / trace-show / replay / validate）；repair-verify 是 read-only 重新证明不自己修码（DOGFOOD-RUN-005）；issue-triage.yml 把 PR 未解决评论自动转 Issue 而非让 Agent 自裁；AGENTS.md 定义权限矩阵 + 停止条件（>5 次失败请 Human）
- L2 工程知识：因为 Agent 判断不可靠（RUN-010 曾误报）；一个错误判断 = 一次未授权变更
- L3 工程模式：职责分离 / 最小权限 / 受控接口在 Agent 系统的实例（同类：lint、CI 静态分析、human-in-the-loop）
- L4 认知模型：**Intelligence ≠ Authority** —— 判断力（智能）与执行权（权威）是两个独立维度
- L5 方法论：Agent 影响状态的动作必须受控接口化；证明与执行分离；权限按可逆性×影响授予；即使 AI 全错也可回滚可验证可恢复

## 第二示范（Evidence Loop → P1）

- L1：RUN-007（before=unknown→after=pass 改为 before=reproduced→after=not_reproduced）、RUN-010（target_failure 差集）、RUN-013（evidence_strength 收紧，Emulator PASS ≠ release gate PASS）
- L2：为什么必须 before 复现——before=unknown 是无效证据
- L3：复现驱动修复模式（同类：TDD red→green、bug 报告"可复现"门槛）
- L4：**声明 ≠ 证据**，信任 = 证据链的完整性与真实性
- L5：行动准则——每次修复必须绑定 reproduced 证据，未复现不承认修复

## 常见错误（本 skill 踩过的坑）

1. **跳步**：只写 L4/L5，L1-L3 只剩证据编号引用 → 用户判定"一点价值都没有"
2. **深度版但结构仍是命题/证据/挂接**：即使从事件讲起，没按五层递进组织 → 仍被判定"跳过前 3 步"
3. **把"实现细节"当"方法论"**：L3 必须是可复用模板，不是本项目专属细节
4. **升维无据**：只有单一项目证据却写"普遍定律" → 必须标 `Cross-project validation pending`
