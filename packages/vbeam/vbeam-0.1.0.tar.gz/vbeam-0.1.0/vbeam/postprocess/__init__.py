from typing import Optional, Union

from vbeam.fastmath import numpy as np
from vbeam.interpolation import FastInterpLinspace


def coherence_factor(
    beamformed_data: np.ndarray,
    receivers_axis: int,
    num_active_elements: Optional[np.ndarray] = None,
):
    if num_active_elements is None:
        num_active_elements = beamformed_data.shape[receivers_axis]
    coherent_sum = np.abs(np.sum(beamformed_data, receivers_axis)) ** 2
    incoherent_sum = np.sum(np.abs(beamformed_data) ** 2, receivers_axis)
    return np.nan_to_num(coherent_sum / incoherent_sum / num_active_elements)


def normalized_decibels(data: np.ndarray):
    "Convert the data into decibels normalized for dynamic range."
    data_db = 20 * np.nan_to_num(np.log10(np.abs(data)))
    return data_db - data_db.max()


def upsample_by_interpolation(
    data: np.ndarray,
    n: Union[int, tuple],
    axis: Union[int, tuple, None] = None,
) -> np.ndarray:
    """Upsample the data along the given axes. Multiple axes may be given."""
    # No axis has been given: upsample all axes
    if axis is None:
        axis = tuple(range(data.ndim))

    # Multiple axes have been given: upsample each axis separately
    if isinstance(axis, tuple):
        if isinstance(n, int):
            n = (n,) * len(axis)
        # Upsample each axis separately
        for axis, _n in zip(axis, n):
            data = upsample_by_interpolation(data, _n, axis)
        return data  # ...and return the data that has been upsampled along all axes

    # Only one axis has been given: upsample that axis
    sample_indices = np.arange(n * data.shape[axis]) / n - (1 / (2 * n))
    data = np.swapaxes(data, axis, 0)
    interpolator = FastInterpLinspace(0, 1, data.shape[0])
    interpolated_data = interpolator.interp1d(
        sample_indices, data, left=data[0], right=data[-1]
    )
    return np.swapaxes(interpolated_data, 0, axis)
