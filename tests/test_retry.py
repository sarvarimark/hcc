# pylint: disable=C0114
# pylint: disable=C0115
# pylint: disable=C0116
import time
import pytest
from hcc.retry import retry_function, RetryPolicy
from .test_utilities import Counter, assert_runtime

def setup_function():
    Counter.reset()

def test_retry_function_with_exceptions_fail():
    Counter.reset()
    max_retries = 3
    base_delay = 100

    def always_fail():
        Counter.next()
        raise Exception("Always fail") # pylint: disable=broad-exception-raised

    start_time = time.time()
    with pytest.raises(Exception, match="Always fail"):
        retry_function(
            func=always_fail,
            is_retry_needed=lambda x: True,
            max_retry_count=max_retries,
            retry_policy=RetryPolicy.LINEAR,
            base_delay=base_delay
        )
    end_time = time.time()

    expected_runtime = (max_retries - 1) * (base_delay / 1000)
    actual_runtime = end_time - start_time

    assert Counter.count == max_retries
    assert_runtime(expected_runtime, actual_runtime)

def test_retry_function_with_exceptions_eventual_success():
    Counter.reset()
    max_retries = 5
    base_delay = 100

    def succeed_on_third_time():
        val = Counter.next()
        if val == 3:
            return val
        raise Exception("Fail on first two attempts") # pylint: disable=broad-exception-raised

    start_time = time.time()
    response = retry_function(
        func=succeed_on_third_time,
        is_retry_needed=lambda x: False,  # Exceptions are always retried
        max_retry_count=max_retries,
        retry_policy=RetryPolicy.LINEAR,
        base_delay=base_delay
    )
    end_time = time.time()

    assert response == 3
    assert_runtime(2 * (base_delay / 1000), end_time - start_time)
