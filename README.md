# Meta Optimization Engine

Rule-driven Meta 广告诊断与优化建议服务，基于 FastAPI 提供 REST 接口，结合 YAML 规则、Pydantic 校验与 320 条验证用例打造“规则、数据、测试”三位一体的买量诊断流程。

## 亮点

- Pydantic 定义 `AdRecord`/`AnalyzeRequest` 输入模型，自动校验上传的 JSON；
- `MetricService` 派生 CTR、LPV、AddToCart、Checkout、Purchase、CPA、ROAS、疲劳/异常等指标；
- `RuleLoader` + `RuleEngine` 以 YAML 条件驱动、排序 + 去重再生成 `primary_action` 与 `diagnosis_summary`；
- 支持 `GET /rules`、`POST /analyze`、`GET /health`（看待系统与规则版本）；
- 一套 `scripts/generate_320_test_cases.py → scripts/analyze_failures.py → scripts/batch_validation.py` 形成规则回归闭环。

## 快速启动（推荐）

```bash
cd D:\agent\meta_agent\meta_optimization_engine
python -m venv .venv
.venv\Scripts\activate
pip install -e .[dev]
uvicorn app.main:app --reload
```

访问 `http://127.0.0.1:8000/docs` 查看自动化 OpenAPI。

## 运行与验证命令

- **启动服务**：`uvicorn app.main:app --reload`  
- **生成 320 条规则测试记录**：`python scripts/generate_320_test_cases.py`  
- **分析当前失败组合**：`python scripts/analyze_failures.py`（结果保存在 `test_output/failures.json`）  
- **批量验证规则匹配**：`python scripts/batch_validation.py`（会输出 `passed/failed` 与样例 failure）  
- **运行所有 pytest**：`pytest`（包含 metrics、rule engine、recommendation、批量用例等）

## 项目结构概览

```text
meta_optimization_engine/
  app/
    config.py     # Settings、规则路径
    main.py       # FastAPI 实例
    routes.py     # /health /rules /analyze
    schemas/       # Input/Output/Rule 模型
    rules/         # meta_rules.yaml + loader
    services/      # ingestion/normalization/metric/rule/recommendation
    utils/         # 辅助工具
  scripts/
    generate_320_test_cases.py  # 针对指标表生成样例
    analyze_failures.py         # grouping failure combos
    batch_validation.py         # 320 条完整回归
    run_engine_demo.py          # 简易演示调用
  tests/            # 单元/集成（metrics、rule engine、recommendation、API、批量）
  test_data/        # JSON + CSV 320 case 基准
  test_output/      # 分析/失败记录
  README.md         # 启动 + 介绍
  DEMO_RUN_GUIDE.md # 演示流程
```

## 规则协作指南

1. 所有规则写在 `app/rules/meta_rules.yaml`，通过 `RuleLoader` 加载；新增规则时同步更新 `meta_ads_metrics_threshold_actions_table.md` + `scripts/generate_320_test_cases.py` 中的描述并重建测试 JSON/CSV。
2. 规则优先级由 `priority_score` 决定，`RecommendationService` 会按动作优先级（比如 `FIX_TRACKING/FIX_PAYMENT` > `PAUSE` > `OBSERVE`）挑选最终 action。
3. 调整规则后，务必执行 `python scripts/generate_320_test_cases.py` → `python scripts/analyze_failures.py` → `python scripts/batch_validation.py` → `pytest`，确保新逻辑与 320 条用例以及现有接口同步。

## 贡献

请参考 [CONTRIBUTING.md](./CONTRIBUTING.md)（新增）了解如何报 issue、fork、分支、提交、测试与 PR。

