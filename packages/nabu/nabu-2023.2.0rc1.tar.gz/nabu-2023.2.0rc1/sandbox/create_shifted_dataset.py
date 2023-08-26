import numpy as np
from scipy.ndimage import shift as ndshift
from nabu.preproc.shift import VerticalShift

def create_shifted_dataset(sinogram, n_z, shifts, **interp_kwargs):
    """
    From a 2D sinogram, create a collection of (2D) "projections" where shifts were applied in each dimension.

    Let (n_a, n_x) be the sinogram dimensions.

    Step 1: shift horizontally each sinogram row
    Step 2: create n_a images. On each image, insert the corresponding sinogram row.


    Parameters
    ----------
    sinogram: numpy.ndarray
        Sinogram image.
    n_z: int
        Number of rows in each resulting images
    shifts: numpy.ndarray
        Array containing the (X, Z) shifts (horizontal, vertical)
    """
    n_a, n_x = sinogram.shape
    assert shifts.ndim == 2
    assert shifts.shape[0] == n_a

    res = np.zeros((n_a, n_z, n_x), "f")
    middle = n_z //2

    shifter = VerticalShift(res.shape, -shifts[:, 1])

    for i in range(n_a):
        # Do the shift in two steps. First horizontal, then vertical.
        # This can (and should) be done because backprojector only interpolates along the X dimension
        # OK
        res[i][middle] = ndshift(sinogram[i], shifts[i, 0], **interp_kwargs)
        # Comes with lots of artefacts for half-pixel shifts. To be investigated. Use nabu.misc.shift.VerticalShift ?
        # res[i] = ndshift(res[i], (shifts[i, 1], 0))
    shifter.apply_vertical_shifts(res, np.arange(shifts.shape[0]))


    return res



from nxtomomill.nexus.nxtomo import NXtomo
from nxtomomill.utils import ImageKey


def create_nxtomo(projections, fname):
    n_a, n_z, n_x = projections.shape

    nxtomo = NXtomo("entry")
    nxtomo.instrument.detector.data = projections
    nxtomo.instrument.detector.image_key_control = [ImageKey.PROJECTION] * n_a
    nxtomo.sample.rotation_angle = np.linspace(0, 180, n_a, False)
    nxtomo.instrument.detector.field_of_view = "Full"
    nxtomo.instrument.detector.x_pixel_size = nxtomo.instrument.detector.y_pixel_size = 6.5 * 1e-6
    nxtomo.energy = 20.0 # keV
    nxtomo.instrument.detector.distance = 1.0 # meter

    nxtomo.save(file_path=fname, overwrite=True, nexus_path_version=1.1)


import sys
import os
from nabu.testutils import get_data
if __name__ == "__main__":

    # CASE = "vertical_linear"
    # CASE = "horizontal_linear"
    # CASE = "horizontal_random"
    # CASE = "horizontal_random"
    CASE = "vertical_horizontal_linear"
    # CASE = "vertical_horizontal_random"

    hshift_min = 0
    hshift_max = 120
    vshift_min = 0
    vshift_max = 30

    dirname = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()

    s = get_data("mri_sino500.npz")["data"]
    n_a, n_x = s.shape

    if CASE == "vertical_linear":
        shifts = np.vstack([np.zeros(n_a), np.linspace(vshift_min, vshift_max, n_a)]).T
    elif CASE == "horizontal_linear":
        shifts = np.vstack([np.linspace(hshift_min, hshift_max, n_a), np.zeros(n_a)]).T
    elif CASE == "vertical_horizontal_linear":
        shifts = np.vstack([np.linspace(hshift_min, hshift_max, n_a), np.linspace(vshift_min, vshift_max, n_a)]).T
    else:
        raise NotImplementedError()

    n_z = 100
    print("Creating projections - dataset shape=(%d, %d, %d)" % (n_a, n_z, n_x))
    projs = create_shifted_dataset(s, n_z, shifts)
    print("Creating NXTomo file")
    create_nxtomo(projs, dirname + "/%s.nx" % CASE)
    print("Writing translations file")
    np.savetxt(dirname + "/%s.txt" % CASE, shifts)



