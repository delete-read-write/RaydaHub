from typing import Literal
from urllib.parse import quote_plus

from pydantic import BaseModel, Field, PostgresDsn, SecretStr

type LoggingLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class AppSettings(BaseModel):
    service_name: str = "RaydaHub"
    service_version: str = "0.1.0"


class LoggingSettings(BaseModel):
    level: LoggingLevel = "INFO"
    fmt: str = (
        "[%(asctime)s.%(msecs)03d] [%(threadName)s] "
        "%(funcName)20s "
        "%(module)s:%(lineno)d "
        "%(levelname)-8s - %(message)s"
    )
    datefmt: str = "%Y-%m-%d %H:%M:%S"


class FastAPISettings(BaseModel):
    debug: bool = False
    docs_url: str | None = "/docs"
    redoc_url: str | None = "/redoc"
    openapi_url: str | None = "/openapi.json"


class SQLASettings(BaseModel):
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 15
    max_overflow: int = 10
    connect_timeout_s: int = Field(default=5, gt=0)


class PostgresSettings(BaseModel):
    user: str
    password: SecretStr
    host: str
    port: int
    db: str

    @property
    def dsn(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+psycopg",
                username=self.user,
                password=quote_plus(self.password.get_secret_value()),
                host=self.host,
                port=self.port,
                path=self.db,
            )
        )
