"""Excel 适配器：读取第一个工作表。"""
import pandas as pd
from io import BytesIO

from backend.app.preprocess.base import PreprocessAdapter


class ExcelAdapter(PreprocessAdapter):
    """Excel (.xlsx) 格式预处理适配器"""
    
    def read(self, file_bytes: bytes) -> pd.DataFrame:
        # 读取第一个 sheet，不解析公式
        return pd.read_excel(BytesIO(file_bytes), sheet_name=0, engine="openpyxl")
