from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    project_name: str = "CRM"
    app_host: str = "localhost"
    app_port: int = 8080

    cors_origins: list = ["*"]

    model_config = SettingsConfigDict(
        extra="allow"
    )

app_config = AppConfig()