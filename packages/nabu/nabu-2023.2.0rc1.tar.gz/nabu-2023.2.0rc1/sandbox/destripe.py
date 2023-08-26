import scipy.ndimage as ndi
from scipy import interpolate

def detect_stripe(list_data, snr):
    """
    Locate stripe positions using Algorithm 4 in Ref. [1]

    Parameters
    ----------
    list_data : array_like
        1D array. Normalized data.
    snr : float
        Ratio (>1.0) for stripe detection. Greater is less sensitive.

    Returns
    -------
    array_like
        1D binary mask.

    References
    ----------
    [1] : https://doi.org/10.1364/OE.26.028396
    """
    npoint = len(list_data)
    list_sort = np.sort(list_data)
    xlist = np.arange(0, npoint, 1.0)
    ndrop = np.int16(0.25 * npoint)
    (slope, intercept) = np.polyfit(xlist[ndrop:-ndrop - 1],
                                    list_sort[ndrop:-ndrop - 1], 1)[:2]
    y_end = intercept + slope * xlist[-1]
    noise_level = np.abs(y_end - intercept)
    if noise_level < 1.0e-5:
        raise ValueError("The method doesn't work on noise-free data. If you "
                         "apply the method on simulated data, please add"
                         " noise!")
    val1 = np.abs(list_sort[-1] - y_end) / noise_level
    val2 = np.abs(intercept - list_sort[0]) / noise_level
    list_mask = np.zeros(npoint, dtype=np.float32)
    if val1 >= snr:
        upper_thresh = y_end + noise_level * snr * 0.5
        list_mask[list_data > upper_thresh] = 1.0
    if val2 >= snr:
        lower_thresh = intercept - noise_level * snr * 0.5
        list_mask[list_data <= lower_thresh] = 1.0
    return list_mask


def sort_forward(mat, axis=0):
    """
    Sort gray-scales of an image along an axis.
    e.g. axis=0 is to sort along each column.

    Parameters
    ----------
    mat : array_like
        2D array.
    axis : int
        Axis along which to sort.

    Returns
    --------
    mat_sort : array_like
        2D array. Sorted image.
    mat_index : array_like
        2D array. Index array used for sorting backward.
    """
    if axis == 0:
        mat = np.transpose(mat)
    (nrow, ncol) = mat.shape
    list_index = np.arange(0.0, ncol, 1.0)
    mat_index = np.tile(list_index, (nrow, 1))
    mat_comb = np.asarray(np.dstack((mat_index, mat)))
    mat_comb_sort = np.asarray(
        [row[row[:, 1].argsort()] for row in mat_comb])
    mat_sort = mat_comb_sort[:, :, 1]
    mat_index = mat_comb_sort[:, :, 0]
    if axis == 0:
        mat_sort = np.transpose(mat_sort)
        mat_index = np.transpose(mat_index)
    return mat_sort, mat_index


def sort_backward(mat, mat_index, axis=0):
    """
    Sort gray-scales of an image using an index array provided.
    e.g. axis=0 is to sort each column.

    Parameters
    ----------
    mat : array_like
        2D array.
    mat_index : array_like
        2D array. Index array used for sorting.
    axis : int
        Axis along which to sort.

    Returns
    --------
    mat_sort : array_like
        2D array. Sorted image.
    """
    if axis == 0:
        mat = np.transpose(mat)
        mat_index = np.transpose(mat_index)
    mat_comb = np.asarray(np.dstack((mat_index, mat)))
    mat_comb_sort = np.asarray(
        [row[row[:, 0].argsort()] for row in mat_comb])
    mat_sort = mat_comb_sort[:, :, 1]
    if axis == 0:
        mat_sort = np.transpose(mat_sort)
    return mat_sort



