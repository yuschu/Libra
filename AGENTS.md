# Libra — 给 AI 编码工具（opencode / ECC）的开发说明书

> 本文件是你接手本项目的唯一上下文。开始任何改动前先读完，并严格遵守「铁律」。

## 一、项目是什么
Libra 是一个城市交通运行数据**可视化分析 + 流量预测 + 拥堵预警**系统（专科毕业设计）。
数据涵盖：流量、平均速度、拥堵、事故、车/非机动车类型、交通行为。
当前阶段：起步骨架已跑通（FastAPI 后端 + SQLite + ECharts 演示页），正在逐步加功能。

## 二、技术栈（开源优先、组件化、高兼容）
- 后端：Python 3.10+ / FastAPI / Uvicorn / SQLite（开发），可平滑切换 MySQL
- 数据处理：Pandas；数据预处理做成**可插拔组件**（见第五节）
- 大屏前端：ECharts 5 + DataV（`@jiaminghi/data-v`），可视化编辑器 GoView / datav-vue3
- 管理后台：vue-pure-admin
- 预测：在线 Prophet；离线实验用 LibCity（Bigscity）、XGBoost / scikit-learn
- 轻量与兼容：整体追求**轻量化**，并要能在**老电脑**上跑（见第三节）
- Git 远程：https://github.com/yuschu/Libra.git （主分支 `main`）

## 三、轻量化与老电脑兼容（硬要求）
- 前端保持**轻量静态页**：单页 HTML + ECharts，**ECharts 用本地文件、不走外网 CDN**；不要引入需要 npm 构建的重型前端工程作为主大屏
- 代码用 **ES2015** 写法，兼容旧版 Chromium，不用最新 JS 语法/API，不用强制新版浏览器特性
- 运行环境：老电脑**无需自行安装浏览器**。优先用本机已有浏览器打开；如需"内嵌"，用**便携版 Chromium 内核**启动一个本地页面，**不要用 Electron 整包打包**（体积臃肿，违背轻量化）
- 后端：用 SQLite、少依赖、启动快，不开多余服务；演示机配置低也能流畅跑
- 大屏图表做数据量与动画降级，低配机不卡

## 四、傻瓜式一键运行（Windows）
1. 双击 **`setup.bat`**：建虚拟环境、装核心依赖、导入示例数据（仅首次）。
2. 双击 **`run.bat`**：启动后端，并自动打开演示大屏。
3. 接口文档：http://127.0.0.1:8000/docs
4. 预测依赖较大，需要时再 `pip install -r backend/requirements-ml.txt`。

## 五、数据预处理组件（必须做）
做一个内嵌的预处理组件，把多种来源统一转成标准时序表，再入库：
- 支持格式：CSV / Excel(xlsx) / JSON / REST API 接口
- 输出统一 schema：`dt(时间), road_id, flow, avg_speed, density, weather`，
  事故单独 `accident` 表，车/非车类型与行为用独立维度表
- 职责：编码探测、时间戳对齐、缺失/异常值清洗、单位统一，做成可复用 pipeline
- 新数据源 = 加一个 adapter，不改主流程

## 六、目录结构
```
Libra/
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI 入口与路由
│   │   ├── ingestion/load.py # CSV 导入 SQLite（幂等）
│   │   ├── preprocess/        # 多格式预处理 adapter（待建）
│   │   ├── core/ routers/ services/ models/ schemas/  # 待扩展
│   ├── .venv/                 # 虚拟环境（不入库）
│   ├── requirements.txt       # 核心依赖
│   └── requirements-ml.txt    # 预测依赖（按需）
├── data/
│   ├── traffic_sample.csv      # 示例数据（7天×24h×3路段）
│   └── gen_sample.py           # 示例数据生成脚本
├── web-screen/index.html        # 演示大屏
├── setup.bat / run.bat         # 一键脚本
└── README.md
```

## 七、数据库与数据
- SQLite：`backend/traffic.db`（**不入库**）
- 核心表 `traffic_flow(dt, road_id, flow, avg_speed, density, weather)`，索引 `(road_id, dt)`
- 待建：`accident`（事故）、`vehicle_type`（车/非机动车类型）、`behavior`（交通行为）
- 重新导入：`python backend/app/ingestion/load.py`

## 八、接口规范（统一、兼容、组件化）
- 统一前缀 `/api/v1`，版本号进 URL，便于将来升级
- 统一响应体：`{ "code": 0, "message": "ok", "data": ... }`，错误 code 非 0
- 鉴权：管理后台接口走 **JWT**（登录发 token，后续接口带 `Authorization: Bearer <token>`）
- 分页：列表接口统一参数 `page`、`page_size`，返回 `{ list, total, page, page_size }`
- 现有接口：
  - `GET /api/v1/stats/overview` —— 总流量、平均速度、路段数
  - `GET /api/v1/traffic/flows?road_id=R001` —— 某路段最近 24h 流量

## 九、铁律（每次动作完成后必须执行）
**每完成一个改动，必须提交并推送，不允许只改不推：**
```bash
git add .
git commit -m "简明描述这次改了什么"
git push
```
提交信息用中文短句，一次动作一个 commit。

## 十、不能做的事
- 不要提交 `.venv/`、`*.db`、`.env`、`__pycache__/`（已在 .gitignore）
- 时间序列**必须按时间先后切分**训练/测试集，禁止随机 shuffle（数据泄漏）
- 模型**离线训练、在线只推理**；预测结果存库，不要每次请求现跑
- 新增接口走 `/api/v1`，遵守第八节响应体/JWT/分页规范
- 不要把密钥、token 写进代码；不要为了省事跳过预处理直接塞脏数据
- 不要用 Electron 整包打包；不要让前端依赖外网 CDN

## 十一、30 周开发里程碑（参考，做一步推一步）
- 第 1–4 周：骨架、数据库、预处理组件、基础可视化闭环
- 第 5–10 周：大屏（路段切换、拥堵热力、事故/车非车类型图表）
- 第 11–18 周：Prophet/XGBoost 预测接口 + 模型评估
- 第 19–24 周：分级预警（黄/橙/红）+ JWT 管理后台
- 第 25–30 周：联调、写论文实现/测试章节、部署与答辩

## 十二、下一步待办（按顺序做，做一步推一步）
1. 大屏加「路段下拉切换」和「时段×星期拥堵热力图」
2. 建 `preprocess/` 多格式预处理组件
3. 接入 Prophet：`POST /api/v1/predictions/flow`，离线训练、在线推理
4. 事故表 `accident` 与分级预警（黄/橙/红）
5. JWT 登录 + 管理后台（用户、预警规则）
