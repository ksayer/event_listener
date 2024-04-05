import requests


class TelegramNotifier:
    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id

    def send_message(self, msg: str):
        base_bot_url = "https://api.telegram.org/bot{}/".format(self.token)
        params = {'chat_id': self.chat_id, 'text': msg}
        url = ''.join([base_bot_url, 'sendMessage'])
        try:
            response = requests.post(url, data=params, timeout=3)
            if response.status_code != 200:
                raise ValueError(response.text)
        except Exception as error:
            print(f'Error sending telegram message: {error}. {error.args}')
            print(msg)
