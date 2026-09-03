# Knowledge Object Schema（知识对象契约）— v3

> 多 Agent 考古的最终产物。每个 Knowledge Object 必须能回答"谁发现的、谁支持的、谁反对的、证据是什么、适用于什么"。
> v2 新增：①Policy Flow 纳入 flows ②flow_traceability（L1 事实回溯 Flow Edge）③promotion 论证块。
> v3 新增：①**`knowledge_layer` 字段**（engineering / generalized）——三层知识架构，底层工程知识独立保留 ②工程知识对象允许 L1/L2 独立成篇 ③generalized 对象必须能回溯到 engineering 底座。
> v3.1 新增：①**EK 不是扁平清单，是图的节点**——每条 engineering 对象必须声明 `links`（边类型见 `contracts/ek-graph-schema.md`）②**KO 不是手工挑选的 EK 列表，是 EK 图上的簇**——generalized 对象必须声明 `aggregation_rule`（R1-R4 聚合规则），禁止"因为都属于某子系统所以放一起"。

## 三层知识架构

```
Project Layer（项目地图：架构/模块/配置/生命周期/依赖/入口）
   │
   ▼
Engineering Knowledge（L1/L2：核心机制/关键实现/决策/失败/配置/边界）← 宽底座，推理原材料
   │
   ▼
Generalized Knowledge（L3/L4/L5：Pattern / Cognitive Model / Methodology）← 窄尖顶，可迁移认知
```

**本 schema 统一管理两层 Knowledge Object**（engineering 与 generalized），用 `knowledge_layer` 区分。

## 层间关系：EK 图与聚合（v3.1）

```
Engineering Knowledge（EK，宽底座）
  ├── 每个 EK = 图节点，声明 links（6 类边：mechanism/subsystem/causal/dependency/constraint/contrast）
  └── 边定义见 contracts/ek-graph-schema.md
         │
         ▼ 聚合规则（R1 机制簇 / R2 因果链簇 / R3 不变量簇 / R4 主题簇）
Generalized Knowledge（KO，窄尖顶）
  ├── 每个 KO = EK 图上的簇，声明 aggregation_rule（R1-R4 + 簇内 EK + 边类型）
  └── 簇成立须同时满足：内聚性 / 跨实例性 / 解释范围扩大 / 可命名 / 可回溯
```

**v3.1 铁律**：
- 每个 engineering 对象必须声明 `links`（≥1 条边）——孤立 EK 要么被连接，要么降级 D 级
- 每个 generalized 对象必须声明 `aggregation_rule`——无规则 = 拍脑袋分组，不通过
- generalized 对象必须通过 `derivation.facts` 回溯到 engineering 层（或 Evidence Graph），否则视为"无底座的悬空升维"，不通过。

## 核心字段（必填）

```json
{
  "knowledge_layer": "engineering|generalized",
  "claim": "一句话知识主张",
  "category": "PRODUCT|ARCHITECTURE|ENGINEERING|DESIGN|AGENT|RUNTIME|MEMORY|CONTEXT|PERMISSION|TESTING|EVALUATION|TOOLING|WORKFLOW|DECISION|FAILURE|EXPERIMENT|PATTERN|PRINCIPLE|METHODOLOGY",
  "abstraction": "L0|L1|L2|L3|L4",
  "value": "A|B|C|D|E",
  "provenance": {
    "discovered_by": "code-analyst",
    "supported_by": ["test-analyst", "failure-analyst"],
    "contested_by": ["counterexample-hunter"]
  },
  "epistemic_status": "Fact|Observation|Hypothesis|Validated Pattern|Principle|Law",
  "derivation": {
    "facts": ["EV-001", "EV-004"],
    "observations": [],
    "patterns": [],
    "models": [],
    "promotion_arguments": ["L2→L3: 论证块（new explanatory power / evidence / scope validity）"]
  },
  "evidence": {
    "supporting": ["EV-001", "EV-004"],
    "contradicting": ["EV-012"]
  },
  "flows": {
    "control": "...",
    "state": "...",
    "data": "...",
    "evidence": "...",
    "authority": "...",
    "memory": "...",
    "policy": "..."
  },
  "flow_traceability": {
    "l1_facts_to_edges": [
      {"l1_fact": "approval 走 Gate", "flow_edge": "F-01: orchestrator.rs:173", "verified": true}
    ]
  },
  "scope": {
    "applies_when": "Agent 系统 / 导出器 / 编辑器内核",
    "does_not_apply_when": "纯 CRUD 应用无此问题"
  },
  "confidence": "high|medium|low",
  "links": [
    {"to": "EK-02", "type": "causal", "direction": "out", "note": "三态决策结果触发修正案持久化"}
  ],
  "aggregation_rule": {
    "rule": "R2", 
    "cluster_eks": ["EK-01", "EK-18", "EK-21"],
    "edges": ["causal: EK-01→EK-18→EK-21"],
    "naming": "为什么这个簇能命名",
    "scope_expansion": "KO claim 比任一成员 EK 解释范围大的论证"
  }
}
```

