#!/usr/bin/env python

import numpy as np
from nabu.cuda.medfilt import MedianFilter
import pycuda.autoinit; import pycuda.gpuarray as garray
from time import sleep

radios = np.load("/home/pierre/tmp/crayon_100.npy")
#
radios = radios[:250, :, :]
radios = np.tile(radios, (1, 20, 1))
#
d_radios = garray.to_gpu(radios)

M = MedianFilter(d_radios.shape)
M2 = MedianFilter(d_radios[0].shape)

d_out = garray.zeros_like(d_radios)

def medfilt_b(M2, d_rads, d_out):
    for i in range(d_rads.shape[0]):
        M2.medfilt2(d_rads[i], output=d_out[i])


# 3D
M.medfilt2(d_radios, output=d_out) # warm-up
sleep(.1)
M.medfilt2(d_radios, output=d_out) # measure

sleep(.2)

# Batched
medfilt_b(M2, d_radios, d_out) # warm-up
sleep(.1)
medfilt_b(M2, d_radios, d_out) # measure


# on a (1500, 100, 2048) volume:    (image: 0.82 MB)
# 3D:       25 ms
# batched:  62 ms

# on a (1500, 400, 2048) volume:    (image: 3.3 MB)
# 3D:       80 ms
# batched:  90 ms

# on a (1000, 600, 2048) volume:    (image: 4.9 MB)
# 3D:       80 ms
# batched:  83 ms

# on a (250, 2000, 2048) volume:    (image: 16 MB)
# 3D:       67 ms
# batched:  66 ms
# This situation is almost ideal for batched: almost no latency




#
# Taking larger individual 2D images reduces the overhead-cost of batched 2D.
# But it needs more memory (except if the "output" is not a 3D volume).
