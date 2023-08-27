from typing import List, Union

from lr_schedules.interp import interp


class LinearScheduler:
    """
    Performs linear interpolation between pairs of (time, value).
    """

    def __init__(
        self,
        times: List[Union[int, float]],
        values: List[Union[int, float]],
        total_training_steps: int = None,
    ):
        """
        Initializes the LinearScheduler.

        Args:
            times: List of times. If values are between 0 and 1, they are interpreted as
                fractions of total_training_steps. In this case, total_training_steps must be provided.
                Otherwise, can be absolute values, e.g. [0, 100, 200, etc.]

            values: List of values corresponding to the times.
            total_training_steps: Total number of training steps.

        Raises:
            AssertionError: If times are not in ascending order, or if times and values do not have the same length.
        """
        if total_training_steps is None:
            assert not (0 <= min(times) <= max(times) <= 1), (
                "If times contain values between 0 and 1, they are interpreted as fractions "
                "of total_training_steps. In this case, total_training_steps must be provided."
            )
        assert all(
            times[i] <= times[i + 1] for i in range(len(times) - 1)
        ), "`times` must be in ascending order"
        assert len(times) == len(values), "`times` and `values` must have the same length"

        self.times = times
        self.values = values
        self.total_training_steps = (
            total_training_steps if total_training_steps is not None else 1
        )

    def __call__(self, step: int) -> Union[int, float]:
        """
        Computes the interpolated value for a given step.

        Args:
            step: The current step.

        Returns:
            The interpolated value.
        """
        return interp(step / self.total_training_steps, self.times, self.values)
