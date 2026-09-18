"""统一响应封装与错误码定义。"""
from typing import Any, Optional
from fastapi.responses import JSONResponse


class ResponseCode:
    """标准响应码"""
    OK = 0
    BAD_REQUEST = 400
    NOT_FOUND = 404
    INTERNAL_ERROR = 500
    VALIDATION_ERROR = 422


def ok(data: Any = None, message: str = "ok") -> dict:
    """成功响应"""
    return {"code": ResponseCode.OK, "message": message, "data": data}


def error(code: int, message: str, data: Any = None) -> dict:
    """错误响应"""
    return {"code": code, "message": message, "data": data}


def bad_request(message: str = "请求参数错误", data: Any = None) -> dict:
    return error(ResponseCode.BAD_REQUEST, message, data)


def not_found(message: str = "资源不存在", data: Any = None) -> dict:
    return error(ResponseCode.NOT_FOUND, message, data)


def internal_error(message: str = "服务器内部错误", data: Any = None) -> dict:
    return error(ResponseCode.INTERNAL_ERROR, message, data)


def validation_error(message: str = "数据校验失败", data: Any = None) -> dict:
    return error(ResponseCode.VALIDATION_ERROR, message, data)


class APIResponse(JSONResponse):
    """统一 JSON 响应，自动包装 code/message/data"""
    def __init__(
        self,
        content: Any = None,
        message: str = "ok",
        code: int = ResponseCode.OK,
        status_code: int = 200,
        **kwargs
    ):
        super().__init__(
            content={"code": code, "message": message, "data": content},
            status_code=status_code,
            **kwargs
        )
