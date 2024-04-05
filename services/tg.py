import logging
import requests


logger = logging.getLogger(__name__)


class TelegramNotifier:
    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id

    def send_message(self, msg: str) -> bool:
        base_bot_url = f"https://api.telegram.org/bot{self.token}/"
        params = {'chat_id': self.chat_id, 'text': msg}
        url = f"{base_bot_url}sendMessage"
        try:
            response = requests.post(url, data=params, timeout=3)
            if response.status_code == 200:
                print(msg)
                return True
            logger.error(f'Error sending telegram message: '
                         f'{response.status_code}. {response.text}\n{msg}')
        except requests.exceptions.RequestException as error:
            logger.error(f'Error sending telegram message: '
                         f'{error}. {error.args}\n{msg}')
        return False
