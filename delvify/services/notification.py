import httpx

from delvify.core.logger import LoggerMixin
from delvify.core.retries import retry
from delvify.core.settings import AppSettings, app_settings
from delvify.schemas.email import Email


class NotificationService(LoggerMixin):
    def __init__(self, settings: AppSettings = app_settings):
        super().__init__()
        if settings.NOTIFICATION_SERVICE_URL is None:
            raise Exception("NOTIFICATION_SERVICE_URL is not set")
        self._host = settings.NOTIFICATION_SERVICE_URL

    @retry(max_retries=5, base_delay=2)
    def send_email(self, email: Email) -> None:
        response = httpx.post(
            f"{self._host}api/v1/notifications/email?name=stdout",
            json=email.model_dump(mode="json"),
        )
        if response.status_code != 200:
            raise Exception(
                f"Failed to send email to {email.destination}. "
                + f"Response code: {response.status_code}"
                + f"Response body: {response.text}"
            )
        return
