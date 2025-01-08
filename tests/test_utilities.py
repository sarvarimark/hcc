# pylint: disable=C0114
# pylint: disable=C0115
# pylint: disable=C0116
class Counter:
    count = 0

    @staticmethod
    def next():
        Counter.count += 1
        return Counter.count

    @staticmethod
    def reset():
        Counter.count = 0

def assert_runtime(expected_runtime: float, actual_runtime: float, tolerance: float = 0.05):
    assert (expected_runtime * (1 - tolerance) <= actual_runtime <=
            expected_runtime * (1 + tolerance))

def assert_runtime_interval(
    min_expected_runtime: float,
    max_expected_runtime: float,
    actual_runtime: float,
    tolerance: float = 0.05
):
    assert (min_expected_runtime * (1 - tolerance) <= actual_runtime <=
            max_expected_runtime * (1 + tolerance))
