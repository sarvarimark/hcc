# TODO add logs
# TODO add docs
# pylint: disable=C0114
# pylint: disable=C0115
# pylint: disable=C0116
from enum import Enum
from typing import Callable, Any
import time
import random

class RetryPolicy(Enum):
    IMMEDIATE = 1
    LINEAR = 2
    JITTER = 3

def retry_function(
    func: Callable[[], Any],
    is_retry_needed: Callable[[Any], bool],
    max_retry_count: int,
    retry_policy: RetryPolicy = RetryPolicy.LINEAR,
    base_delay: int = 200,
) -> Any:
    attempt = 0
    while True:
        result = func()
        if attempt == max_retry_count - 1:
            return result
        if not is_retry_needed(result):
            return result
        attempt += 1
        delay(retry_policy, base_delay)

def retry_function_infinite(
    func: Callable[[], Any],
    is_retry_needed: Callable[[Any], bool],
    retry_policy: RetryPolicy = RetryPolicy.LINEAR,
    base_delay: int = 200,
) -> Any:
    while True:
        result = func()
        if not is_retry_needed(result):
            return result
        delay(retry_policy, base_delay)

def delay(retry_policy: RetryPolicy, base_delay: int) -> None:
    base_delay_in_seconds = base_delay / 1000
    if retry_policy == RetryPolicy.IMMEDIATE:
        time.sleep(0.0)
    elif retry_policy == RetryPolicy.LINEAR:
        time.sleep(base_delay_in_seconds)
    elif retry_policy == RetryPolicy.JITTER:
        time.sleep(base_delay_in_seconds * random.uniform(0.5, 1.5))
