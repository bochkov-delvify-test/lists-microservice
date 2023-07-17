from fastapi import FastAPI

from delvify.api.v1 import ms_router
from delvify.core import app_settings, logger


def startup_handler():
    logger.info("App Started")


def shutdown_handler():
    logger.info("App Stopped")


def build_app() -> FastAPI:
    app = FastAPI(title=app_settings.SERVICE_NAME, openapi_url="/api/v1/openapi.json")
    app.include_router(ms_router)
    app.add_event_handler("startup", startup_handler)
    app.add_event_handler("shutdown", shutdown_handler)
    return app


ms = build_app()
