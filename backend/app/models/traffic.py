"""SQLAlchemy 模型定义。"""
from sqlalchemy import Column, Integer, String, Float, Text, Index
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class TrafficFlow(Base):
    """交通流量表"""
    __tablename__ = "traffic_flow"

    id = Column(Integer, primary_key=True, autoincrement=True)
    dt = Column(String(19), nullable=False, index=True)  # YYYY-MM-DD HH:MM
    road_id = Column(String(32), nullable=False, index=True)
    flow = Column(Integer, nullable=False)
    avg_speed = Column(Float, nullable=False)
    density = Column(Float, nullable=False)
    weather = Column(String(16), nullable=False)

    __table_args__ = (
        Index("idx_road_dt", "road_id", "dt"),
    )
