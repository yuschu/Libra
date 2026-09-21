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

    import os, numpy as np
    _TENSOR = None
    def _tensor(self):
        if self.__class__._TENSOR is None:
            p = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "gz_tensor.npy")
            p = os.path.normpath(p)
            self.__class__._TENSOR = np.load(p)
        return self.__class__._TENSOR

    def get_flows(self, road_id: str = "GZ001", limit: int = 24) -> dict:
        """从OpenITS广州数据集读真实速度（km/h）"""
        try:
            t = self._tensor()
            # road_id GZ001 -> index 0
            idx = int(road_id.replace("GZ","")) - 1
            if idx < 0 or idx >= t.shape[0]:
                idx = 0
            # 取第30天（8月30日）一天144个时段
            day = t[idx, 29, :]  # shape (144,)
            # 转成 HH:MM 标签
            labels = []
            values = []
            for i in range(0, 144, 6):  # 每小时一个点，24个
                h = i // 6
                m = (i % 6) * 10
                labels.append(f"{h:02d}:{m:02d}")
                v = float(day[i])
                values.append(round(v, 1) if not np.isnan(v) else 40.0)
            return {"road_id": road_id, "labels": labels, "values": values}
        except Exception as e:
            return {"road_id": road_id, "labels": [], "values": [], "error": str(e)}
