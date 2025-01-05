# pylint: disable=C0114
# pylint: disable=C0115
# pylint: disable=C0116
import time
from hcc import retry_function, RetryPolicy

class Counter:
    count = 0

    @staticmethod
    def next():
        Counter.count += 1
        print(Counter.count)
        return Counter.count

    @staticmethod
    def reset():
        Counter.count = 0

def assert_runtime(expected_runtime: float, actual_runtime: float, tolerance: float = 0.1):
    assert (expected_runtime * (1 - tolerance) <= actual_runtime <=
            expected_runtime * (1 + tolerance))

def assert_runtime_interval(
    min_expected_runtime: float,
    max_expected_runtime: float,
    actual_runtime: float,
    tolerance: float = 0.1
):
    assert (min_expected_runtime * (1 - tolerance) <= actual_runtime <=
            max_expected_runtime * (1 + tolerance))

def setup_function():
    Counter.reset()

def test_retry_function_success_immediate():
    start_time = time.time()
    response = retry_function(
        func = Counter.next,
        is_retry_needed = lambda result: result < 3,
        retry_policy = RetryPolicy.IMMEDIATE,
        max_retry_count = 5,
        base_delay = 100,
    )
    end_time = time.time()
    assert response == 3
    assert end_time - start_time < 0.1

def test_retry_function_fail_immediate():
    start_time = time.time()
    response = retry_function(
        func = Counter.next,
        is_retry_needed = lambda result: result < 10,
        retry_policy = RetryPolicy.IMMEDIATE,
        max_retry_count = 5,
        base_delay = 100,
    )
    end_time = time.time()
    assert response == 5
    assert end_time - start_time < 0.1

def test_retry_function_success_linear():
    start_time = time.time()
    response = retry_function(
        func = Counter.next,
        is_retry_needed = lambda result: result < 3,
        retry_policy = RetryPolicy.LINEAR,
        max_retry_count = 5,
        base_delay = 100,
    )
    end_time = time.time()
    assert response == 3
    assert_runtime(0.2, end_time - start_time)

def test_retry_function_fail_linear():
    start_time = time.time()
    response = retry_function(
        func = Counter.next,
        is_retry_needed = lambda result: result < 10,
        retry_policy = RetryPolicy.LINEAR,
        max_retry_count = 5,
        base_delay = 100,
    )
    end_time = time.time()
    assert response == 5
    assert_runtime(0.4, end_time - start_time)

def test_retry_function_success_jitter():
    start_time = time.time()
    response = retry_function(
        func = Counter.next,
        is_retry_needed = lambda result: result < 3,
        retry_policy = RetryPolicy.JITTER,
        max_retry_count = 5,
        base_delay = 100,
    )
    end_time = time.time()
    assert response == 3
    assert_runtime_interval(0.2 * 0.5, 0.2 * 1.5, end_time - start_time)

def test_retry_function_fail_jitter():
    start_time = time.time()
    response = retry_function(
        func = Counter.next,
        is_retry_needed = lambda result: result < 10,
        retry_policy = RetryPolicy.JITTER,
        max_retry_count = 5,
        base_delay = 100,
    )
    end_time = time.time()
    assert response == 5
    assert_runtime_interval(0.4 * 0.5, 0.4 * 1.5, end_time - start_time)