def remove_stripe_based_sorting(sinogram, size=21, dim=1, **options):
    """
    Remove stripe artifacts in a sinogram using the sorting technique,
    algorithm 3 in Ref. [1]. Angular direction is along the axis 0.

    Parameters
    ----------
    sinogram : array_like
        2D array. Sinogram image.
    size : int
        Window size of the median filter.
    dim : {1, 2}, optional
        Dimension of the window.
    options : dict, optional
        Use another smoothing filter rather than the median filter.
        E.g. options={"method": "gaussian_filter", "para1": (1,21)}

    Returns
    -------
    array_like
        2D array. Stripe-removed sinogram.

    References
    ----------
    [1] : https://doi.org/10.1364/OE.26.028396
    """
    msg = "\n Please use the dictionary format: options={'method':" \
          " 'filter_name', 'para1': parameter_1, 'para2': parameter_2}"
    sino_sort, sino_index = sort_forward(np.float32(sinogram), axis=0)
    if len(options) == 0:
        if dim == 2:
            sino_sort = ndi.median_filter(sino_sort, (size, size))
        else:
            sino_sort = ndi.median_filter(sino_sort, (1, size))
    else:
        for opt_name in options:
            opt = options[opt_name]
            if not isinstance(opt, dict):
                raise ValueError(msg)
            method = tuple(opt.values())[0]
            para = tuple(opt.values())[1:]
            sino_sort = getattr(ndi, method)(sino_sort, *para)

    return sort_backward(sino_sort, sino_index, axis=0)





def remove_large_stripe(sinogram, snr=3.0, size=51, drop_ratio=0.1, norm=True,
                        **options):
    """
    Remove large stripe artifacts in a sinogram, algorithm 5 in Ref. [1].
    Angular direction is along the axis 0.

    Parameters
    ----------
    sinogram : array_like
        2D array. Sinogram image
    snr : float
        Ratio (>1.0) for stripe detection. Greater is less sensitive.
    size : int
        Window size of the median filter.
    drop_ratio : float, optional
        Ratio of pixels to be dropped, which is used to reduce
        the possibility of the false detection of stripes.
    norm : bool, optional
        Apply normalization if True.
    options : dict, optional
        Use another smoothing filter rather than the median filter.
        E.g. options={"method": "gaussian_filter", "para1": (1,21))}.

    Returns
    -------
    array_like
        2D array. Stripe-removed sinogram.

    References
    ----------
    [1] : https://doi.org/10.1364/OE.26.028396
    """
    msg = "\n Please use the dictionary format: options={'method':" \
          " 'filter_name', 'para1': parameter_1, 'para2': parameter_2}"
    sinogram = np.copy(np.float32(sinogram))
    drop_ratio = np.clip(drop_ratio, 0.0, 0.8)
    (nrow, ncol) = sinogram.shape
    ndrop = int(0.5 * drop_ratio * nrow)
    sino_sort, sino_index = sort_forward(sinogram, axis=0)
    if len(options) == 0:
        sino_smooth = ndi.median_filter(sino_sort, (1, size))
    else:
        sino_smooth = np.copy(sino_sort)
        for opt_name in options:
            opt = options[opt_name]
            if not isinstance(opt, dict):
                raise ValueError(msg)
            method = tuple(opt.values())[0]
            para = tuple(opt.values())[1:]

            sino_smooth = getattr(ndi, method)(sino_smooth, *para)

    list1 = np.mean(sino_sort[ndrop:nrow - ndrop], axis=0)
    list2 = np.mean(sino_smooth[ndrop:nrow - ndrop], axis=0)
    list_fact = np.divide(list1, list2,
                          out=np.ones_like(list1), where=list2 != 0)
    list_mask = detect_stripe(list_fact, snr)
    list_mask = np.float32(ndi.binary_dilation(list_mask, iterations=1))
    if norm is True:
        sinogram = sinogram / np.tile(list_fact, (nrow, 1))
    sino_corr = sort_backward(sino_smooth, sino_index, axis=0)
    xlist_miss = np.where(list_mask > 0.0)[0]
    sinogram[:, xlist_miss] = sino_corr[:, xlist_miss]
    return sinogram