## knowledge_layer 语义（v3）

| 值 | 层 | 抽象级 | 用途 | 是否需升维 |
|----|----|--------|------|-----------|
| `engineering` | Engineering Knowledge | L0/L1/L2 | 推理原材料 / 无损底座 / 项目如何解决工程问题 | 否（独立价值，不参与升维竞争） |
| `generalized` | Generalized Knowledge | L3/L4/L5 | 可迁移认知 / Pattern / Model / Methodology | 是（须过 Abstraction Promotion Gate） |

**层间关系**：generalized 对象必须能通过 `derivation.facts` 回溯到 engineering 层（或 Evidence Graph），否则视为"无底座的悬空升维"，不通过。

**Engineering Knowledge 允许的形态**（v3 新增，不要求完整五层链）：
- 核心机制（服务如何工作）
- 关键实现（实现 pattern）
- 关键决策（为什么这样设计）
- 失败与修复（踩坑/修复/回退）
- 测试揭示的行为（测试暴露的边界）
- 重要配置（关键配置项）
- 边界与例外（适用/不适用条件）

每条 Engineering Knowledge 至少具备：`claim`（具体问题）+ `source`（锚定符号）+ `detail`（实现说明）+ `scope`（边界）+ **`links`（≥1 条边，指向相关 EK，见 ek-graph-schema.md）**。

## 可选字段（有则填，无为填而填）

```json
{
  "disputes": [
    {"claim_by": "code-analyst", "counter_by": "counterexample-hunter", "resolution": "CONDITIONAL"}
  ],
  "validation": {
    "truth": "PASS|FAIL|PARTIAL",
    "coverage": "PASS|FAIL",
    "abstraction": "OK|OVER-ABSTRACTED|UNDER-JUSTIFIED",
    "counterexample": "none|found(详情)",
    "counterexample_budget": {"required": 3, "attempted": 3, "searched_paths": ["bypass", "admin", "test-only"]},
    "blind_reconstruction": "performed|not_performed"
  }
}
```

## 铁律

- `provenance` 是核心：必须知道谁发现、谁支持、谁反对（来自 protocols/evidence-provenance.md）
- `epistemic_status` 必须诚实：Hypothesis 不能写成 Validated Pattern
- `contradicting` 证据**不能删除**，只能通过 `disputes` 记录化解结果
- Abstraction 超过 L3 必须有 `validation.abstraction == OK`（解释范围扩大已论证，且由 abstraction-auditor 独立判定）
- **v2 新增**：`flow_traceability` 必须非空——L1 事实必须能回溯 Flow Edge，否则 KO 不通过 Flow→KO 交叉校验门
- **v2 新增**：`validation.blind_reconstruction` 必须为 performed，否则该 KO 的验证结果无效
- **v3 新增**：`knowledge_layer` 必须显式声明——默认不是 generalized；engineering 对象不强行升维，generalized 对象必须有底层底座可回溯
