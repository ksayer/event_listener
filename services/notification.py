from datetime import datetime, timezone, timedelta
from typing import Protocol

from core.settings import settings
from database.models import NotificationDaemon, TotalDistribution
from services.report import ReportService


class NotificationService(Protocol):
    def send_message(self, msg: str):
        ...


def get_report() -> str:
    created = datetime.now(tz=timezone.utc) - timedelta(hours=24)
    distributions = TotalDistribution.filter_by_created(created)
    return ReportService(distributions).create()


class NotificationDistributor:
    def __init__(self, notification_services: list[NotificationService]):
        self.notification_services = notification_services

    def send_notification(self):
        if self._notification_ready():
            msg = get_report()
            for service in self.notification_services:
                service.send_message(msg)
            NotificationDaemon.update_time()

    @staticmethod
    def _notification_ready() -> bool | None:
        previous_report = NotificationDaemon.get_or_create()
        now = datetime.now(tz=timezone.utc)
        last_report = previous_report.last_report_at
        if (
            not last_report or
            (now - last_report.astimezone(timezone.utc)).seconds > settings.notification_period
        ):
            return True
