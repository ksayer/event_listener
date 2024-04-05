from time import sleep

from services.monitor_events import monitor_total_distribution_events
from services.notification import NotificationDistributor
from services.tg import TelegramNotifier


def main():
    while True:
        monitor_total_distribution_events()
        NotificationDistributor(notification_services=[TelegramNotifier()]).send_notification()
        sleep(5)


if __name__ == "__main__":
    main()
