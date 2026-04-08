# 架构与数据流概览

## 核心层级

- **入口层**：`app/main.py`  创建 FastAPI 实例；`app/routes.py` 暴露三个端点 `GET /health` `GET /rules` `POST /analyze`，`AnalyzeRequest` 通过 `AdRecord` 强类型校验。  
- **服务层**：`RecommendationService`（`app/services/recommendation_service.py`）串联 ingestion、normalization、metric、rule engine、rule loader 并在 `analyze()` 返回 `AnalyzeResponse`。  
- **规则&逻辑**：`RuleLoader` 读取 `app/rules/meta_rules.yaml` → `RuleEngine` 逐条件匹配 → 输出 `MatchedRuleResult`；动作由 `_action_priority` + `priority_score` 决定 `primary_action`，并生成带指标片段的 `diagnosis_summary`。

## 数据 & 指标

- `MetricService` 产生 CTR/CPC/CPM、LPV/AddToCart/Checkout/Purchase、CPA/ROAS/AOV、保存/分享/评论率、视频表现、疲劳/异常等字段；同时标记 `sample_size_ok`、`creative_fatigue_risk`、`data_anomaly_suspected`，规则可直接用作条件。  
- `NormalizationService` 补全 `frequency` 与 `average_order_value`，保证指标计算不会因空值失败。  
- `RuleEngine` 支持 `lt`/`lte`/`gt`/`gte`/`eq`/`neq`/`between`/`in`/`not_in`/`is_true`/`is_false`，便于在 YAML 中描述任意组合判断。

## 规则维护与校验闭环

1. `meta_ads_metrics_threshold_actions_table.md` 描述“指标异动 → 优化动作”表格，作为策略明细。  
2. `scripts/generate_320_test_cases.py` 读取该表、用 `AdRecord` 模板构建 320 条测试输入，`isolate_for_expected_action` 确保每条案例只以期望动作为主。  
3. `test_data/meta_ads_320_test_cases.{json,csv}`：测试数据供 `pytest`、`scripts/batch_validation.py` 与 `scripts/analyze_failures.py` 共享。  
4. `scripts/analyze_failures.py` 聚焦 “实际 vs 预期” 组合，并写入 `test_output/failures.json` 以便追踪常见误判。  
5. `scripts/batch_validation.py` 每次规则更新后运行，确认 320 条用例的 `primary_action` 仍在兼容动作集合内。

## 测试与演示

- `tests/` 包含 metrics、rule engine、recommendation service、FastAPI（TestClient）、320 条批量参数化等单元/集成。  
- `scripts/run_engine_demo.py` 构造单条 `AdRecord`，可直接在 CLI 下验证规则输出；配合 `sample_payload.json` 与 `sample_expected_output.json` 可提供 demo 页面或 Postman 参考。  
- `DEMO_RUN_GUIDE.md` 记录了一系列推荐的交互顺序（生成数据 → 运行 demo → 批量校验），方便新人上手。

## 开源准备

- `README.md` 里已替换为多节指南（启动、运行、验证、规则协作、贡献）。  
- 新增 `CONTRIBUTING.md` 说明 fork/branch/workflow/testing/validation 流程。  
- 建议添加 `LICENSE`（如 MIT）与 `.github/ISSUE_TEMPLATE`（可后续补充）以完成开源仓库基础设施。
