# traffic-system

城市交通运行数据可视化分析、流量预测与拥堵预警系统（起步骨架 v0.1）

## 今天跑通最小闭环

1. 启动后端（在 backend 目录）：
   ```powershell
   cd D:\InformationTechnologyStudy\traffic-system\backend
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   uvicorn app.main:app --reload
   ```
2. 浏览器打开 http://127.0.0.1:8000/docs 看接口文档。
3. 双击打开 web-screen/index.html，应看到一条流量折线（数据来自后端）。

## 下一步
- 把 data/ 里的公开 CSV 读进 SQLite，替换 main.py 里的假数据；
- 再增加热力图、路段排行等图表；
- 接入 Prophet 预测接口。
