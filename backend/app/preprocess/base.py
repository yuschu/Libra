"""预处理适配器基类：定义统一接口，供 CSV/Excel/JSON/API 适配器实现。"""
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Any, Optional
import pandas as pd


class BadRow:
    """坏行记录"""
    def __init__(self, row_index: int, raw_data: Dict[str, Any], errors: List[str]):
        self.row_index = row_index
        self.raw_data = raw_data
        self.errors = errors

    def to_dict(self) -> Dict[str, Any]:
        return {
            "row_index": self.row_index,
            "raw_data": self.raw_data,
            "errors": self.errors
        }


class PreprocessAdapter(ABC):
    """预处理适配器抽象基类"""
    
    # 标准列名映射（目标 schema）
    TARGET_COLUMNS = {
        "dt": ["dt", "date", "time", "datetime", "timestamp", "时间", "日期", "日期时间"],
        "road_id": ["road_id", "road", "segment", "segment_id", "link_id", "路段", "路段id", "道路"],
        "flow": ["flow", "volume", "traffic_flow", "车流量", "流量"],
        "avg_speed": ["avg_speed", "speed", "average_speed", "velocity", "平均速度", "速度"],
        "density": ["density", "concentration", "密度"],
        "weather": ["weather", "condition", "天气", "天气状况"]
    }
    
    # 数值列范围校验
    NUMERIC_RANGES = {
        "flow": (0, 10000),
        "avg_speed": (0, 200),
        "density": (0, 1.0)
    }

    @abstractmethod
    def read(self, file_bytes: bytes) -> pd.DataFrame:
        """读取文件字节流为 DataFrame"""
        pass

    def detect_columns(self, df: pd.DataFrame) -> Dict[str, str]:
        """
        自动检测列映射：返回 {标准列名: 原始列名}
        策略：精确匹配 -> 模糊匹配（忽略大小写、下划线） -> 关键词匹配
        """
        mapping = {}
        df_cols_lower = {c.lower().replace("_", "").replace(" ", ""): c for c in df.columns}
        
        for target, candidates in self.TARGET_COLUMNS.items():
            found = None
            # 1. 精确匹配（不区分大小写）
            for cand in candidates:
                for df_col, orig in df_cols_lower.items():
                    if cand.lower().replace("_", "").replace(" ", "") == df_col:
                        found = orig
                        break
                if found:
                    break
            # 2. 关键词包含匹配
            if not found:
                for cand in candidates:
                    key = cand.lower().replace("_", "").replace(" ", "")
                    for df_col, orig in df_cols_lower.items():
                        if key in df_col or df_col in key:
                            found = orig
                            break
                    if found:
                        break
            if found:
                mapping[target] = found
        return mapping

    def clean(self, df: pd.DataFrame, column_mapping: Dict[str, str]) -> pd.DataFrame:
        """
        清洗数据：重命名列、类型转换、时间对齐、异常值处理
        """
        # 重命名为标准列名
        rename_map = {v: k for k, v in column_mapping.items()}
        df = df.rename(columns=rename_map)
        
        # 只保留目标列
        target_cols = [c for c in self.TARGET_COLUMNS.keys() if c in df.columns]
        df = df[target_cols].copy()
        
        # 时间列处理：解析、对齐到小时
        if "dt" in df.columns:
            df["dt"] = pd.to_datetime(df["dt"], errors="coerce")
            # 对齐到整点（向下取整）
            df["dt"] = df["dt"].dt.floor("h")
            df = df.dropna(subset=["dt"])
            df["dt"] = df["dt"].dt.strftime("%Y-%m-%d %H:%M")
        
        # 数值列类型转换
        for col in ["flow", "avg_speed", "density"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        
        # 去除关键列为空的行
        key_cols = [c for c in ["dt", "road_id"] if c in df.columns]
        if key_cols:
            df = df.dropna(subset=key_cols)
        
        # 数值范围校验
        for col, (min_v, max_v) in self.NUMERIC_RANGES.items():
            if col in df.columns:
                df = df[(df[col].isna()) | ((df[col] >= min_v) & (df[col] <= max_v))]
        
        # density 裁剪到 [0, 1]
        if "density" in df.columns:
            df["density"] = df["density"].clip(0, 1)
        
        # weather 标准化
        if "weather" in df.columns:
            df["weather"] = df["weather"].astype(str).str.strip()
            df["weather"] = df["weather"].replace({"nan": None, "None": None})
        
        return df.reset_index(drop=True)

    def validate(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, List[BadRow]]:
        """
        校验数据：返回 (有效数据, 坏行列表)
        """
        bad_rows = []
        valid_mask = pd.Series(True, index=df.index)
        
        # 必填列检查
        for col in ["dt", "road_id"]:
            if col not in df.columns:
                # 整列缺失视为全坏
                for idx, row in df.iterrows():
                    bad_rows.append(BadRow(idx, row.to_dict(), [f"缺少必填列: {col}"]))
                return pd.DataFrame(), bad_rows
            missing = df[col].isna()
            if missing.any():
                for idx in df[missing].index:
                    bad_rows.append(BadRow(idx, df.loc[idx].to_dict(), [f"{col} 为空"]))
                valid_mask &= ~missing
        
        # 数值列非空检查
        for col in ["flow", "avg_speed", "density"]:
            if col in df.columns:
                missing = df[col].isna()
                if missing.any():
                    for idx in df[missing].index:
                        bad_rows.append(BadRow(idx, df.loc[idx].to_dict(), [f"{col} 非数值或为空"]))
                    valid_mask &= ~missing
        
        valid_df = df[valid_mask].copy().reset_index(drop=True)
        return valid_df, bad_rows

    def aggregate_hourly(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        按 (road_id, dt) 聚合到小时粒度
        flow=sum, avg_speed=mean, density=mean, weather=mode(众数)
        """
        if df.empty:
            return df
        
        agg_funcs = {}
        if "flow" in df.columns:
            agg_funcs["flow"] = "sum"
        if "avg_speed" in df.columns:
            agg_funcs["avg_speed"] = "mean"
        if "density" in df.columns:
            agg_funcs["density"] = "mean"
        if "weather" in df.columns:
            agg_funcs["weather"] = lambda x: x.mode().iloc[0] if not x.mode().empty else None
        
        # road_id 保留第一个（同一分组内应相同）
        if "road_id" in df.columns:
            agg_funcs["road_id"] = "first"
        
        result = df.groupby("dt", as_index=False).agg(agg_funcs)
        return result

    def process(self, file_bytes: bytes) -> Tuple[pd.DataFrame, List[BadRow]]:
        """
        完整处理流程：读取 -> 检测列 -> 清洗 -> 校验 -> 聚合
        返回 (聚合后的干净 DataFrame, 坏行列表)
        """
        df = self.read(file_bytes)
        mapping = self.detect_columns(df)
        df_clean = self.clean(df, mapping)
        valid_df, bad_rows = self.validate(df_clean)
        aggregated = self.aggregate_hourly(valid_df)
        return aggregated, bad_rows
