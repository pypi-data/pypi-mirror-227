#!/usr/bin/env python

import numpy as np
from pycuda.compiler import SourceModule
import pycuda.autoinit
from scipy.misc import ascent
import pycuda.gpuarray as garray
from scipy.ndimage.filters import median_filter
from spire.utils import ims

img = ascent().astype("f")

def test0():

    with open("/home/pierre/projects/nabu/nabu/cuda/src/medfilt.cu") as fid:
        src = fid.read()
    S = SourceModule(src, include_dirs=["/home/pierre/projects/nabu/nabu/cuda/src/"])
    M = S.get_function("medfilt2d")
    d_img = garray.to_gpu(img)
    d_out = garray.zeros_like(d_img)

    # 4x
    img2 = np.tile(img, (4,4))
    d_img2 = garray.to_gpu(img2)
    d_out2 = garray.zeros_like(d_img2)
    # warm-up
    M(d_img2.gpudata, d_out2.gpudata, np.int32(2048), np.int32(2048), np.int32(1), block=(32, 32, 1), grid=(64, 64))

    M(d_img2.gpudata, d_out2.gpudata, np.int32(2048), np.int32(2048), np.int32(1), block=(32, 32, 1), grid=(64, 64))


def test1():
    from nabu.cuda.medfilt import MedianFilter

    img2 = np.tile(img, (4,4))
    d_img2 = garray.to_gpu(img2)
    d_out2 = garray.zeros_like(d_img2)

    M2 = MedianFilter(img2.shape)
    M2.medfilt2(d_img2, output=d_out2) # warm-up
    M2.medfilt2(d_img2, output=d_out2)


if __name__ == "__main__":
    test1()

