from typing import Any

from fastapi import APIRouter

from delvify.core import app_settings

endpoint = APIRouter()


@endpoint.get("")
def index() -> Any:
    return {"message": f"Hi there! This is {app_settings.SERVICE_NAME} microservice."}
