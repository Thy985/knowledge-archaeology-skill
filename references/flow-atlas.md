# Flow Atlas（七类流）— v2

> v2 新增第七类流 **Policy Flow**（治理闭环）。背景：Codex v1 Benchmark 发现考古对"系统如何持续约束自己"（Policy Governance / Feedback Loop / Context Control）不敏感，遗漏 exec_policy / 上下文治理 / 审批→策略固化三个高价值机制。Policy Flow 补这个盲区。

## 定位

Flow 与 State 是连接"工程资产"与"工程知识/模式/认知模型"的**结构化中间层**：

```
工程资产 → 系统结构重建 → 流/状态重建 → 事实/行为/结果/证据关联 → 工程知识 → 模式 → 认知模型 → 方法论
```

**原则必须从流的重复结构中被"看见"，而不是被"发明"。** 只读 ADR 只能知道"设计上要求分离"；画出控制流才看到"AI 不直接拥有执行权"是通过什么运行时结构实现的。

## 铁律：不是画图任务

每条流必须：
1. **锚定真实符号**（类/方法/文件名/行号/ADR/RUN）——禁止概念箭头
2. 标注**数据形态变化**（String → List\<DocumentElement\> → …）
3. 标注**决策点/Gate 带判定逻辑**（不是"★ Gate"，而是"RUN-013 七级阈值怎么判定"）
4. 标注**守恒点 / 降级态 / bug 落点**
5. 结尾给出"从这条流看见的认知模型"

画得好的流 = 读透的代码；画得空的流 = 没读透的代码。

## 七类流定义

### 1. Control Flow（控制流）
- 回答：谁决定下一步做什么？
- 关注：决策点、分支、Gate、Human approval、Retry、Rollback、Escalation
- 适合提取：Agent Governance（决策点分布 = 控制权结构）

### 2. State Flow（状态流）
- 回答：系统状态如何变化？
- 关注：状态容器、生命周期、可逆性、状态机、状态转换触发事件、bug 落点
- 例：Committed → Transaction → Live → Validation → Commit → History；IME 4 态状态机
- 认知来源：不同生命周期状态不能混容器（P3）

### 3. Data Flow（数据流）
- 回答：数据从哪产生到哪去？
- 关注：转换边界（危险区）、数据形态、守恒点、单一真相源
- 例：Markdown → Parser → AST → Serializer（round-trip 不动点）；公式 LaTeX → RenderPlan（SVG→PNG→文本降级）

### 4. Evidence Flow（证据流）—— 对 Agent 项目尤其重要
- 回答：声明如何变成可证明？
- 关注：Claim → Capability Contract → Test → Runtime → Evidence → Evidence Strength → Release Gate
- 认知来源：系统不是从"代码存在"跳到"功能成立"，中间存在证据生产链（P1 结构性来源）

### 5. Authority Flow（权限流）
- 回答：每一步到底谁拥有执行权？
- 关注：AI Intent → Capability Request → Permission Check → Execution Boundary → Action → Audit
- 认知来源：Intelligence ≠ Authority（P2 可审计化）

### 6. Memory Flow（记忆流）
- 回答：记忆如何流转与沉淀？
- 关注：分层上下文（Always/Phase/Scope）、状态指针 vs 完整证据、会话记忆降权、有界事件记录、事实账本
- 注意：**先核实项目里真实存在什么记忆资产**（.agent/、docs/evidence、audit），不要用"经典 Agent 记忆链"硬套

### 7. Policy Flow（政策流）—— v2 新增，针对 Agent/AI 系统
- 回答：**系统如何改变自己"下一步"的规则？**
- 关注：治理闭环 / 自我约束 / 反馈循环 / 上下文治理 / 策略固化
- 标准链：`Decision → Approval → Policy → Enforcement → Future Decision`
- 例（Codex 验证过）：审批通过 → 提议把 allow 规则落盘（proposed_execpolicy_amendment → blocking_append_allow_prefix_rule）→ ExecPolicyManager 对后续命令匹配 rules → 同类命令免审/危险命令拒绝
- 认知来源：系统通过机制持续约束自己（Policy Governance），不是一次性设计
- 与 Control Flow 区别：Control 回答"下一步做什么"；Policy 回答"系统如何改变自己对'下一步'的规则"——是 Feedback Loop 的载体
- 注意：**先核实项目真实治理资产**（policy 文件、rules、guard、审批→策略固化点、上下文硬限制），不臆造策略链

## 知识对象 × 七类流关联

理想情况下每个知识对象最终关联：

```
Knowledge Object
├── Control Flow（谁决定）
├── State Flow（状态如何变）
├── Data Flow（数据如何走）
├── Evidence Flow（如何证明）
├── Authority Flow（谁有执行权）
├── Memory Flow（记忆如何沉淀）
├── Policy Flow（规则如何被固化与演进）
└── Source Evidence（代码/ADR/测试/RUN）
```

## 重复结构归纳（最关键一步）

把多条流的骨架并排，找重复出现的结构。例（Tafcm 验证过）：

```
产生（Command/Analyzer/渲染器）→ 验证（roundtrip_fuzz/Validator/telemetry）→ 授权（Policy）→ 执行 → 记录
```

该结构在编辑器命令链、Agent 执行链、渲染降级链、导出投影链、记忆层**多处独立出现** → 归纳出 P2（Intelligence ≠ Authority）、P5（验证独立于执行）、P1（声明≠证据）。**这不是想出来的，是从结构中归纳出来的。**
