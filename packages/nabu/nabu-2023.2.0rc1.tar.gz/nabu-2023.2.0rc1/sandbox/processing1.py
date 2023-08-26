#!/usr/bin/env python

import numpy as np
from time import time
import pycuda.gpuarray as garray
from nabu.io.reader import NPZReader
from nabu.preproc.gpuphase import GPUPaganinPhaseRetrieval
from nabu.reconstruction.fbp import Backprojector


def process_chunk(path, chunk_size, chunk_index):
    dwidth = 2048# TODO in file
    n_angles = 2000 # TODO in file
    margin = 20

    start_y = chunk_index * chunk_size
    end_y = (chunk_index + 1) * chunk_size
    sub_region = (0, dwidth, start_y, end_y)

    reader = NPZReader(path, sub_region=sub_region)
    paganin = GPUPaganinPhaseRetrieval(
        (chunk_size, dwidth),
        margin=((0, margin), (0, 0)), #
        delta_beta=1.
    )
    fbp = Backprojector((dwidth, dwidth), n_angles)

    chunk = np.zeros((n_angles, chunk_size, dwidth), dtype="f")
    d_chunk = garray.zeros((chunk_size-margin, n_angles, dwidth), dtype="f")

    # Interleave I/O and processing ?
    t0 = time()
    for i in range(n_angles):
        frame = reader.next()
        chunk[i] = frame.astype("f")
        print("Read frame %d (%.1f MB)" % (reader.current_frame, frame.nbytes/1e6))
    read_time = time() - t0

    t1 = time()
    for i in range(n_angles):
        paganin.apply_filter(chunk[i], output=d_chunk[:, i, :])
        print("Pag %d" % i)
    pag_time = time() - t1

    # Rec
    t2 = time()
    d_rec = garray.zeros((chunk_size-margin, dwidth, dwidth), dtype="f")
    for i in range(chunk_size - margin):
        rec = fbp.fbp(d_chunk[i], output=d_rec[i])
        print("Rec %d" % i)
    rec_time = time() - t2

    # Write
    # ~ np.save("/dev/shm/rec.npy", d_rec.get())

    print("Read time: %.2f s \t Paganin: %.2f s \t FBP: %.2f s" % (read_time, pag_time, rec_time))


if __name__ == "__main__":
    # ~ process_chunk("/data/pierre/misc/MRI512_proj500_frames.npz", 40, 0)
    process_chunk("/data/pierre/misc/MRI3D_2048cube_proj_frames.npz", 200, 5)

