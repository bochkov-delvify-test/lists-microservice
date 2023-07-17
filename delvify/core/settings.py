# mypy: disable-error-code="call-arg"
from typing import Any, Mapping, Optional

from pydantic import FieldValidationInfo, SecretStr, field_validator
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    SERVICE_NAME: str
    SECRET_KEY: SecretStr

    TOKEN_ALGORITHM: str

    model_config = SettingsConfigDict(case_sensitive=True)


def build_conn_url(env: dict[str, Any] | Mapping) -> str:
    return "{scheme}://{user}:{password}@{host}/{db}".format(
        scheme=env.get("DB_SCHEME"),
        user=env.get("DB_USER"),
        password=env.get("DB_PASSWORD"),
        host=env.get("DB_HOST"),
        db=env.get("DB_NAME"),
    )


class DBSettings(BaseSettings):
    DB_SCHEME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_URI: Optional[MultiHostUrl] = None

    @field_validator("DB_URI")
    @classmethod
    def get_db_uri(cls, v: Optional[str], info: FieldValidationInfo) -> Any:
        data = info.data
        if isinstance(v, str):
            return v
        return build_conn_url(data)

    model_config = SettingsConfigDict(case_sensitive=True)


app_settings: AppSettings = AppSettings()
db_settings: Optional[
    DBSettings
] = None  # Change to DBSettings() if you are using a database
