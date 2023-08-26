"""Implement a dummy ols function."""
import numpy as np
import numpy.typing as npt


n_obs = "n_obs"
n_vars = "n_vars"


def ols(
    y: npt.NDArray[np.floating], x: npt.NDArray[np.floating]
) -> npt.NDArray[np.floating]:
    """Dummy ordinary least squares function."""
    xtx = x.T @ x
    xty = x.T @ y
    return np.linalg.inv(xtx) @ xty
