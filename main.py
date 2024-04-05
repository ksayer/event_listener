from time import sleep

from core.settings import settings
from services.monitor_events import monitor_total_distribution_events
from services.notification import NotificationDistributor
from services.tg import TelegramNotifier


def main():
    while True:
        monitor_total_distribution_events()
        NotificationDistributor(
            notification_services=[TelegramNotifier(settings.tg_token, settings.tg_chat_id)]
        ).send_notification()
        sleep(10)


if __name__ == "__main__":
    main()
