"""数据入库服务：小时聚合 + upsert。"""
from sqlalchemy.orm import Session
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy import func
from typing import Dict, List
import pandas as pd

from backend.app.models.traffic import TrafficFlow


class IngestService:
    """交通流量入库服务"""
    
    def __init__(self, db: Session):
        self.db = db

    def ingest(self, df: pd.DataFrame) -> Dict[str, int]:
        """
        将清洗后的小时级数据 upsert 入库
        返回: {inserted, updated, skipped}
        """
        if df.empty:
            return {"inserted": 0, "updated": 0, "skipped": 0}
        
        # 确保必要列存在
        required = ["dt", "road_id", "flow", "avg_speed", "density", "weather"]
        for col in required:
            if col not in df.columns:
                df[col] = None
        
        records = df.to_dict("records")
        inserted = 0
        updated = 0
        skipped = 0
        
        for rec in records:
            # 先查询是否已存在
            existing = self.db.query(TrafficFlow).filter(
                TrafficFlow.road_id == rec["road_id"],
                TrafficFlow.dt == rec["dt"]
            ).first()
            
            # 构建 upsert 语句
            stmt = sqlite_insert(TrafficFlow).values(
                dt=rec["dt"],
                road_id=rec["road_id"],
                flow=int(rec["flow"]) if rec["flow"] is not None else 0,
                avg_speed=float(rec["avg_speed"]) if rec["avg_speed"] is not None else 0.0,
                density=float(rec["density"]) if rec["density"] is not None else 0.0,
                weather=rec["weather"] or ""
            )
            
            # 冲突时更新（保留最新）
            stmt = stmt.on_conflict_do_update(
                index_elements=["road_id", "dt"],
                set_={
                    "flow": stmt.excluded.flow,
                    "avg_speed": stmt.excluded.avg_speed,
                    "density": stmt.excluded.density,
                    "weather": stmt.excluded.weather
                }
            )
            
            self.db.execute(stmt)
            
            # 统计：先查再 upsert，准确区分新增/更新
            if existing:
                updated += 1
            else:
                inserted += 1
        
        self.db.commit()
        return {"inserted": inserted, "updated": updated, "skipped": skipped}

    def load_sample(self) -> Dict[str, int]:
        """加载示例数据"""
        from backend.app.preprocess import CSVAdapter
        import os
        
        sample_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "traffic_sample.csv")
        sample_path = os.path.abspath(sample_path)
        
        with open(sample_path, "rb") as f:
            data = f.read()
        
        adapter = CSVAdapter()
        df, bad_rows = adapter.process(data)
        return self.ingest(df)

    def clear_all(self) -> int:
        """清空所有数据"""
        count = self.db.query(TrafficFlow).delete()
        self.db.commit()
        return count

    def get_status(self) -> Dict:
        """获取数据状态"""
        total = self.db.query(func.count(TrafficFlow.id)).scalar() or 0
        if total == 0:
            return {
                "has_data": False,
                "row_count": 0,
                "road_count": 0,
                "date_range": None
            }
        
        roads = self.db.query(func.count(TrafficFlow.road_id.distinct())).scalar() or 0
        min_dt = self.db.query(func.min(TrafficFlow.dt)).scalar()
        max_dt = self.db.query(func.max(TrafficFlow.dt)).scalar()
        
        return {
            "has_data": True,
            "row_count": total,
            "road_count": roads,
            "date_range": {"start": min_dt, "end": max_dt}
        }
