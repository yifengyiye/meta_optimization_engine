# Contributing

欢迎为 Meta Optimization Engine 贡献：规则、测试用例、文档或 API 改进。请按以下流程操作：

1. **Fork & branch**：在 GitHub 上 fork 本仓库，任何 feature/bugfix 用 `git checkout -b feature/<short>`。
2. **更新依赖**：创建虚拟环境 `.venv`、激活后 `pip install -e .[dev]`，确保所有命令在该环境中执行。
3. **修改规则/代码**：
   - 规则只写在 `app/rules/meta_rules.yaml`，新条目同步更新 `meta_ads_metrics_threshold_actions_table.md`、`scripts/generate_320_test_cases.py`。
   - 调整推荐逻辑请同步更新 `app/services/recommendation_service.py` 相关排序/优先级。
4. **生成/验证测试数据**：
   - `python scripts/generate_320_test_cases.py` → 更新 `test_data/*.json|.csv`；
   - `python scripts/analyze_failures.py` → 快速定位“期望→实际”组合；
   - `python scripts/batch_validation.py` → 确保 320 案例通过；
   - `pytest` → 覆盖 metrics、rule engine、recommendation、API。
5. **提交说明**：编写清晰的 commit message，说明改动缘由与范围，引用相关 issue/entry（如有）。
6. **Pull Request**：提交 PR 前请确保过所有测试，CI 将自动执行上述批量验证，PR 描述应包含变更总结和验证步骤。

有问题请在 issue 里描述复现步骤与日志，我们会尽快协助。
