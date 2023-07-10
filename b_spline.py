from scipy import interpolate
import numpy as np


def generate_estimated_coords(x, y, n: int = 100):
    tck: tuple[np.ndarray, np.ndarray, int] = interpolate.splrep(x, y, s=0, k=3)  # type: ignore
    x_new = np.linspace(min(x), max(x), n)
    y_fit = interpolate.BSpline(*tck)(x_new)
    return [round(c, 4) for c in x_new], [round(c, 4) for c in y_fit]
