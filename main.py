import logging
from time import sleep

from core.settings import settings
from services.monitor_events import monitor_total_distribution_events
from services.notification import NotificationDistributor
from services.tg import TelegramNotifier


logger = logging.getLogger(__name__)


def main():
    while True:
        try:
            monitor_total_distribution_events()
            NotificationDistributor(
                notification_services=[TelegramNotifier(settings.tg_token, settings.tg_chat_id)]
            ).send_notification()
        except BaseException as error:
            logger.error(error)
        sleep(settings.main_loop_delay)


if __name__ == "__main__":
    main()
