# pylint: disable=C0114
# pylint: disable=C0115
# pylint: disable=C0116
from unittest.mock import patch, Mock
from hcc.hcc import Channel

@patch('hcc.hcc.requests.get')
def test_channel_get_success(mock_get: Mock):
    mock_get.side_effect = [
        Mock(status_code=200, json_data={"key1": "value1"})
    ]

    channel = Channel(
        url="https://mockserver.com/success",
        timeout=1.0,
        max_retry_count=3
    )

    response = channel.get()
    assert response.status_code == 200
    assert mock_get.call_count == 1

@patch('hcc.hcc.requests.get')
def test_channel_get_fail(mock_get: Mock):
    mock_get.side_effect = [
        Mock(status_code=500, json_data=None),
        Mock(status_code=500, json_data=None),
        Mock(status_code=500, json_data=None)
    ]

    channel = Channel(
        url="https://mockserver.com/fail",
        timeout=1.0,
        max_retry_count=3
    )

    response = channel.get()
    assert response.status_code == 500
    assert mock_get.call_count == 3

@patch('hcc.hcc.requests.get')
def test_channel_get_success_on_third_time(mock_get: Mock):
    mock_get.side_effect = [
        Mock(status_code=500, json_data=None),
        Mock(status_code=500, json_data=None),
        Mock(status_code=200, json_data={"key1": "value1"})
    ]

    channel = Channel(
        url="https://mockserver.com/success_on_third_time",
        timeout=1.0,
        max_retry_count=3
    )

    response = channel.get()
    assert response.status_code == 200
    assert mock_get.call_count == 3
