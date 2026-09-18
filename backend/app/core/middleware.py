"""中间件：CORS、请求日志等。"""
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response
import time

from backend.app.core.config import settings
from backend.app.core.logging import get_logger, RequestLogger


logger = get_logger(__name__)
request_logger = RequestLogger(logger)


def setup_cors(app: FastAPI) -> None:
    """配置 CORS"""
    origins = settings.cors_origins_list
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


async def request_logging_middleware(request: Request, call_next):
    """请求日志中间件"""
    start_time = time.perf_counter()
    try:
        response = await call_next(request)
        latency_ms = (time.perf_counter() - start_time) * 1000
        request_logger.log_request(
            method=request.method,
            path=request.url.path,
            params=dict(request.query_params),
            status_code=response.status_code,
            latency_ms=latency_ms
        )
        return response
    except Exception as e:
        latency_ms = (time.perf_counter() - start_time) * 1000
        request_logger.log_request(
            method=request.method,
            path=request.url.path,
            params=dict(request.query_params),
            status_code=500,
            latency_ms=latency_ms,
            error=str(e)
        )
        raise
