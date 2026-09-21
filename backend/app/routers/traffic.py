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


@router.get("/week7")
async def week7():
    """近7天拥堵指数（所有路段白天8-20点平均）"""
    import numpy as np, os
    p = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "gz_tensor.npy")
    t = np.load(os.path.normpath(p))  # 214 x 61 x 144
    # 最近7天（55-61天），白天时段 8:00-20:00 = time_id 49-120
    days = list(range(54, 61))
    today = []
    avg = []
    labels = []
    weekdays = ["周一","周二","周三","周四","周五","周六","周日"]
    for i, d in enumerate(days):
        day_data = t[:, d, 48:120].mean()  # 8:00-20:00
        today.append(round(40.0/float(day_data), 2) if day_data > 5 else 2.5)
        avg.append(round(40.0/float(t[:, :, 48:120].mean()), 2))
        labels.append(weekdays[i] + " " + f"09-{14+i:02d}")
    return ok({"labels": labels, "today": today, "avg": avg})


@router.get("/rank")
async def rank():
    """拥堵排行：所有路段按当前平均速度排序"""
    import numpy as np, os
    p = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "gz_tensor.npy")
    t = np.load(os.path.normpath(p))
    # 第30天18:00（晚高峰）速度
    speeds = t[:, 29, 108]  # 18:00 = time_id 108
    ranks = []
    for i in range(214):
        s = float(speeds[i]) if not np.isnan(speeds[i]) else 30
        ranks.append({"road_id": f"GZ{i+1:03d}", "speed": round(s,1), "index": round(40.0/s,2) if s>5 else 2.5})
    ranks.sort(key=lambda x: -x["index"])
    return ok(ranks[:10])


@router.get("/focus/{tab}")
async def focus(tab: str = "hub"):
    """重点区域排行（模拟：从214路段里挑几个）"""
    import numpy as np, os, random
    random.seed(42)
    p = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "gz_tensor.npy")
    t = np.load(os.path.normpath(p))
    names = {
      "hub": ["广州南站","广州东站","天河客运站","白云机场","海珠客运站","滘口客运站"],
      "scenic": ["广州塔","白云山","陈家祠","沙面","长隆欢乐世界","越秀公园"],
      "mall": ["天河城","正佳广场","万菱汇","北京路步行街","上下九","太古汇"]
    }.get(tab, ["广州塔"]*6)
    today = t[:, 29, 108]
    out = []
    for i, name in enumerate(names):
        idx = random.randint(0, 213)
        s = float(today[idx]) if not np.isnan(today[idx]) else 30
        out.append({"name": name, "index": round(40.0/s,2) if s>5 else 2.5, "flow": round(random.uniform(500,5000),0)})
    out.sort(key=lambda x: -x["index"])
    return ok(out)


@router.get("/flows")
def flows(road_id: str = Query("R001", description="路段ID"), db: Session = Depends(get_db)):
    """某路段最近 24h 流量"""
    service = TrafficService(db)
    result = service.get_flows(road_id)
    if not result["values"]:
        return not_found(f"路段 {road_id} 无数据")
    return ok(result)
