# Benchmark Workflow（基准测试）— v3.1

> 用已完成考古的项目验证 skill 本身的质量。回答：这个 skill 真的比上一版产出更多/更准吗？
> v2 新增：**以 benchmarks/codex/ 的 v1 基线为锚，度量 v1→v2 的真实变化。**
> v3 新增：**三层知识架构配比度量**——验证 v3 是否克服"过度压缩"（只保留 KO 丢弃工程知识）。
> v3.1 新增：**EK Graph 度量**——验证工程知识层是否从"扁平清单"升级为"有边连接的图"，KO 是否从"手工分组"升级为"规则聚合"。

## 触发

- 新版本 skill 发布后（v3.1 发布 → 用 Codex 重跑对比）
- 用户要求检验 skill 效果
- 用新架构对已考古项目重跑（如 Tafcm / Codex）

## 方法

对同一项目跑两遍（v3 vs v3.1），对比：

| 维度 | v3 基线 | v3.1 | 说明 |
|------|---------|------|------|
| Generalized KO 数 | 8（Codex）| ? | 数量不是目标，覆盖质量才是 |
| Engineering Knowledge 数 | 52（Codex）| ? | 宽底座是否保持 |
| **EK 平均出边数** | 0（扁平清单）| ? | **每条 EK 是否有 links（≥1 合格）** |
| **游离 EK 比例** | 100%（无图）| ? | **无边 EK / 总数（<20% 合格）** |
| **聚合规则覆盖率** | 0%（无规则）| ? | **有 aggregation_rule 的 KO / 总数（=100%）** |
| **KO 平均簇规模** | 无 | ? | derivation.facts 数（3~12 健康） |
| **假聚合比例** | 无 | ? | "同子系统=聚合理由"的 KO 数 |
| 三层配比 | Facts:100 : EK:52 : KO:8 | ? | 宽底座+窄尖顶是否保持 |
| KO 底座可回溯率 | 100% | ? | generalized 能否回溯到 engineering 底座 |
| False Acceptance | ? | ? | Validator 误放行比例 |
| Critical Missing | ? | ? | 高密度子系统遗漏数 |
| Fact Error | ? | ? | KO 引入不存在事实数 |
| Over-generalization | ? | ? | 过度升维比例 |
| Counterexample Found | ? | ? | 反例检测数 |
| Blind Reconstruction | 强制 | 强制 | Validator 独立盲重建执行率 |

## v1 基线（已完成，见 `benchmarks/codex/（基准演进归档，独立存放）`）

- `extraction-v1/`：v1 考古原产物（6 文件）
- `independent-audit-v1/`：独立对抗验证（10 文件）
- `failure-analysis.md`：失败分析（三个结论 + 三个遗漏 + 43% 信号）
- `lessons-for-v2.md`：F1-F6 设计需求 + Policy Flow 第七类流
- **`extraction-v2/`**：v2 考古原产物（3 波，7 KO）——v3 对比基线
- **`lessons-for-v3.md`**（待创建）：v3 升级蓝图——三层知识架构 / 宽底座窄尖顶 / 工程知识层独立保留

## 测量指标

1. **增量发现**：新架构发现旧架构遗漏的知识（如 exec_policy / 上下文治理 / 策略固化）
2. **反例质量**：Counterexample Hunter 找到的有效反例（能把 claim 条件化）——对比 v1 声称的 0
3. **降级有效性**：Abstraction Promotion Gate 阻止的过度升维（对比 v1 的 KO-03 过度升维）
4. **冲突价值**：Reconciler 产出的 CONDITIONAL 知识数量
5. **证据支撑**：Knowledge Object 中 ≥2 独立源支撑的比例
6. **盲重建有效性**：Validator 独立发现 Miner 事实错误/遗漏的次数
7. **v3 三层配比**：Engineering Knowledge 层是否建立（数量/覆盖/保留完整度）；Generalized KO 底座可回溯率
8. **v3.1 EK Graph**：EK 平均出边数（≥1 合格）；游离 EK 比例（<20% 合格）；聚合规则覆盖率（=100%）；KO 平均簇规模（3~12 健康）；假聚合（"同子系统"式理由）KO 数（=0）

## 反例压力测试（推荐实验）

对已有 P 原则做 Counterexample Hunter 压力测试：
- Claim: "所有 execution 都经过 authorization gate"
- 搜索：bypass / admin path / direct call / test path / override / legacy path
- 结果：claim 条件化 or 维持（必须记录 searched_paths）

## 基准报告格式

```
Project: <name>
Version: <skill version>  （对比 v3 基线）
结果:
  三层配比: Facts:N / Engineering:N / Generalized KO:N
  EK 平均出边数: ?（v3: 0 扁平清单）
  游离 EK 比例: ?%（<20% 合格）
  聚合规则覆盖率: ?%（=100% 合格）
  KO 平均簇规模: ?（3~12 健康）
  假聚合 KO 数: ?（"同子系统"式理由）
  Engineering Knowledge 覆盖: 核心机制?/实现?/决策?/失败?/配置?/边界?
  KO 底座可回溯率: ?%
  False Acceptance: ?%（v3: ?）
  Critical Missing: ?（v3: ?）
  Fact Error: ?（v3: ?）
  Over-generalization: ?%（v3: ?）
  反例发现: N 个
  降级次数: N（阻止了 M 次过度升维）
  冲突化解: N 个 CONDITIONAL
  盲重建发现: N 次
  证据支撑: X% 对象 ≥2 独立源
结论: v3.1 是否达成改进目标（EK 从扁平清单升级为图 / KO 从手工分组升级为规则聚合）
```
