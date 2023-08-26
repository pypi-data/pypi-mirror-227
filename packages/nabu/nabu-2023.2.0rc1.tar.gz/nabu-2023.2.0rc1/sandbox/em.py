import numpy as np
import pycuda.autoinit; import pycuda.gpuarray as garray; import pycuda.driver as cuda
from nabu.reconstruction.fbp import Backprojector
from nabu.reconstruction.projection import Projector
from spire.utils import ims
from pycuda.elementwise import ElementwiseKernel

mri_sino = np.load("/data/pierre/tests/MRI_512_proj_400.npy")[50]
d_sino = garray.to_gpu(mri_sino)

class EM:
    def __init__(self, slice_shape, angles, proj=None, backproj=None):
        self.proj = Projector(slice_shape, angles)
        self.backproj = Backprojector(self.proj.sino_shape, angles=angles)

        self.d_proj = garray.zeros(self.proj.sino_shape, "f")
        self.d_img = garray.zeros(self.backproj.slice_shape, "f")
        self._init_eltwise()


    def _init_eltwise(self):
        self.update_proj = ElementwiseKernel(
            "float* proj, float* data, float eps",
            "proj[i] = (fabsf(proj[i]) > eps) ? data[i]/proj[i] : data[i];",
            "update_proj"
        )
        self.update_img = ElementwiseKernel(
            "float* sol, float* backproj, float* oinv",
            "sol[i] *= backproj[i] * oinv[i];",
            "update_img"
        )


    def run(self, sino, n_it, eps=1e-6):

        P = lambda x: self.proj(x, output=self.d_proj)
        PT = lambda y: self.backproj.backproj(y, output=self.d_img)
        o = garray.ones_like(sino)
        oinv = garray.to_gpu(1./self.backproj.backproj(o))
        x = garray.ones_like(oinv)

        for k in range(n_it):
            proj = P(x)
            self.update_proj(proj, sino, eps)
            backproj = PT(proj)
            self.update_img(x, backproj, oinv)
        return x

em = EM(512, 400)
ims(em.run(d_sino, 800).get())