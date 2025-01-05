# TODO add docs
# pylint: disable=C0114
# pylint: disable=C0115
# pylint: disable=C0116
from enum import Enum
from typing import Callable, Any
import math
import time
import random

class RetryPolicy(Enum):
    IMMEDIATE = 1
    LINEAR = 2
    JITTER = 3

def retry_function(
    func: Callable[[], Any],
    is_retry_needed: Callable[[Any], bool],
    max_retry_count: int | None,
    retry_policy: RetryPolicy = RetryPolicy.LINEAR,
    base_delay: int = 200,
) -> Any:
    _max_retry_count = max_retry_count if max_retry_count is not None else math.inf
    attempt = 0
    while True:
        result = func()
        if attempt == _max_retry_count - 1:
            return result
        if not is_retry_needed(result):
            return result
        attempt += 1
        base_delay_in_seconds = base_delay / 1000
        if retry_policy == RetryPolicy.IMMEDIATE:
            time.sleep(0.0)
        elif retry_policy == RetryPolicy.LINEAR:
            time.sleep(base_delay_in_seconds)
        elif retry_policy == RetryPolicy.JITTER:
            time.sleep(base_delay_in_seconds * random.uniform(0.5, 1.5))
