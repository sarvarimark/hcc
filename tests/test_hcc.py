# pylint: disable=C0114
# pylint: disable=C0115
# pylint: disable=C0116
from unittest.mock import patch, Mock
from typing import Any, Optional
from hcc.hcc import Channel

call_count = 0

def mocked_requests_get(*args: Any, **kwargs: Any) -> Any:
    class MockResponse:
        def __init__(self, json_data: Optional[dict[str, str]], status_code: int):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    global call_count
    call_count += 1

    if args[0] == 'https://mockserver.com/success':
        return MockResponse({"key1": "value1"}, 200)
    if args[0] == 'https://mockserver.com/success_on_third_time':
        print(call_count)
        if call_count % 3 == 0:
            return MockResponse({"key1": "value1"}, 200)
        return MockResponse(None, 500)
    if args[0] == 'https://mockserver.com/succes_on_fifth_time':
        print(call_count)
        if call_count % 5 == 0:
            return MockResponse({"key1": "value1"}, 200)
        return MockResponse(None, 500)
    if args[0] == 'https://mockserver.com/fail':
        return MockResponse(None, 500)

def setup_function():
    global call_count
    call_count = 0

@patch('hcc.hcc.requests.get', side_effect=mocked_requests_get)
def test_channel_get_success(mock_get: Mock):
    channel = Channel(
        url="https://mockserver.com/success",
        timeout=1.0,
        max_retry_count=3
    )

    response = channel.get()
    assert response.status_code == 200
    assert mock_get.call_count == 1

@patch('hcc.hcc.requests.get', side_effect=mocked_requests_get)
def test_channel_get_fail(mock_get: Mock):
    channel = Channel(
        url="https://mockserver.com/fail",
        timeout=1.0,
        max_retry_count=3
    )

    response = channel.get()
    assert response.status_code == 500
    assert mock_get.call_count == 3

@patch('hcc.hcc.requests.get', side_effect=mocked_requests_get)
def test_channel_get_success_on_third_time(mock_get: Mock):
    channel = Channel(
        url="https://mockserver.com/success_on_third_time",
        timeout=1.0,
        max_retry_count=3
    )

    response = channel.get()
    assert response.status_code == 200
    assert mock_get.call_count == 3
