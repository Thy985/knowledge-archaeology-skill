# Rulesets 配置指南（knowledge-archaeology-skill）

> 更新：2026-09-03 — 规则集已通过 API 成功创建并验证。

## 一、GitHub 已生效配置（2026-09-03 实测）

### 1. 分支保护 `main`（API 已配）
- `required_status_checks`：**strict=true**，3 个 CI check 强制：
  - `Layers 1/2/3/5 (Contract · Deterministic · Regression · Mutation)`
  - `Layer 4 · Benchmark + Quality Gate`
  - `Quality Gate (all 5 layers)`
- `allow_force_pushes: false` / `allow_deletions: false`
- `enforce_admins: false`（owner 不受分支保护限制）

### 2. Ruleset（2 个，API 已建）

| id | 名称 | enforcement | rules | bypass |
|----|------|-------------|-------|--------|
| 22186480 | Main + High-Risk: PR + CI + No Force Push/Delete | active | pull_request + non_fast_forward + deletion | owner(User, always) |
| 22186481 | High-Risk Paths: PR + CI Mandatory | active | pull_request + deletion | owner(User, always) |

> 注：GitHub 的 `GET /rulesets` 列表接口不返回 `rules` 明细（显示空数组），但创建接口已确认实际规则生效。

## 二、关键排错结论（踩坑记录）

### 1. `pull_request` rule 必须带全全部 Required 参数
只传 `required_approving_review_count` 会 422 `Invalid property /rules/0`。必须同时提供：
```json
{
  "type": "pull_request",
  "parameters": {
    "required_approving_review_count": 0,
    "dismiss_stale_reviews_on_push": false,
    "require_code_owner_review": false,
    "require_last_push_approval": false,
    "required_review_thread_resolution": false,
    "allowed_merge_methods": ["merge", "squash"]
  }
}
```

### 2. `bypass_actors` 必须用 `User` 类型 + 用户 ID
- `RepositoryRole` + user_id → 422 `Invalid bypass actor`
- `Team` + user_id → 422 `Actor team must be part of the ruleset source`
- ✅ `User` + user_id → 成功
```json
"bypass_actors": [{"actor_id": 242532545, "actor_type": "User", "bypass_mode": "always"}]
```

### 3. `file_path_restriction` condition → **GitHub API 500（服务端 bug）**
- 无论路径格式（`rules/**` / `/rules/**` / `**/rules/**` / 空数组）一律 500
- **结论**：当前 GitHub API 版本对 `conditions.file_path_restriction` 返回 500，无法通过 API 创建路径级规则集
- **替代**：
  a. 在网页 UI `Settings → Rules` 手动添加文件路径条件（UI 走内部通道，可能可用）
  b. 依赖现有保护：分支保护已强制 PR+CI，workflow `progressive-autonomy` 已按 `rules/risk-paths.json` 对高风险路径禁止自动合并
- `ruleset-highrisk.json` 当前为分支级版本（无路径条件）；如需路径级，在网页上给该规则集添加 File path restrictions（清单见下）

## 三、高风险路径清单（网页添加路径条件时用）

```
agents/**
contracts/**
workflows/**
protocols/promotion*
protocols/escalation*
protocols/disagreement*
protocols/blind-reconstruction*
rules/**
tools/ka_engine.py
```

## 四、最终保护架构

```
┌─────────────────────────────────────────────────────────┐
│ 分支保护 main（API）                                     │
│   PR 必须过 3 个 CI check（strict）                       │
│   禁 force push / 禁删除                                 │
├─────────────────────────────────────────────────────────┤
│ Ruleset 1 · Main + High-Risk（API）                     │
│   pull_request + non_fast_forward + deletion            │
├─────────────────────────────────────────────────────────┤
│ Ruleset 2 · High-Risk Paths（API，分支级）               │
│   pull_request + deletion（可网页加路径条件升级为路径级） │
├─────────────────────────────────────────────────────────┤
│ workflow · progressive-autonomy（软件层）                │
│   low-risk → 自动合并                                   │
│   medium/high → 不自动合并，人工 Gate                   │
└─────────────────────────────────────────────────────────┘
```
