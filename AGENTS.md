# Libra — 给 AI 编码工具（opencode / ECC）的开发说明书

> 本文件是你接手本项目的唯一上下文。开始任何改动前先读完，并严格遵守「铁律」。

## 一、项目是什么
Libra 是一个城市交通运行数据**可视化分析 + 流量预测 + 拥堵预警**系统，按生产级项目标准开发。
数据涵盖：流量、平均速度、拥堵、事故、车/非机动车类型、交通行为。
当前阶段：起步骨架已跑通（FastAPI 后端 + SQLite + ECharts 演示页），正在逐步加功能。

## 二、技术栈（开源优先、组件化、高兼容）
- 后端：Python 3.10+ / FastAPI / Uvicorn / SQLite（开发），可平滑切换 MySQL
- 数据处理：Pandas；数据预处理做成**可插拔组件**（见第五节）
- 大屏前端：完整可视化大屏（Vue + GoView/datav-vue3 + DataV + ECharts 5），**面向非专业人员展示，视觉效果优先**
- 管理后台：vue-pure-admin，**只做最小集**（登录 + 预警规则配置），结构参考 RuoYi-Vue-FastAPI；**不做完整 RBAC/角色/菜单权限体系**，避免喧宾夺主
- 预测：在线 Prophet（**必须做、是核心**）；XGBoost / LibCity 为加分项，Prophet 跑通是底线，LibCity 配置不通可跳过
- 轻量与兼容：整体追求**轻量化**，并要能在**老电脑**上跑（见第三节）
- Git 远程：https://github.com/yuschu/Libra.git （主分支 `main`）

## 三、面向非专业人员演示（展示优先）
- 这是给**非专业人员**看的：视觉效果、完整度、"一看就懂"优先，**不再为兼容老电脑砍功能**，按完整方案做
- 大屏用完整方案（Vue / GoView），可上大屏风格、地图、动效
- 非专业人员**无需装环境、无需懂命令**：做到一键启动；最终可打包成可执行程序（如 Electron）双击即看
- 仍要求：不依赖外网（演示现场没网也能跑），界面直观友好、不暴露代码和命令行
- 性能适度即可：别因数据量过大明显卡顿，不强制做低配降级

## 四、傻瓜式一键运行与数据初始化（Windows）
1. 双击 **`setup.bat`**：建虚拟环境、装核心依赖（仅首次），**不自动灌示例数据**。
2. 双击 **`run.bat`**：启动后端并打开界面。
3. 接口文档：http://127.0.0.1:8000/docs
4. 预测依赖较大，需要时再 `pip install -r backend/requirements-ml.txt`。

### 数据初始化与空态交互（必须做）
- **启动后让用户选**：首次进入界面时弹窗/引导二选一——「使用示例数据」或「导入我的数据」，不要默认直接用示例数据
- **无数据时空态提醒**：数据库为空时，大屏弹明确提示「暂无数据，请选择示例数据或导入数据」，图表显示空状态而非报错
- **一键清空**：提供「清空已导入数据」按钮，一键删除所有业务数据并回到空态
- 选「示例数据」即一键灌入示例；选「导入」走第五节上传页

## 五、数据预处理组件（必须做，且要傻瓜式）
做一个内嵌的预处理组件，把多种来源统一转成标准时序表，再入库。**非专业人员不用写代码、不用跑命令**：
- 网页上传入口：浏览器里选文件 → 点上传即可，自动完成识别、清洗、入库
- 支持格式：CSV / Excel(xlsx) / JSON / REST API 接口
- 自动识别列含义（哪列是时间、哪列是路段、哪列是流量/速度），识别不准时让用户下拉确认映射
- 输出统一 schema：`dt(时间), road_id, flow, avg_speed, density, weather`；事故单独 `accident` 表，车/非车类型与行为用独立维度表
- 自动清洗：编码探测、时间戳对齐、缺失/异常值处理、单位统一，做成可复用 pipeline
- 反馈友好：上传后显示成功/失败、导入条数、跳过了哪些坏行；可查看已导入数据、重复导入自动去重
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
- 不要让前端依赖外网 CDN（演示现场需离线可用）

## 十一、工程质量、日志与豆包监督（必须做）
- 结构化日志：用 Python `logging` 写文件到 `logs/`，记录每次请求/任务的时间、动作、入参、结果、报错；不要只 `print` 到控制台
- 配置走 `.env`（提供 `.env.example`），路径/端口/密钥不硬编码
- 安全：配置 CORS 白名单；SQL 一律参数化查询防注入；接口入参做校验
- 关键接口（stats / flows / predictions）写最小接口测试
- **豆包监督机制**：
  1. opencode 每完成一个动作必须 `git add . → commit → push`，commit message 写清改了哪些文件、做了什么；
  2. 每次 push 后，由豆包（人工监督方）执行 review：`git log` 看本次改动、跑 `run.bat` 验证接口通、检查是否违反本说明书铁律；
  3. review 不通过就打回，让 opencode 修正后重新提交，**未通过 review 不得进入下一步**。

## 十二、30 周开发里程碑（参考，做一步推一步）
- 第 1–4 周：骨架、数据库、预处理组件、基础可视化闭环
- 第 5–10 周：大屏（路段切换、拥堵热力、事故/车非车类型图表）
- 第 11–18 周：Prophet/XGBoost 预测接口 + 模型评估
- 第 19–24 周：分级预警（黄/橙/红）+ JWT 管理后台
- 第 25–30 周：联调、打包交付、文档收尾与验收

## 十三、下一步待办（按顺序做，做一步推一步）
1. 大屏加「路段下拉切换」和「时段×星期拥堵热力图」
2. 建 `preprocess/` 多格式预处理组件
3. 接入 Prophet：`POST /api/v1/predictions/flow`，离线训练、在线推理
4. 事故表 `accident` 与分级预警（黄/橙/红）
5. JWT 登录 + 管理后台（用户、预警规则）
