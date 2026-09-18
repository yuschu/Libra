"""数据导入端点集成测试。"""
import pytest
import io
from fastapi.testclient import TestClient
from sqlalchemy import delete

from backend.app.models.traffic import TrafficFlow
from backend.app.core.database import test_engine, TestSessionLocal


def clear_test_db():
    """清空测试数据库"""
    db = TestSessionLocal()
    try:
        db.execute(delete(TrafficFlow))
        db.commit()
    finally:
        db.close()


class TestDataUpload:
    """POST /api/v1/data/upload 测试"""

    def setup_method(self):
        clear_test_db()

    def test_upload_valid_csv(self, client, db_session):
        """上传有效 CSV 文件"""
        csv_content = """dt,road_id,flow,avg_speed,density,weather
2026-09-01 00:00,R001,100,40.0,0.25,晴
2026-09-01 01:00,R001,120,42.0,0.28,晴
2026-09-01 00:00,R002,150,45.0,0.30,阴"""
        files = {"files": ("test.csv", io.BytesIO(csv_content.encode("utf-8")), "text/csv")}
        resp = client.post("/api/v1/data/upload", files=files)
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0
        assert len(data["data"]) == 1
        item = data["data"][0]
        assert item["filename"] == "test.csv"
        assert item["inserted"] > 0
        assert item["bad_rows"] == []

    def test_upload_multiple_files(self, client, db_session):
        """批量上传多个文件"""
        csv1 = "dt,road_id,flow,avg_speed,density,weather\n2026-09-01 00:00,R001,100,40.0,0.25,晴"
        csv2 = "dt,road_id,flow,avg_speed,density,weather\n2026-09-01 01:00,R001,120,42.0,0.28,晴"
        files = [
            ("files", ("a.csv", io.BytesIO(csv1.encode("utf-8")), "text/csv")),
            ("files", ("b.csv", io.BytesIO(csv2.encode("utf-8")), "text/csv")),
        ]
        resp = client.post("/api/v1/data/upload", files=files)
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0
        assert len(data["data"]) == 2

    def test_upload_invalid_file(self, client, db_session):
        """上传无效文件（非 CSV/Excel）"""
        files = {"files": ("test.txt", io.BytesIO(b"invalid"), "text/plain")}
        resp = client.post("/api/v1/data/upload", files=files)
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0
        assert len(data["data"]) == 1
        assert "error" in data["data"][0]

    def test_upload_empty_file_list(self, client):
        """不上传文件"""
        resp = client.post("/api/v1/data/upload", files={})
        assert resp.status_code in (200, 422)


class TestDataSample:
    """POST /api/v1/data/sample 测试"""

    def setup_method(self):
        clear_test_db()

    def test_load_sample(self, client, db_session):
        """加载示例数据"""
        resp = client.post("/api/v1/data/sample")
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0
        assert data["data"]["inserted"] > 0

    def test_sample_twice_upsert(self, client, db_session):
        """重复加载示例数据应 upsert 不重复"""
        client.post("/api/v1/data/sample")
        resp = client.post("/api/v1/data/sample")
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0


class TestDataClear:
    """POST /api/v1/data/clear 测试"""

    def setup_method(self):
        clear_test_db()

    def test_clear_empty_db(self, client, db_session):
        """空库清空"""
        resp = client.post("/api/v1/data/clear")
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0
        assert data["data"]["cleared_rows"] == 0

    def test_clear_with_data(self, client, db_session):
        """有数据时清空"""
        client.post("/api/v1/data/sample")
        resp = client.post("/api/v1/data/clear")
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0
        assert data["data"]["cleared_rows"] > 0
        resp = client.get("/api/v1/data/status")
        assert resp.json()["data"]["has_data"] is False


class TestDataStatus:
    """GET /api/v1/data/status 测试"""

    def setup_method(self):
        clear_test_db()

    def test_status_empty(self, client, db_session):
        """空库状态"""
        resp = client.get("/api/v1/data/status")
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0
        assert data["data"]["has_data"] is False
        assert data["data"]["row_count"] == 0
        assert data["data"]["road_count"] == 0
        assert data["data"]["date_range"] is None

    def test_status_with_data(self, client, db_session):
        """有数据时状态"""
        client.post("/api/v1/data/sample")
        resp = client.get("/api/v1/data/status")
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0
        assert data["data"]["has_data"] is True
        assert data["data"]["row_count"] > 0
        assert data["data"]["road_count"] > 0
        assert data["data"]["date_range"] is not None
        assert "start" in data["data"]["date_range"]
        assert "end" in data["data"]["date_range"]


class TestDataBadRows:
    """坏行处理测试"""

    def setup_method(self):
        clear_test_db()

    def test_upload_with_bad_rows(self, client, db_session):
        """包含坏行的 CSV（关键列有效，数值列无效）"""
        csv_content = """dt,road_id,flow,avg_speed,density,weather
2026-09-01 00:00,R001,100,40.0,0.25,晴
2026-09-01 00:00,R002,abc,not_a_number,1.5,阴
2026-09-01 01:00,R001,120,42.0,0.28,晴"""
        files = {"files": ("bad.csv", io.BytesIO(csv_content.encode("utf-8")), "text/csv")}
        resp = client.post("/api/v1/data/upload", files=files)
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0
        item = data["data"][0]
        assert item["inserted"] == 2  # 2 valid rows (first and third)
        assert len(item["bad_rows"]) == 1  # 1 bad row captured (second row)


class TestHourlyAggregation:
    """小时聚合测试"""

    def setup_method(self):
        clear_test_db()

    def test_multiple_rows_same_hour_aggregated(self, client, db_session):
        """同一小时多行数据聚合求和"""
        csv_content = """dt,road_id,flow,avg_speed,density,weather
2026-09-01 00:00,R001,100,40.0,0.25,晴
2026-09-01 00:15,R001,50,42.0,0.30,晴
2026-09-01 00:45,R001,30,38.0,0.20,晴"""
        files = {"files": ("agg.csv", io.BytesIO(csv_content.encode("utf-8")), "text/csv")}
        resp = client.post("/api/v1/data/upload", files=files)
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0
        # 3行聚合为1小时，flow求和=180
        assert data["data"][0]["inserted"] == 1
        
        # 验证聚合结果
        resp = client.get("/api/v1/traffic/flows?road_id=R001")
        flow_data = resp.json()["data"]
        assert flow_data["values"][0] == 180  # 100+50+30
