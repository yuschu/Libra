# Libra

城市交通运行数据**可视化分析 · 流量预测 · 拥堵预警**系统。

后端 FastAPI + SQLite，前端 ECharts 大屏，预测用 Prophet / XGBoost。

## 一键运行（Windows）

1. 双击 **`setup.bat`**：建虚拟环境、装核心依赖、导入示例数据（仅首次）。
2. 双击 **`run.bat`**：启动后端，并自动打开演示大屏。
3. 接口文档：<http://127.0.0.1:8000/docs>

> 预测依赖（prophet / xgboost）较大，需要预测功能时再：
> `backend\.venv\Scripts\pip install -r backend\requirements-ml.txt`

## 技术栈

| 层 | 选型 |
|---|---|
| 后端 | Python · FastAPI · Uvicorn |
| 存储 | SQLite（开发），可换 MySQL |
| 前端 | ECharts 5 大屏（后续迁 Vue / GoView） |
| 预测 | Prophet（在线）· XGBoost / LibCity（离线实验） |

## 目录结构

```
Libra/
├── backend/
│   ├── app/main.py              # FastAPI 入口与路由
│   ├── app/ingestion/load.py    # CSV 导入 SQLite（幂等）
│   ├── requirements.txt          # 核心依赖
│   └── requirements-ml.txt      # 预测依赖（按需）
├── data/
│   ├── traffic_sample.csv       # 示例数据（7天×24h×3路段）
│   └── gen_sample.py           # 示例数据生成脚本
├── web-screen/index.html         # 演示大屏
├── setup.bat / run.bat          # 一键脚本
└── AGENTS.md                     # AI 编码（opencode/ECC）开发说明与铁律
```

## 现有接口（/api/v1，统一返回 {code, message, data}）

- `GET /api/v1/stats/overview` —— 总流量、平均速度、路段数
- `GET /api/v1/traffic/flows?road_id=R001` —— 某路段最近 24h 流量

## 数据

- SQLite：`backend/traffic.db`（不入库）
- 表 `traffic_flow(dt, road_id, flow, avg_speed, density, weather)`，索引 `(road_id, dt)`
- 重新导入：`python backend/app/ingestion/load.py`

## 开发说明

用 opencode / ECC 开发时，根目录 `AGENTS.md` 是完整上下文与铁律：
**每完成一个动作必须 `git add . → commit → push`**。

## 路线图

1. 大屏加路段下拉切换、时段×星期拥堵热力图
2. Prophet 流量预测接口（离线训练、在线推理）
3. 事故表与黄/橙/红分级预警
4. 管理后台（用户、预警规则）
