from bisect import bisect_left
from typing import List, Union


def interp(
    time_value: Union[int, float],
    times: List[Union[int, float]],
    values: List[Union[int, float]],
) -> Union[int, float]:
    """Linear interpolation.
    Like numpy.interp, but for a single value.
    (And faster than numpy.interp for a single value.)
    """
    left_idx = bisect_left(times, time_value)
    if left_idx == 0:
        return values[0]
    elif left_idx == len(times):
        return values[-1]
    else:
        slope = (values[left_idx] - values[left_idx - 1]) / (
            times[left_idx] - times[left_idx - 1]
        )
        return values[left_idx - 1] + slope * (time_value - times[left_idx - 1])
