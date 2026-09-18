"""路由模块导出。"""
from backend.app.routers.stats import router as stats_router
from backend.app.routers.traffic import router as traffic_router
from backend.app.routers.data import router as data_router

__all__ = ["stats_router", "traffic_router", "data_router"]
