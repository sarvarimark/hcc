"""Retry module for retrying functions with different policies."""
from enum import Enum
from typing import Callable, Any, Optional
import math
import time
import random

class RetryPolicy(Enum):
    """The RetryPolicy enum defines the possible values for the retry policy.
    
    The possible values are:
        IMMEDIATE: Retry immediately.
        LINEAR: Retry with a linear delay, which is equal to the base_delay.
        JITTER: Retry with a jitter delay, which is a random value
                between 0.5 and 1.5 times the base_delay.
    """
    IMMEDIATE = 1
    LINEAR = 2
    JITTER = 3

def retry_function(
    func: Callable[[], Any],
    is_retry_needed: Callable[[Any], bool],
    max_retry_count: Optional[int] = None,
    retry_policy: Optional[RetryPolicy] = RetryPolicy.LINEAR,
    base_delay: Optional[int] = 200,
) -> Any:
    """Retry a function with different policies.

    Args:
        func: The function to be retried.
        is_retry_needed: The function that determines if a retry is needed.
        max_retry_count: The maximum number of retries (default is None).
                         If set to None, there is no limit on the number of retries.
        retry_policy: The retry policy (default is RetryPolicy.LINEAR).
        base_delay: The base delay in milliseconds (default is 200).

    Returns:
        The result of the function after the first successful call or the last call.
            
    Raises:
        Exception: If the maximum retry count is reached and the function still fails.
    """
    _max_retry_count = max_retry_count if max_retry_count is not None else math.inf
    _base_delay = base_delay if base_delay is not None else 200
    _base_delay_in_seconds = _base_delay / 1000
    attempt = 0
    while True:
        attempt += 1
        try:
            result = func()
        except Exception as e:   # pylint: disable=broad-exception-caught
            if attempt == _max_retry_count:
                raise e
        else:
            if attempt == _max_retry_count:
                return result
            if not is_retry_needed(result):
                return result
        if attempt < _max_retry_count:
            if retry_policy == RetryPolicy.IMMEDIATE:
                pass
            elif retry_policy == RetryPolicy.LINEAR:
                time.sleep(_base_delay_in_seconds)
            elif retry_policy == RetryPolicy.JITTER:
                time.sleep(_base_delay_in_seconds * random.uniform(0.5, 1.5))
