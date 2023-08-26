#!/usr/bin/env python

import numpy as np
from time import time
from nabu.resources.dataset_analyzer import EDFDatasetAnalyzer
from nabu.resources.dataset_validator import NabuValidator
from nabu.io.config import NabuConfigParser, validate_nabu_config
from nabu.io.reader import ChunkReader
from nabu.preproc.ccd_cuda import CudaFlatField, CudaCCDCorrection, CudaLog
from nabu.preproc.phase_cuda import CudaPaganinPhaseRetrieval
from nabu.reconstruction.fbp import Backprojector
from nabu.misc.unsharp_cuda import CudaUnsharpMask

import pycuda.gpuarray as garray
import pycuda.autoinit

# Extract informations from dataset location
E = EDFDatasetAnalyzer("/home/pierre/tmp/5.06_crayon_W150_60_Al2_W0.25_xc1000_")
if len(E.projections) == 0:
    print("No projections found in the scanned dataset")
    exit()
# Read and validate user config file
conf = NabuConfigParser("/home/pierre/tmp/nabu2.conf").conf_dict
nabu_config = validate_nabu_config(conf)
# Build the final nabu processing configuration
V = NabuValidator(nabu_config, E)
V.perform_all_checks()
V.remove_unused_radios() # modifies "E"

# Read a chunk of radios
print("Reading chunk")
t0 = time()
sub_region = (None, None, None, 100)
chunk_reader = ChunkReader(E.projections, sub_region=sub_region)
chunk_reader.load_files()
radios = chunk_reader.files_data.astype("f")
n_angles, n_z, n_x = radios.shape
print("OK (%.3f s)" % (time() - t0))


# transfer the chunk on GPU
d_radios = garray.to_gpu(radios)

# Flat-field
print("Doing flat-field")
t0 = time()
cuda_flatfield = CudaFlatField(d_radios, E.flats, E.darks, sub_region=sub_region)
cuda_flatfield.normalize_radios()
print("OK (%.3f s)" % (time() - t0))


# CCD correction (median-clip)
print("Doing CCD correction")
t0 = time()
cuda_ccd = CudaCCDCorrection(d_radios)
d_radios_corr = garray.zeros_like(d_radios)
cuda_ccd.median_clip_correction(output=d_radios_corr)
print("OK (%.3f s)" % (time() - t0))

# Paganin
print("Doing Paganin")
t0 = time()
cudapaganin = CudaPaganinPhaseRetrieval(
    (n_z, n_x),
    distance=E.distance * 1e2,
    energy=E.energy,
    delta_beta=nabu_config["phase"]["paganin_delta_beta"],
    pixel_size=E.pixel_size
)
for i in range(E.n_angles):
    cudapaganin.apply_filter(d_radios_corr[i], output=d_radios[i])
print("OK (%.3f s)" % (time() - t0))

"""
# Unsharp
print("Doing unsharp")
t0 = time()
if 0:
    cuda_unsharp = CudaUnsharpMask(d_radios.shape, 1.0, 5.)
    cuda_unsharp.unsharp(d_radios, output=d_radios_corr)
else:
    cuda_unsharp = CudaUnsharpMask((n_z, n_x), 1.0, 5.)
    for i in range(E.n_angles):
        cuda_unsharp.unsharp(d_radios[i], d_radios_corr[i])
print("OK (%.3f s)" % (time() - t0))
"""

# Log
print("Doing Logarithm")
t0 = time()
cuda_log = CudaLog(d_radios, clip_min=0.01)
cuda_log.take_logarithm(output=d_radios)
print("OK (%.3f s)" % (time() - t0))


# Reconstruction
d_recs = garray.zeros((n_z, n_x, n_x), dtype="f")
print("Doing reconstruction")
t0 = time()
cudafbp = Backprojector(
    (n_angles, n_x),
    rot_center=nabu_config["reconstruction"]["rotation_axis_position"],
    extra_options={"padding_mode": "edges"}
)
for i in range(n_z):
    d_recs[i] = cudafbp.fbp(d_radios[:, i, :]) # TODO transpose ?
print("OK (%.3f s)" % (time() - t0))


recs = d_recs.get()

# Post-processing (here with numpy)
print("Clip to inner circle")
from nabu.utils import clip_circle
for i in range(n_z):
    recs[i] = clip_circle(recs[i], radius=n_x//2)
print("OK")

# Output
print("Writing result")
t0 = time()
np.save("/home/pierre/tmp/recs.npy", recs)
print("OK (%.3f s)" % (time() - t0))