def remove_dead_stripe(sinogram, snr=3.0, size=51, residual=True,
                       smooth_strength=10):
    """
    Remove unresponsive or fluctuating stripe artifacts in a sinogram,
    algorithm 6 in Ref. [1]. Angular direction is along the axis 0.

    Parameters
    ----------
    sinogram : array_like
        2D array. Sinogram image.
    snr : float
        Ratio (>1.0) for stripe detection. Greater is less sensitive.
    size : int
        Window size of the median filter.
    residual : bool, optional
        Removing residual stripes if True.
    smooth_strength : int, optional
        Window size of the uniform filter used to detect stripes.

    Returns
    -------
    ndarray
        2D array. Stripe-removed sinogram.

    References
    ----------
    [1] : https://doi.org/10.1364/OE.26.028396
    """
    sinogram = np.copy(sinogram)
    (nrow, ncol) = sinogram.shape
    sino_smooth = np.apply_along_axis(ndi.uniform_filter1d, 0, sinogram,
                                      smooth_strength)
    list_diff = np.sum(np.abs(sinogram - sino_smooth), axis=0)
    list_diff_bck = ndi.median_filter(list_diff, size)
    nmean = np.mean(np.abs(list_diff_bck))
    list_diff_bck[list_diff_bck == 0.0] = nmean
    list_fact = list_diff / list_diff_bck
    list_mask = detect_stripe(list_fact, snr)
    list_mask = np.float32(ndi.binary_dilation(list_mask, iterations=1))
    list_mask[0:2] = 0.0
    list_mask[-2:] = 0.0
    xlist = np.where(list_mask < 1.0)[0]
    ylist = np.arange(nrow)
    finter = interpolate.RectBivariateSpline(ylist, xlist, sinogram[:, xlist],
                                             kx=1, ky=1)
    xlist_miss = np.where(list_mask > 0.0)[0]
    if (ncol // 3) > len(xlist_miss) > 0:
        x_mat_miss, y_mat = np.meshgrid(xlist_miss, ylist)
        output = finter.ev(np.ndarray.flatten(y_mat),
                           np.ndarray.flatten(x_mat_miss))
        sinogram[:, xlist_miss] = output.reshape(x_mat_miss.shape)
    if residual is True:
        sinogram = remove_large_stripe(sinogram, snr, size)
    return sinogram


def remove_all_stripe(sinogram, snr=3.0, la_size=51, sm_size=21,
                      drop_ratio=0.1, dim=1, **options):
    """
    Remove all types of stripe artifacts in a sinogram by combining algorithm
    6, 5, 4, and 3 in Ref. [1]. Angular direction is along the axis 0.

    Parameters
    ----------
    sinogram : array_like
        2D array. Sinogram image.
    snr : float
        Ratio (>1.0) for stripe detection. Greater is less sensitive.
    la_size : int
        Window size of the median filter to remove large stripes.
    sm_size : int
        Window size of the median filter to remove small-to-medium stripes.
    drop_ratio : float, optional
        Ratio of pixels to be dropped, which is used to reduce the possibility
        of the false detection of stripes.
    dim : {1, 2}, optional
        Dimension of the window.
    options : dict, optional
        Use another smoothing filter rather than the median filter.
        E.g. options={"method": "gaussian_filter", "para1": (1,21))}

    Returns
    -------
    array_like
        2D array. Stripe-removed sinogram.

    References
    ----------
    [1] : https://doi.org/10.1364/OE.26.028396
    """
    sinogram = remove_dead_stripe(sinogram, snr, la_size, residual=False)
    sinogram = remove_large_stripe(sinogram, snr, la_size, drop_ratio,
                                   **options)
    sinogram = remove_stripe_based_sorting(sinogram, sm_size, dim, **options)
    return sinogram
