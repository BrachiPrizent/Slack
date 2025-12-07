from unittest.mock import patch, MagicMock
from  src.connecting_to_slack import send_slack_message, get_list_of_channels, get_list_of_users

@patch("src.connecting_to_slack.requests.post")
def test_send_slack_message(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "ok"
    mock_post.return_value = mock_response

    send_slack_message("Hello")
    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args
    assert kwargs["json"]["text"] == "Hello"

@patch("src.connecting_to_slack.WebClient")
def test_get_list_of_users(mock_client_class):
    mock_client = MagicMock()
    mock_client.users_list.return_value = {
        "members": [
            {"id": "U1", "name": "Alice", "profile": {"email": "alice@test.com"}, "is_bot": False, "deleted": False},
            {"id": "U2", "name": "Bot", "profile": {"email": "bot@test.com"}, "is_bot": True, "deleted": False},
        ]
    }
    mock_client_class.return_value = mock_client
    get_list_of_users(mock_client)
    mock_client.users_list.assert_called_once()

@patch("src.connecting_to_slack.WebClient")
def test_get_list_of_channels(mock_client_class):
    mock_client = MagicMock()
    mock_client.conversations_list.return_value = {
        "channels": [
            {"id": "C1", "name": "general"},
            {"id": "C2", "name": "random"},
        ]
    }
    mock_client_class.return_value = mock_client
    get_list_of_channels(mock_client)
    mock_client.conversations_list.assert_called_once()
