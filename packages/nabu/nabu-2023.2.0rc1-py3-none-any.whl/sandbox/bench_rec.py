from os import getpid
from time import perf_counter
from multiprocessing import Process
import numpy as np
import pycuda.gpuarray as garray
from nabu.reconstruction.fbp import Backprojector
from nabu.cuda.utils import get_cuda_context

sino_fname = "/tmp_14_days/paleo/sino2.npy"

n_images = 10




def get_sinos(fname):
    sino = np.load(fname)
    h_sinos = np.tile(sino, (n_images, 1, 1))
    d_sinos = garray.to_gpu(h_sinos)
    return h_sinos, d_sinos



def do_multi_reco(B, d_sinos, d_recs):
    n_sinos = d_sinos.shape[0]
    t0 = perf_counter()
    for i in range(n_sinos):
        B.fbp(d_sinos[i], output=d_recs[i])
    h_recs = d_recs[0].get() # do partial copy to avoid big D2H
    el = perf_counter() - t0
    print("[%d] FBP +H2D %d images: %.3f s" % (getpid(), n_sinos, el))
    return h_recs



def bench_simple(fname):

    ctx = get_cuda_context()

    h_sinos, d_sinos = get_sinos(fname)
    n_sinos = d_sinos.shape[0]

    B = Backprojector(d_sinos.shape[1:], padding_mode="edges", cuda_options={"ctx": ctx})
    d_recs = garray.zeros((n_sinos,) + B.slice_shape, "f")

    h_recs = do_multi_reco(B, d_sinos, d_recs)

    return h_recs



def bench_multiproc(fname, n_proc=1):
    procs = []
    for j in range(n_proc):
        p = Process(
            target=bench_simple,
            args=(fname,)
        )
        p.start()
        procs.append(p)

    return procs


