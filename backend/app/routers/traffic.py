"""交通流量相关路由。"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.app.core.response import ok, not_found
from backend.app.services.traffic_service import TrafficService
from backend.app.core.database import get_db


router = APIRouter(prefix="/traffic", tags=["traffic"])


@router.get("/avg-speed-by-hour")
async def avg_speed_by_hour():
    """24小时平均速度（所有214路段聚合）+ 61天均值对比"""
    import numpy as np, os
    p = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "gz_tensor.npy")
    t = np.load(os.path.normpath(p))  # 214 x 61 x 144
    # 第30天当天，每小时一个点（每6个10分钟段取一个）
    today = t[:, 29, :].mean(axis=0)  # shape (144,)
    today_24 = [round(float(today[i*6]), 1) if not np.isnan(today[i*6]) else 0 for i in range(24)]
    # 61天平均
    avg = t[:, :, :].mean(axis=(0,1))  # shape (144,)
    avg_24 = [round(float(avg[i*6]), 1) if not np.isnan(avg[i*6]) else 0 for i in range(24)]
    labels = [f"{h:02d}:00" for h in range(24)]
    # 速度 -> 拥堵指数（畅通速度40为基准，指数=40/speed）
    def to_idx(speeds):
        return [round(40.0/s, 2) if s > 5 else 2.5 for s in speeds]
    return ok({
        "labels": labels,
        "today": to_idx(today_24),
        "avg": to_idx(avg_24)
    })


@router.get("/flows")
def flows(road_id: str = Query("R001", description="路段ID"), db: Session = Depends(get_db)):
    """某路段最近 24h 流量"""
    service = TrafficService(db)
    result = service.get_flows(road_id)
    if not result["values"]:
        return not_found(f"路段 {road_id} 无数据")
    return ok(result)
