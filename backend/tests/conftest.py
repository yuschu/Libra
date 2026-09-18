"""测试配置与公共 fixtures。"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.sqlite import insert as sqlite_insert

from backend.app.main import app
from backend.app.core.database import get_db
from backend.app.models.traffic import Base, TrafficFlow


# 测试数据库
TEST_DATABASE_URL = "sqlite:///./test.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """创建测试表并清理"""
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(autouse=True)
def clear_test_db():
    """每个测试前清空数据库"""
    db = TestSessionLocal()
    try:
        db.execute(delete(TrafficFlow))
        db.commit()
    finally:
        db.close()


@pytest.fixture
def db_session():
    """提供测试数据库会话"""
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(db_session):
    """提供测试客户端"""
    app.dependency_overrides[get_db] = lambda: db_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def sample_data(db_session):
    """插入示例数据（使用 upsert 避免冲突）"""
    data = [
        {"dt": "2026-09-01 00:00", "road_id": "R001", "flow": 100, "avg_speed": 40.0, "density": 0.25, "weather": "晴"},
        {"dt": "2026-09-01 01:00", "road_id": "R001", "flow": 120, "avg_speed": 42.0, "density": 0.28, "weather": "晴"},
        {"dt": "2026-09-01 00:00", "road_id": "R002", "flow": 150, "avg_speed": 45.0, "density": 0.30, "weather": "晴"},
    ]
    for row in data:
        stmt = sqlite_insert(TrafficFlow).values(**row)
        stmt = stmt.on_conflict_do_update(
            index_elements=["road_id", "dt"],
            set_={k: stmt.excluded[k] for k in row.keys()}
        )
        db_session.execute(stmt)
    db_session.commit()
    yield data
