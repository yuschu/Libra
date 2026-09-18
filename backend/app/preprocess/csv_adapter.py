"""CSV 适配器：支持编码自动检测、分隔符推断。"""
import chardet
import pandas as pd
from io import BytesIO
from typing import Tuple, List

from backend.app.preprocess.base import PreprocessAdapter, BadRow


class CSVAdapter(PreprocessAdapter):
    """CSV 格式预处理适配器"""
    
    def read(self, file_bytes: bytes) -> pd.DataFrame:
        # 编码检测
        detected = chardet.detect(file_bytes)
        encoding = detected.get("encoding") or "utf-8"
        confidence = detected.get("confidence", 0)
        
        # 标准化编码名称（chardet 返回大写，pandas 需小写）
        encoding = encoding.lower().replace("utf-8-sig", "utf-8-sig")
        
        # 低置信度时尝试常用编码
        if confidence < 0.7:
            for enc in ["utf-8", "gbk", "gb2312", "utf-8-sig"]:
                try:
                    return pd.read_csv(BytesIO(file_bytes), encoding=enc)
                except UnicodeDecodeError:
                    continue
        
        # 尝试检测到的编码
        try:
            return pd.read_csv(BytesIO(file_bytes), encoding=encoding)
        except UnicodeDecodeError:
            # 回退 utf-8
            return pd.read_csv(BytesIO(file_bytes), encoding="utf-8", errors="replace")
