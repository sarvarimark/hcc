# TODO add logs
# TODO add docs
# pylint: disable=C0114
# pylint: disable=C0115
# pylint: disable=C0116
# TODO default value
# pylint: disable=W0102
import requests
from .retry import retry_function

class Channel:
    def __init__(self, url: str, timeout: float, max_retry_count: int):
        self.url = url
        self.timeout = timeout
        self.max_retry_count = max_retry_count
        self.success_status_codes = [200, 201]

    def get(self, params: dict[str, str] = {}, headers: dict[str, str] = {}) -> requests.Response:
        return retry_function(
            func = lambda: requests.get(
                self.url, timeout=self.timeout, params=params, headers=headers
            ),
            is_retry_needed = lambda response:
                response.status_code not in self.success_status_codes,
            max_retry_count = self.max_retry_count,
        )

    def post(self, data: dict[str, str] = {}, headers: dict[str, str] = {}) -> requests.Response:
        return retry_function(
            func = lambda: requests.post(
                self.url, timeout=self.timeout, data=data, headers=headers
            ),
            is_retry_needed = lambda response:
                response.status_code not in self.success_status_codes,
            max_retry_count = self.max_retry_count,
        )

    def put(self, data: dict[str, str] = {}, headers: dict[str, str] = {}) -> requests.Response:
        return retry_function(
            func = lambda: requests.put(
                self.url, timeout=self.timeout, data=data, headers=headers
            ),
            is_retry_needed = lambda response:
                response.status_code not in self.success_status_codes,
            max_retry_count = self.max_retry_count,
        )

    def delete(self, headers: dict[str, str] = {}) -> requests.Response:
        return retry_function(
            func = lambda: requests.delete(
                self.url, timeout=self.timeout, headers=headers
            ),
            is_retry_needed = lambda response:
                response.status_code not in self.success_status_codes,
            max_retry_count = self.max_retry_count,
        )

if __name__ == "__main__":
    channel = Channel(
        url = "https://jsonplaceholder.typicode.com/todos/9999",
        timeout = 1.0,
        max_retry_count = 3
    )
    response = channel.get()
    print(response.json())
