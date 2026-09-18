"""统计相关路由。"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.core.response import ok
from backend.app.services.traffic_service import TrafficService
from backend.app.core.database import get_db


router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/overview")
def overview(db: Session = Depends(get_db)):
    """总流量、平均速度、路段数"""
    service = TrafficService(db)
    return ok(service.get_overview())
