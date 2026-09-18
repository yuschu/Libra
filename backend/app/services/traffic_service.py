"""交通流量业务逻辑服务。"""
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional

from backend.app.models.traffic import TrafficFlow


class TrafficService:
    """交通流量服务"""
    def __init__(self, db: Session):
        self.db = db

    def get_overview(self) -> dict:
        """获取概览统计"""
        total_flow = self.db.query(func.sum(TrafficFlow.flow)).scalar() or 0
        avg_speed = self.db.query(func.avg(TrafficFlow.avg_speed)).scalar() or 0
        road_count = self.db.query(func.count(TrafficFlow.road_id.distinct())).scalar() or 0
        return {
            "total_flow": int(total_flow),
            "avg_speed": round(float(avg_speed), 1),
            "road_count": road_count,
            "alerts": 0
        }

    def get_flows(self, road_id: str = "R001", limit: int = 24) -> dict:
        """获取某路段最近流量数据"""
        rows = (
            self.db.query(TrafficFlow.dt, TrafficFlow.flow)
            .filter(TrafficFlow.road_id == road_id)
            .order_by(desc(TrafficFlow.dt))
            .limit(limit)
            .all()
        )
        rows = list(reversed(rows))
        labels = [r.dt[11:16] for r in rows]  # "HH:MM"
        values = [r.flow for r in rows]
        return {"road_id": road_id, "labels": labels, "values": values}
