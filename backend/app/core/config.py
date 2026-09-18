"""配置管理：从 .env 加载类型化设置。"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from pathlib import Path


# 项目根目录（backend 的上一级）
PROJECT_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    APP_ENV: str = "dev"
    DATABASE_URL: str = "sqlite:///./traffic.db"
    CORS_ORIGINS: str = "*"

    @property
    def cors_origins_list(self) -> List[str]:
        """解析 CORS_ORIGINS 为列表，支持逗号分隔或 '*'"""
        if self.CORS_ORIGINS.strip() == "*":
            return ["*"]
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]

    @property
    def database_url_resolved(self) -> str:
        """将 DATABASE_URL 中的相对路径解析为基于项目根目录的绝对路径"""
        url = self.DATABASE_URL
        if url.startswith("sqlite:///") and not url.startswith("sqlite:////"):
            # sqlite:///./xxx -> 相对路径，需解析为绝对路径
            rel_path = url[10:]  # 去掉 "sqlite:///"
            abs_path = (PROJECT_ROOT / rel_path).resolve()
            return f"sqlite:///{abs_path}"
        return url


settings = Settings()
