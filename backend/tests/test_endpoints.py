"""核心端点集成测试。"""
import pytest
from fastapi.testclient import TestClient


class TestStatsOverview:
    """GET /api/v1/stats/overview 测试"""

    def test_overview_with_data(self, client, sample_data):
        """有数据时返回正确统计"""
        resp = client.get("/api/v1/stats/overview")
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0
        assert data["message"] == "ok"
        assert data["data"]["total_flow"] == 370  # 100 + 120 + 150
        assert data["data"]["avg_speed"] == 42.3  # (40+42+45)/3 ≈ 42.3
        assert data["data"]["road_count"] == 2
        assert data["data"]["alerts"] == 0

    def test_overview_empty_db(self, client):
        """空数据库返回零值"""
        resp = client.get("/api/v1/stats/overview")
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0
        assert data["data"]["total_flow"] == 0
        assert data["data"]["avg_speed"] == 0
        assert data["data"]["road_count"] == 0


class TestTrafficFlows:
    """GET /api/v1/traffic/flows 测试"""

    def test_flows_existing_road(self, client, sample_data):
        """存在的路段返回流量数据"""
        resp = client.get("/api/v1/traffic/flows?road_id=R001")
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0
        assert data["data"]["road_id"] == "R001"
        assert len(data["data"]["labels"]) == 2
        assert len(data["data"]["values"]) == 2
        assert data["data"]["values"] == [100, 120]

    def test_flows_nonexistent_road(self, client):
        """不存在的路段返回 404"""
        resp = client.get("/api/v1/traffic/flows?road_id=R999")
        assert resp.status_code == 200  # 我们返回 200 但 code 非 0
        data = resp.json()
        assert data["code"] == 404
        assert "无数据" in data["message"]

    def test_flows_default_road(self, client, sample_data):
        """默认路段 R001"""
        resp = client.get("/api/v1/traffic/flows")
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0
        assert data["data"]["road_id"] == "R001"
