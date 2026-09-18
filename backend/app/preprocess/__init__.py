"""预处理模块导出。"""
from backend.app.preprocess.base import PreprocessAdapter, BadRow
from backend.app.preprocess.csv_adapter import CSVAdapter
from backend.app.preprocess.excel_adapter import ExcelAdapter

__all__ = ["PreprocessAdapter", "BadRow", "CSVAdapter", "ExcelAdapter"]

# 适配器注册表：扩展名 -> 适配器类
ADAPTERS = {
    ".csv": CSVAdapter,
    ".xlsx": ExcelAdapter,
    ".xls": ExcelAdapter,
}


def get_adapter(filename: str) -> PreprocessAdapter:
    """根据文件名获取对应适配器实例"""
    import os
    ext = os.path.splitext(filename.lower())[1]
    adapter_cls = ADAPTERS.get(ext)
    if not adapter_cls:
        raise ValueError(f"不支持的文件格式: {ext}")
    return adapter_cls()
