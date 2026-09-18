"""数据库连接与会话管理。"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from backend.app.core.config import settings
from backend.app.models.traffic import Base


# 主数据库
engine = create_engine(
    settings.database_url_resolved,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url_resolved else {},
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 测试数据库（内存或文件）
TEST_DATABASE_URL = "sqlite:///./test.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False}, echo=False)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def init_db() -> None:
    """初始化数据库表"""
    Base.metadata.create_all(bind=engine)


def init_test_db() -> None:
    """初始化测试数据库表"""
    Base.metadata.create_all(bind=test_engine)


def get_db() -> Generator[Session, None, None]:
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_test_db() -> Generator[Session, None, None]:
    """获取测试数据库会话"""
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
