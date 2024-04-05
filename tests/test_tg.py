import pytest
from unittest.mock import patch, MagicMock

from services.tg import TelegramNotifier


# Тест на успешную отправку сообщения
@patch('services.tg.requests.post')
def test_send_message_success(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_post.return_value = mock_response

    notifier = TelegramNotifier(token="fake_token", chat_id="fake_chat_id")
    try:
        result = notifier.send_message("Test message")
        assert result is True
    except Exception as e:
        pytest.fail(f"Unexpected exception raised: {e}")


@patch('services.tg.requests.post')
def test_send_message_failure(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.text = "Bad request"
    mock_post.return_value = mock_response

    notifier = TelegramNotifier(token="fake_token", chat_id="fake_chat_id")
    result = notifier.send_message("Test message")
    assert result is False
