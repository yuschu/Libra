"""元数据相关路由：路段信息、事故、车辆类型等。"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import json
import os

from backend.app.core.response import ok, not_found, internal_error


router = APIRouter(prefix="/meta", tags=["meta"])

# 数据文件路径
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
ROAD_META_PATH = os.path.join(DATA_DIR, "road_meta.json")
ACCIDENTS_PATH = os.path.join(DATA_DIR, "accidents.json")
VEHICLE_TYPES_PATH = os.path.join(DATA_DIR, "vehicle_types.json")


def load_json_file(path: str, default=None) -> Any:
    """加载 JSON 文件"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"数据文件格式错误: {str(e)}")


@router.get("/roads")
async def get_roads():
    """获取所有路段元数据"""
    data = load_json_file(ROAD_META_PATH, {"roads": []})
    return ok(data.get("roads", []))


@router.get("/roads/{road_id}")
async def get_road(road_id: str):
    """获取单个路段详情"""
    data = load_json_file(ROAD_META_PATH, {"roads": []})
    for road in data.get("roads", []):
        if road["road_id"] == road_id:
            return ok(road)
    return not_found(f"路段 {road_id} 不存在")


@router.get("/accidents")
async def get_accidents(road_id: str = None, dt_start: str = None, dt_end: str = None):
    """获取事故列表，支持按路段和时间范围筛选"""
    data = load_json_file(ACCIDENTS_PATH, {"accidents": []})
    accidents = data.get("accidents", [])
    
    if road_id:
        accidents = [a for a in accidents if a["road_id"] == road_id]
    if dt_start:
        accidents = [a for a in accidents if a["dt"] >= dt_start]
    if dt_end:
        accidents = [a for a in accidents if a["dt"] <= dt_end]
    
    return ok(accidents)


@router.get("/active-provinces")
async def get_active_provinces():
    """从路段坐标反推有数据的省份（目前数据在广东）"""
    # 根据路段中心经纬度判断省份范围
    data = load_json_file(ROAD_META_PATH, {"roads": []})
    roads = data.get("roads", [])
    if not roads:
        return ok(["广东省"])
    # 广州中心 113.2-113.5, 23.0-23.2 -> 广东省
    return ok(["广东省"])


@router.get("/vehicle-types")
async def get_vehicle_types(road_id: str = None, dt_start: str = None, dt_end: str = None):
    """获取车辆类型统计，支持按路段和时间范围筛选"""
    data = load_json_file(VEHICLE_TYPES_PATH, {"vehicle_types": []})
    vehicle_types = data.get("vehicle_types", [])
    
    if road_id:
        vehicle_types = [v for v in vehicle_types if v["road_id"] == road_id]
    if dt_start:
        vehicle_types = [v for v in vehicle_types if v["dt"] >= dt_start]
    if dt_end:
        vehicle_types = [v for v in vehicle_types if v["dt"] <= dt_end]
    
    return ok(vehicle_types)
