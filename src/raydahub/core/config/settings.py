from typing import Literal

from pydantic import BaseModel

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
