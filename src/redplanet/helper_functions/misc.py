from contextlib import contextmanager
import time

import numpy as np



@contextmanager
def timer(message='', d=3):
    """
    A context manager that measures the time taken to execute the code block within it.

    Parameters
    ----------
    message : str, optional
        A message to display when the code block is executed, by default nothing.
    d : int, optional
        The number of decimal places to display in the elapsed time, by default 3.

    Examples
    --------
    >>> from redplanet.helper_functions.misc import timer
    >>> with timer('Elapsed time: '):
    ...     print(f'Sum of first 10^7 squared integers: {sum(x*x for x in range(10_000_000)):,}')

    Sum of first 10^7 squared integers: 333,333,283,333,335,000,000
    Elapsed time: 0.886 seconds
    """
    start = time.time()
    yield
    end = time.time()
    elapsed = end - start
    print(f"{message}{elapsed:.{d}f} seconds")



def find_closest_indices(
    sorted_array: np.ndarray,
    target_values: np.ndarray
) -> np.ndarray:
    """
    Find the indices of the closest elements in a sorted array for each target value.

    For each value in `target_values`, this function identifies the index of the element in `sorted_array` that is closest to it. In cases where a target value is exactly midway between two elements, the index of the left (smaller) element is returned.

    Parameters
    ----------
    sorted_array : np.ndarray
        A one-dimensional NumPy array sorted in ascending order. The array should contain numeric values.

    target_values : np.ndarray
        A one-dimensional NumPy array of target values for which to find the closest indices in `sorted_array`.

    Returns
    -------
    np.ndarray
        A one-dimensional NumPy array of integers, where each element is the index in `sorted_array` that is closest to the corresponding target value in `target_values`.


    Examples
    --------
    >>> import numpy as np
    >>> sorted_array = np.array([10, 20, 30, 40, 50])
    >>> target_values = np.array([25, 35, 5, 55])
    >>> find_closest_indices(sorted_array, target_values)
    array([1, 2, 0, 4])

    In this example:
    - For target `25`, the closest element is `20` at index `1`.
    - For target `35`, the closest element is `30` at index `2`.
    - For target `5`, the closest element is `10` at index `0`.
    - For target `55`, the closest element is `50` at index `4`.
    """
    insertion_indices = np.searchsorted(sorted_array, target_values)
    insertion_indices = np.clip(insertion_indices, 1, len(sorted_array) - 1)
    left_neighbors = sorted_array[insertion_indices - 1]
    right_neighbors = sorted_array[insertion_indices]
    closest_indices = np.where(
        np.abs(target_values - left_neighbors) <= np.abs(target_values - right_neighbors),
        insertion_indices - 1,
        insertion_indices
    )
    return closest_indices
