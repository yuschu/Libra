"""FastAPI 应用入口。"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from backend.app.core.config import settings
from backend.app.core.logging import setup_logging
from backend.app.core.middleware import setup_cors, request_logging_middleware
from backend.app.core.database import init_db
from backend.app.routers import stats, traffic, data, meta


# 初始化日志
setup_logging()

# 创建应用
app = FastAPI(title="Libra Traffic API", version="0.1.0")

# 中间件
setup_cors(app)
app.middleware("http")(request_logging_middleware)

# 初始化数据库
init_db()

# 静态文件服务
WEB_SCREEN_DIR = Path(__file__).parent.parent.parent / "web-screen"
app.mount("/web-screen", StaticFiles(directory=WEB_SCREEN_DIR), name="web-screen")

# 路由
app.include_router(stats.router, prefix="/api/v1")
app.include_router(traffic.router, prefix="/api/v1")
app.include_router(data.router, prefix="/api/v1")
app.include_router(meta.router, prefix="/api/v1")


@app.get("/")
def root():
    return {"msg": "ok, see /docs"}
