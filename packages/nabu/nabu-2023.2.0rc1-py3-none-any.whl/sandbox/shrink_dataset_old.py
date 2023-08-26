import numpy as np
from multiprocessing.pool import ThreadPool
from tomoscan.io import HDF5File
from tomoscan.esrf import HDF5TomoScan
from tomoscan.esrf.scan.utils import get_compacted_dataslices
from nxtomomill.nexus import NXtomo
from ..misc.binning import binning as image_binning


def read_compacted_frames(frames_urls, shape, dtype):
    frames_urls = get_compacted_dataslices(frames_urls)
    frames_idx = sorted(frames_urls.keys())
    res = np.zeros((len(frames_idx),) + shape, dtype=dtype)

    first_frame_url = frames_urls[frames_idx[0]]
    fdesc = HDF5File(first_frame_url.file_path(), "r")

    read = {}
    n_frames = 0
    for frame_idx in frames_idx:
        url = frames_urls[frame_idx]
        data_slice = url.data_slice()
        (s, e) = (data_slice.start, data_slice.stop)
        if read.get((s, e), False) == True:
            continue
        res[n_frames:n_frames + (e-s), ...] = fdesc[url.data_path()][s:e, ...]
        n_frames += e-s
        read[(s, e)] = True
    fdesc.close()
    return res


def get_dataset_dtype(scan):
    data_url = scan.projections[sorted(scan.projections.keys())[0]]
    with HDF5File(data_url.file_path(), "r") as f:
        dtype = f[data_url.data_path()].dtype
    return dtype


def shrink_dataset(data_path, binning, subsampling, entry=None, n_threads=1):
    scan = HDF5TomoScan(data_path, entry=entry)

    frame_shape = (scan.dim_2, scan.dim_1)
    frame_dtype = get_dataset_dtype(scan)


    def _apply_binning(img_res_tuple):
        img, res = img_res_tuple
        res[:] = image_binning(img, binning)

    res = []
    for frames in [scan.projections, scan.flats, scan.darks]:
        data = read_compacted_frames(frames, frame_shape, frame_dtype)
        if subsampling is not None and subsampling > 1:
            data = data[::subsampling]
        if binning is not None:
            data_binned = np.zeros((data.shape[0], data.shape[1]//binning[0], data.shape[2]//binning[1]), data.dtype)
            with ThreadPool(n_threads) as tp:
                tp.map(_apply_binning, zip(data, data_binned))
            data = data_binned
        res.append(data)
    projections, flats, darks = res


    nxtomo = NXtomo()

    nxtomo.control = srcurrent # ??

    'end_time',
    'energy',
 'instrument',
 'is_root',
 'load',
 'node_name',
 'parent',
 'path',
 'root_path',
 'sample',
 'save',
 'start_time',
 'sub_select_from_angle_offset',
 'sub_select_selection_from_angle_range',
 'title',
 'to_nx_dict'








"""

 'alignment_projections', # {}
 'count_time', # len(t.flats) + len(t.projections) + len(t.darks)
 'dim_1',
 'dim_2',
 'distance',
 'electric_current',
 'end_time',
 'energy',
 'entry',
 'equal',
 'estimated_cor_frm_motor',
 'exposure_time',
 'ff_interval',
 'field_of_view',
 'flat_field_correction',
 'flat_n',
 'flats',
 'frames',
 'from_dict',
 'from_identifier',
 'get_bounding_box',
 'get_dark_expected_location',
 'get_dataset_basename',
 'get_detector_data_path',
 'get_distance',
 'get_distance_expected_location',
 'get_energy_expected_location',
 'get_flat_expected_location',
 'get_identifier',
 'get_master_file',
 'get_pixel_size',
 'get_pixel_size_expected_location',
 'get_proj_angle_url',
 'get_projection_expected_location',
 'get_projections_intensity_monitor',
 'get_relative_file',
 'get_sinogram',
 'get_valid_entries',
 'get_volume_output_file_name',
 'get_x_flipped',
 'get_y_flipped',
 'group_size',
 'ignore_projections',
 'image_key',
 'image_key_control',
 'instrument_name',
 'intensity_monitor',
 'intensity_normalization',
 'is_abort',
 'is_tomoscan_dir',
 'load_from_dict',
 'load_reduced_darks',
 'load_reduced_flats',
 'magnification',
 'map_urls_on_scan_range',
 'master_file',
 'nexus_path',
 'nexus_version',
 'node_is_nxtomo',
 'normed_darks',
 'normed_flats',
 'path',
 'pixel_size',
 'projections',
 'projections_compacted',
 'reduced_darks',
 'reduced_darks_infos',
 'reduced_flats',
 'reduced_flats_infos',
 'return_projs',
 'rotation_angle',
 'sample_name',
 'save_reduced_darks',
 'save_reduced_flats',
 'scan_range',
 'sequence_name',
 'set_normed_darks',
 'set_normed_flats',
 'set_reduced_darks',
 'set_reduced_flats',
 'source',
 'source_name',
 'source_type',
 'start_time',
 'to_dict',
 'tomo_n',
 'type',
 'update',
 'x_flipped',
 'x_pixel_size',
 'x_translation',
 'y_flipped',
 'y_pixel_size',
 'y_translation',
 'z_translation']

 """
