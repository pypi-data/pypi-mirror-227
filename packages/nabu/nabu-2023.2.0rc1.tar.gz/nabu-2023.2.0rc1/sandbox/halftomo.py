import numpy as np
from spire.utils import ims

def convert_halftomo(sino, rotation_axis_position):
    assert sino.ndim == 2
    assert (sino.shape[0] % 2) == 0
    na, nx = sino.shape
    na2 = na//2
    r = rotation_axis_position
    d = nx - r
    res = np.zeros((na2, 2*r), dtype="f")

    sino1 = sino[:na2, :]
    sino2 = sino[na2:, ::-1]
    res[:, :nx - d] = sino1[:, :nx - d]
    #
    w1 = np.linspace(0, 1, d, endpoint=True)
    res[:, nx-d:nx] = (1 - w1) * sino1[:, nx-d:] + w1 * sino2[:, d:2*d]
    #
    res[:, nx:] = sino2[:, 2*d:]

    return res

