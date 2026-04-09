# Meta Ads Optimization Engine


Rule-driven Meta 广告诊断与优化建议服务，基于 FastAPI 提供 REST 接口，结合 YAML 规则、Pydantic 校验与 320 条验证用例打造“规则、数据、测试”三位一体的买量诊断流程。

## 🌟 项目亮点

- **类型安全**：使用 Pydantic V2 定义输入输出模型，自动进行数据校验和文档生成
- **规则驱动**：YAML 配置的规则引擎，支持复杂条件匹配和优先级排序
- **完整指标**：自动计算 CTR、LPV、AddToCart、Checkout、Purchase、CPA、ROAS 等核心指标
- **可扩展性**：模块化架构，支持轻松添加新规则和指标
- **测试完备**：320 条测试用例确保规则准确性和系统稳定性
- **API 友好**：提供 RESTful 接口，支持批量分析和规则管理

## 🚀 快速开始

### 环境要求

- Python 3.11+
- pip

### 安装与启动

```bash
# 克隆项目
git clone git@github.com:yifengyiye/meta_ads_optimization_engine.git
cd meta_ads_optimization_engine 

# 创建虚拟环境
python -m venv .venv

# 激活环境（Windows）
.venv\Scripts\activate

# 安装依赖
pip install -e .[dev]

# 启动服务
uvicorn app.main:app --reload
```

## 📖 使用指南

### API 接口

- **健康检查**：`GET /health` - 查看服务状态和规则版本
- **规则列表**：`GET /rules` - 获取所有启用的规则
- **批量分析**：`POST /analyze` - 提交广告数据进行诊断和优化建议

### 示例请求

```bash
curl -X POST "http://127.0.0.1:8000/analyze" -H "Content-Type: application/json" -d '{
  "records": [
    {
      "date": "2024-01-01",
      "account_id": "acc_test_001",
      "campaign_id": "camp_test_001",
      "adset_id": "adset_test_001",
      "ad_id": "ad_test_001",
      "spend": 100.0,
      "impressions": 10000,
      "clicks": 40,
      "link_clicks": 35,
      "landing_page_views": 30,
      "add_to_cart": 5,
      "initiate_checkout": 3,
      "purchases": 1,
      "revenue": 200.0
    }
  ]
}'
```

## 🛠️ 开发与测试

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_rule_engine.py -v

# 生成测试用例
python scripts/generate_320_test_cases.py

# 分析失败案例
python scripts/analyze_failures.py

# 批量验证规则
python scripts/batch_validation.py
```

### 添加新规则

1. 在 `app/rules/meta_rules.yaml` 中添加规则定义
2. 更新 `scripts/generate_320_test_cases.py` 中的测试数据生成逻辑
3. 运行测试确保规则正确匹配

## 📁 项目结构

```text
meta_optimization_engine/
├── app/                     # 主应用目录
│   ├── config.py           # 配置管理
│   ├── main.py             # FastAPI 应用入口
│   ├── routes.py           # API 路由定义
│   ├── schemas/           # 数据模型定义
│   ├── rules/             # 规则配置和加载器
│   ├── services/          # 业务逻辑服务
│   └── utils/             # 工具函数
├── scripts/               # 辅助脚本
│   ├── generate_320_test_cases.py    # 生成测试用例
│   ├── analyze_failures.py           # 分析失败案例
│   ├── batch_validation.py           # 批量验证
│   └── run_engine_demo.py            # 演示脚本
├── tests/                 # 测试目录
│   ├── test_metrics.py    # 指标计算测试
│   ├── test_rule_engine.py # 规则引擎测试
│   ├── test_recommendations.py # 推荐服务测试
│   ├── test_api.py        # API 测试
│   └── test_batch_cases.py # 批量用例测试
├── test_data/             # 测试数据
├── test_output/           # 测试输出
├── pyproject.toml         # 项目配置和依赖
├── README.md             # 项目说明
├── CONTRIBUTING.md       # 贡献指南
├── DEMO_RUN_GUIDE.md     # 演示指南
└── LICENSE               # MIT 许可证
```

## 🤝 贡献指南

欢迎为项目贡献代码、规则或文档！请参考 [CONTRIBUTING.md](./CONTRIBUTING.md) 了解详细的贡献流程。

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](./LICENSE) 文件。
