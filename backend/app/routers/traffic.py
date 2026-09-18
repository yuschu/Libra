"""交通流量相关路由。"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.app.core.response import ok, not_found
from backend.app.services.traffic_service import TrafficService
from backend.app.core.database import get_db


router = APIRouter(prefix="/traffic", tags=["traffic"])


@router.get("/flows")
def flows(road_id: str = Query("R001", description="路段ID"), db: Session = Depends(get_db)):
    """某路段最近 24h 流量"""
    service = TrafficService(db)
    result = service.get_flows(road_id)
    if not result["values"]:
        return not_found(f"路段 {road_id} 无数据")
    return ok(result)
