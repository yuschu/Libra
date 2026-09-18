# Libra — 给 AI 编码工具（opencode）的开发说明书

> 本文件是你接手本项目的唯一上下文。开始任何改动前先读完，并严格遵守文末「铁律」。

## 一、项目是什么
Libra 是一个城市交通运行数据**可视化分析 + 流量预测 + 拥堵预警**系统（专科毕业设计）。
当前阶段：起步骨架已跑通（FastAPI 后端 + SQLite + ECharts 演示页），正在逐步加功能。

## 二、技术栈
- 后端：Python 3.10+ / FastAPI / Uvicorn / SQLite（开发），演示期可换 MySQL
- 数据：Pandas，标准库 sqlite3
- 前端：`web-screen/index.html`（当前用 ECharts CDN 的演示页，后续再迁 Vue/GoView）
- 预测：在线 Prophet；离线实验用 LibCity、XGBoost
- Git 远程：https://github.com/yuschu/Libra.git （主分支 `main`）

## 三、傻瓜式一键运行（Windows）
1. 双击 **`setup.bat`**：自动建虚拟环境、装依赖、导入示例数据（只需第一次跑）。
2. 双击 **`run.bat`**：启动后端，并自动打开演示页。
3. 接口文档自动生成：浏览器访问 http://127.0.0.1:8000/docs
4. 预测相关依赖（prophet/xgboost）较大，需要时再 `pip install -r requirements-ml.txt`。

## 四、目录结构
```
Libra/
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI 入口与路由
│   │   ├── ingestion/load.py # CSV 导入 SQLite（幂等）
│   │   ├── core/ routers/ services/ models/ schemas/  # 待扩展
│   ├── .venv/                 # 虚拟环境（不入库）
│   ├── requirements.txt       # 核心依赖
│   └── requirements-ml.txt    # 预测依赖（按需装）
├── data/
│   ├── traffic_sample.csv    # 示例数据（7天×24h×3路段）
│   └── gen_sample.py          # 示例数据生成脚本
├── web-screen/index.html      # 演示大屏
├── setup.bat / run.bat        # 一键脚本
└── README.md
```

## 五、数据库与数据
- SQLite 文件：`backend/traffic.db`（**不入库**）
- 表 `traffic_flow(dt, road_id, flow, avg_speed, density, weather)`，索引 `(road_id, dt)`
- 重新导入数据：`python backend/app/ingestion/load.py`

## 六、现有接口（统一前缀 /api/v1，返回 {code,message,data}）
- `GET /api/v1/stats/overview`：总流量、平均速度、路段数
- `GET /api/v1/traffic/flows?road_id=R001`：该路段最近 24 小时流量

## 七、铁律（每次动作完成后必须执行）
**每完成一个改动，必须提交并推送，不允许只改不推：**
```bash
git add .
git commit -m "简明描述这次改了什么"
git push
```
提交信息用中文短句即可，一次动作一个 commit。

## 八、不能做的事
- 不要提交 `.venv/`、`*.db`、`.env`、`__pycache__/`（已在 .gitignore）
- 时间序列数据**必须按时间先后切分**训练/测试集，禁止随机 shuffle（会数据泄漏）
- 模型**离线训练、在线只推理**；预测结果存库，不要每次请求现跑
- 新增接口统一走 `/api/v1`，返回统一响应体
- 不要把密钥、token 写进代码

## 九、下一步待办（按顺序做，做一步推一步）
1. 大屏加「路段下拉切换」和「时段×星期拥堵热力图」
2. 接入 Prophet：新增 `POST /api/v1/predictions/flow`，离线训练、在线推理
3. 事故表 accident 与分级预警（黄/橙/红）
4. 管理后台（用户、预警规则）
