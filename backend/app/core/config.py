"""配置管理：从 .env 加载类型化设置。"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


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


settings = Settings()
