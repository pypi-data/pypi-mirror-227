from typing import Any, List, Tuple

import numpy as np

import pct_tools_ext


def compute_ATAx(x: np.ndarray[Any, np.float32], filenames: List[str]) -> np.ndarray[Any, np.float32]:
    """Compute the multiplication A.T * A * x.

    Args:
        x: A column vector of shape (m, 1).
        filenames: The filenames of the matrices.

    Returns:
        The resulting vector of shape (m, 1) of the multiplication A.T * A * x.
    """
    return pct_tools_ext.compute_ATAx(x, filenames)
