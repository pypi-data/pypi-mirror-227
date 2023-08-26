#!/usr/bin/env python

import numpy as np
from time import time
from nabu.resources.dataset_analyzer import EDFDatasetAnalyzer
from nabu.resources.dataset_validator import NabuValidator
from nabu.io.config import NabuConfigParser, validate_nabu_config
from nabu.io.reader import ChunkReader
from nabu.preproc.ccd import FlatField, CCDCorrection, CCDProcessing
from nabu.preproc.phase import PaganinPhaseRetrieval
from nabu.reconstruction.fbp import Backprojector
from nabu.misc.unsharp import UnsharpMask

# Extract informations from dataset location
E = EDFDatasetAnalyzer("/home/pierre/tmp/5.06_crayon_W150_60_Al2_W0.25_xc1000_")
# Read and validate user config file
conf = NabuConfigParser("/home/pierre/tmp/nabu2.conf").conf_dict
nabu_config = validate_nabu_config(conf)
# Build the final nabu processing configuration
V = NabuValidator(nabu_config, E)
V.perform_all_checks()
V.remove_unused_radios() # modifies "E"


DO_FLATFIELD = True
DO_CCD_CORR = True
DO_PAGANIN = True
DO_UNSHARP = False
DO_LOG = True


# Read a chunk of radios
print("Reading chunk")
t0 = time()
sub_region = (None, None, None, 100)
chunk_reader = ChunkReader(E.projections, sub_region=sub_region)
chunk_reader.load_files()
radios = chunk_reader.files_data.astype("f")
n_angles, n_z, n_x = radios.shape
print("OK (%.3f s)" % (time() - t0))


if DO_FLATFIELD:
    print("Doing flat-field")
    t0 = time()
    flatfield = FlatField(radios, E.flats, E.darks, sub_region=sub_region)
    radios = flatfield.normalize_radios()
    print("OK (%.3f s)" % (time() - t0))


if DO_CCD_CORR:
    print("Doing CCD correction")
    t0 = time()
    ccd = CCDCorrection(radios)
    # ~ radios_corr = np.zeros_like(radios)
    ccd.median_clip_correction()
    print("OK (%.3f s)" % (time() - t0))


if DO_PAGANIN:
    print("Doing Paganin")
    t0 = time()
    paganin = PaganinPhaseRetrieval(
        (n_z, n_x),
        distance=E.distance * 1e2,
        energy=E.energy,
        delta_beta=nabu_config["phase"]["paganin_delta_beta"],
        pixel_size=E.pixel_size
    )
    for i in range(E.n_angles):
        # ~ paganin.apply_filter(radios_corr[i], output=radios[i])
        radios[i] = paganin.apply_filter(radios[i])
    print("OK (%.3f s)" % (time() - t0))

if DO_UNSHARP:
    # Unsharp
    print("Doing unsharp")
    t0 = time()
    unsharp = UnsharpMask((n_z, n_x), 1.0, 5.)
    for i in range(E.n_angles):
        cuda_unsharp.unsharp(radios[i], radios_corr[i])
    print("OK (%.3f s)" % (time() - t0))

if DO_LOG:
    # Log
    print("Doing Logarithm")
    t0 = time()
    logproc = CCDProcessing(radios)
    logproc.take_logarithm(output=radios, clip_min=0.01)
    print("OK (%.3f s)" % (time() - t0))


# Reconstruction
recs = np.zeros((n_z, n_x, n_x), dtype="f")
print("Doing reconstruction")
t0 = time()
cudafbp = Backprojector(
    (n_x, n_x),
    E.n_angles,
    rot_center=nabu_config["reconstruction"]["rotation_axis_position"],
    extra_options={"padding_mode": "edges"}
)
for i in range(n_z):
    recs[i] = cudafbp.fbp(radios[:, i, :]) # TODO transpose ?
print("OK (%.3f s)" % (time() - t0))


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


