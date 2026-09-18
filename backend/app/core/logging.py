"""结构化日志配置：JSON 格式，按天轮转，保留 7 天。"""
import logging
import logging.handlers
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


class JSONFormatter(logging.Formatter):
    """JSON 格式化器"""
    def format(self, record: logging.LogRecord) -> str:
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        # 添加额外字段
        for key, value in record.__dict__.items():
            if key not in {"name", "msg", "args", "created", "filename", "funcName",
                          "levelname", "levelno", "lineno", "module", "msecs",
                          "message", "msg", "pathname", "process", "processName",
                          "relativeCreated", "thread", "threadName", "exc_info",
                          "exc_text", "stack_info", "getMessage"}:
                log_data[key] = value
        # 异常信息
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_data, ensure_ascii=False)


def setup_logging(log_dir: str = "logs", app_name: str = "libra") -> None:
    """配置结构化日志"""
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)

    # 根 logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # 清除现有 handlers
    root_logger.handlers.clear()

    # 控制台输出（开发环境）
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(JSONFormatter())
    root_logger.addHandler(console_handler)

    # 文件输出：应用日志（按天轮转，保留 7 天）
    app_file = log_path / f"{app_name}.log"
    file_handler = logging.handlers.TimedRotatingFileHandler(
        app_file,
        when="midnight",
        interval=1,
        backupCount=7,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(JSONFormatter())
    root_logger.addHandler(file_handler)

    # 文件输出：错误日志（单独文件，按天轮转，保留 7 天）
    error_file = log_path / f"{app_name}_error.log"
    error_handler = logging.handlers.TimedRotatingFileHandler(
        error_file,
        when="midnight",
        interval=1,
        backupCount=7,
        encoding="utf-8"
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(JSONFormatter())
    root_logger.addHandler(error_handler)

    # 设置第三方库日志级别
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """获取指定名称的 logger"""
    return logging.getLogger(name)


class RequestLogger:
    """请求日志记录器"""
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def log_request(
        self,
        method: str,
        path: str,
        params: Dict[str, Any],
        status_code: int,
        latency_ms: float,
        error: str = None
    ) -> None:
        """记录请求日志"""
        extra = {
            "event": "http_request",
            "method": method,
            "path": path,
            "params": params,
            "status_code": status_code,
            "latency_ms": latency_ms,
        }
        if error:
            extra["error"] = error
            self.logger.error(f"{method} {path} - {status_code} - {latency_ms:.2f}ms - {error}", extra=extra)
        else:
            self.logger.info(f"{method} {path} - {status_code} - {latency_ms:.2f}ms", extra=extra)
