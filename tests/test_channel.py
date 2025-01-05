# pylint: disable=C0114
# pylint: disable=C0115
# pylint: disable=C0116
from unittest.mock import patch, Mock
from hcc.channel import Channel

@patch('hcc.channel.requests.get')
def test_channel_get_success(mock_get: Mock):
    mock_get.side_effect = [
        Mock(status_code=200)
    ]

    channel = Channel(
        url = "https://mockserver.com/success",
        max_retry_count = 3
    )

    response = channel.get()
    assert response.status_code == 200
    assert mock_get.call_count == 1

@patch('hcc.channel.requests.get')
def test_channel_get_fail(mock_get: Mock):
    mock_get.side_effect = [
        Mock(status_code=500),
        Mock(status_code=500),
        Mock(status_code=500)
    ]

    channel = Channel(
        url="https://mockserver.com/fail",
        max_retry_count=3
    )

    response = channel.get()
    assert response.status_code == 500
    assert mock_get.call_count == 3

@patch('hcc.channel.requests.get')
def test_channel_get_success_on_third_time(mock_get: Mock):
    mock_get.side_effect = [
        Mock(status_code=500),
        Mock(status_code=500),
        Mock(status_code=200)
    ]

    channel = Channel(
        url="https://mockserver.com/success_on_third_time",
        max_retry_count=3
    )

    response = channel.get()
    assert response.status_code == 200
    assert mock_get.call_count == 3

@patch('hcc.channel.requests.post')
def test_channel_post_success(mock_post: Mock):
    mock_post.side_effect = [
        Mock(status_code=201)
    ]

    channel = Channel(
        url="https://mockserver.com/success",
        max_retry_count=3
    )

    response = channel.post(data={})
    assert response.status_code == 201
    assert mock_post.call_count == 1

@patch('hcc.channel.requests.post')
def test_channel_post_fail(mock_post: Mock):
    mock_post.side_effect = [
        Mock(status_code=500),
        Mock(status_code=500),
        Mock(status_code=500)
    ]

    channel = Channel(
        url="https://mockserver.com/fail",
        max_retry_count=3
    )

    response = channel.post(data={})
    assert response.status_code == 500
    assert mock_post.call_count == 3

@patch('hcc.channel.requests.post')
def test_channel_post_success_on_third_time(mock_post: Mock):
    mock_post.side_effect = [
        Mock(status_code=500),
        Mock(status_code=500),
        Mock(status_code=201)
    ]

    channel = Channel(
        url="https://mockserver.com/success_on_third_time",
        max_retry_count=3
    )

    response = channel.post(data={})
    assert response.status_code == 201
    assert mock_post.call_count == 3

@patch('hcc.channel.requests.put')
def test_channel_put_success(mock_put: Mock):
    mock_put.side_effect = [
        Mock(status_code=201)
    ]

    channel = Channel(
        url="https://mockserver.com/success",
        max_retry_count=3
    )

    response = channel.put(data={})
    assert response.status_code == 201
    assert mock_put.call_count == 1

@patch('hcc.channel.requests.put')
def test_channel_put_fail(mock_put: Mock):
    mock_put.side_effect = [
        Mock(status_code=500),
        Mock(status_code=500),
        Mock(status_code=500)
    ]

    channel = Channel(
        url="https://mockserver.com/fail",
        max_retry_count=3
    )

    response = channel.put(data={})
    assert response.status_code == 500
    assert mock_put.call_count == 3

@patch('hcc.channel.requests.put')
def test_channel_put_success_on_third_time(mock_put: Mock):
    mock_put.side_effect = [
        Mock(status_code=500),
        Mock(status_code=500),
        Mock(status_code=201)
    ]

    channel = Channel(
        url="https://mockserver.com/success_on_third_time",
        max_retry_count=3
    )

    response = channel.put(data={})
    assert response.status_code == 201
    assert mock_put.call_count == 3

@patch('hcc.channel.requests.delete')
def test_channel_delete_success(mock_delete: Mock):
    mock_delete.side_effect = [
        Mock(status_code=200)
    ]

    channel = Channel(
        url="https://mockserver.com/success",
        max_retry_count=3
    )

    response = channel.delete()
    assert response.status_code == 200
    assert mock_delete.call_count == 1

@patch('hcc.channel.requests.delete')
def test_channel_delete_fail(mock_delete: Mock):
    mock_delete.side_effect = [
        Mock(status_code=500),
        Mock(status_code=500),
        Mock(status_code=500)
    ]

    channel = Channel(
        url="https://mockserver.com/fail",
        max_retry_count=3
    )

    response = channel.delete()
    assert response.status_code == 500
    assert mock_delete.call_count == 3

@patch('hcc.channel.requests.delete')
def test_channel_delete_success_on_third_time(mock_delete: Mock):
    mock_delete.side_effect = [
        Mock(status_code=500),
        Mock(status_code=500),
        Mock(status_code=200)
    ]

    channel = Channel(
        url="https://mockserver.com/success_on_third_time",
        max_retry_count=3
    )

    response = channel.delete()
    assert response.status_code == 200
    assert mock_delete.call_count == 3
