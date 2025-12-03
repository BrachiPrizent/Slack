from unittest.mock import patch, MagicMock
import src.app

@patch("src.app.requests.post")
def test_send_slack_message(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "ok"
    mock_post.return_value = mock_response

    src.app.send_slack_message("Hello")
    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args
    assert kwargs["json"]["text"] == "Hello"

@patch("src.app.WebClient")
def test_get_list_of_users(mock_client_class):
    mock_client = MagicMock()
    mock_client.users_list.return_value = {
        "members": [
            {"id": "U1", "name": "Alice", "profile": {"email": "alice@test.com"}, "is_bot": False, "deleted": False},
            {"id": "U2", "name": "Bot", "profile": {"email": "bot@test.com"}, "is_bot": True, "deleted": False},
        ]
    }
    mock_client_class.return_value = mock_client
    src.app.get_list_of_users(mock_client)
    mock_client.users_list.assert_called_once()

@patch("src.app.WebClient")
def test_get_list_of_channels(mock_client_class):
    mock_client = MagicMock()
    mock_client.conversations_list.return_value = {
        "channels": [
            {"id": "C1", "name": "general"},
            {"id": "C2", "name": "random"},
        ]
    }
    mock_client_class.return_value = mock_client
    src.app.get_list_of_channels(mock_client)
    mock_client.conversations_list.assert_called_once()

@patch("src.app.send_slack_message")
@patch("src.app.WebClient")
def test_main_with_message(mock_client_class, mock_send):
    mock_client = MagicMock()
    mock_client_class.return_value = mock_client
    test_args = ["-m", "Hello from test"]
    src.app.main(test_args)
    mock_send.assert_called_once_with("Hello from test")
