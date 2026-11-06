from pydantic import BaseModel


class AppSettings(BaseModel):
    service_name: str = "RaydaHub"
    service_version: str = "0.1.0"
