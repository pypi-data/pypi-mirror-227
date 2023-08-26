import os
import numpy as np
import pycuda.gpuarray as cua
from pycuda.reduction import ReductionKernel as CU_RedK
from pycuda.elementwise import ElementwiseKernel as CU_ElK
import pycuda.tools as cu_tools
from pycuda.compiler import SourceModule

argmax_dtype = np.dtype([("idx", np.int32), ("cur_max", np.float32)])
cu_tools.get_or_register_dtype("idx_max", argmax_dtype)

from pyvkfft.fft import rfftn as pyvkfft_rfftn, irfftn as pyvkfft_irfftn



src_complex = """
#include <pycuda-complex.hpp>
typedef pycuda::complex<float> complexf;

/// dot product
inline __device__ float dot(complexf a, complexf b)
{
    return a.real() * b.real() + a.imag() * b.imag();
}

/// Norm
inline __device__ float ComplexNormN(const complexf v, const int nn)
{
  const float a = sqrtf(dot(v, v));
  float an = a;
  for(int i=1;i<nn;i++) an *= a;
  return an;
}

/// Complex atomic add
inline __device__ complexf atomicAdd(complexf *p, complexf v)
{
   // TODO: avoid using private ->_M_im and ->_M_re
   return complexf(atomicAdd(&(p->_M_re), v.real()), atomicAdd(&(p->_M_im), v.imag()));
}
"""


src_argmax = """
#include <pycuda-complex.hpp>
typedef pycuda::complex<float> complexf;

// This must be defined in Python using:
// argmax_dtype = np.dtype([("idx", np.int32), ("cur_max", np.float32)])
// cu_tools.get_or_register_dtype("idx_max", argmax_dtype)


struct idx_max
{
    int idx;
    float cur_max;
    __device__ idx_max()
    { }
    __device__ idx_max(int cidx, float cmax)
    : idx(cidx), cur_max(cmax)
    { }
    __device__ idx_max(idx_max const &src)
    : idx(src.idx), cur_max(src.cur_max)
    { }
    __device__ idx_max(idx_max const volatile &src)
    : idx(src.idx), cur_max(src.cur_max)
    { }
    __device__ idx_max volatile &operator=(
        idx_max const &src) volatile
    {
        idx = src.idx;
        cur_max = src.cur_max;
        return *this;
    }
};

 __device__ idx_max argmax_reduce(idx_max a, idx_max b)
 {
   if(a.cur_max>b.cur_max) return a;
   return b;
 }
"""



def register_translation_2d_paraboloid_cuda(ref_img, img, low_cutoff=None, high_cutoff=None,
                                            low_width=0.03, high_width=0.03,
                                            return_cc=False, return_gpu_arrays=False):
    """
    CUDA image registration. Sub-pixel accuracy is provided by a paraboloid
    fit of the CC maximum.
    :param ref_img, img: the images to be registered, either as numpy array or as
        a pycuda.gpuarray.GPUArray. Type should be float32.
        These can also be a stack of 2D images of size - in that case
        the registration is done in // for the all images, and the shift are returned
        as arrays which have the shape ref_img.shape[:-2].
    :param low_cutoff: a 0<value<<0.5 can be given (typically it should be a few 0.01),
        an erfc filter with a cutoff at low_cutoff*N (where N is the size along each dimension)
        will be applied, after the images have been FT'd.
    :param high_cutoff: same as low_cutoff fot the high frequency filter, should be close below 0.5.
        This is less useful than the low_cutoff, as the high frequencis are the most useful for
        the registration.
    :param low_width: the width of the low cutoff filter, also as a percentage of the size. Default=0.03
    :param high_width: same as low_width
    :param return_cc: if True, also return the CC map (default=False)
    :param return_gpu_arrays: if True, return the results as gpu arrays (default=False)
    :return: the computed shift as a tuple (dy, dx)
    """
    if not isinstance(ref_img, cua.GPUArray):
        ref_img = cua.to_gpu(ref_img.astype(np.float32))
    else:
        ref_img = ref_img.astype(np.float32)

    if not isinstance(img, cua.GPUArray):
        img = cua.to_gpu(img.astype(np.float32))
    else:
        img = img.astype(np.float32)

    if register_translation_2d_paraboloid_cuda.cu_argmax_f_red is None:
        register_translation_2d_paraboloid_cuda.cu_argmax_f_red = \
            CU_RedK(argmax_dtype, neutral="idx_max(0,0.0f)", name='argmax_f',
                    reduce_expr="argmax_reduce(a,b)",
                    map_expr="idx_max(i, d[i])",
                    preamble=src_argmax, #getks("cuda/argmax.cu"),
                    options=["-use_fast_math"],
                    arguments="float *d")

    if register_translation_2d_paraboloid_cuda.cu_paraboloid9 is None:
        cu_paraboloid_src = """
        // parabolic 3-point fit along x and y, computed for a stack of CC maps
        // result is stored in cy and cx
        __device__ void paraboloid9fit(const int i, float* cy, float* cx, idx_max *im, float *cc, const int ny, const int nx)
        {
            const int idx = im[i].idx;
            const int iy = idx / nx;
            const int ix = idx - iy*nx;
            const int ixm = ix-1 + nx *(ix==0);
            const int ixp = ix+1 - nx *(ix==(nx-1));
            const int iym = iy-1 + ny *(iy==0);
            const int iyp = iy+1 - ny *(iy==(ny-1));

            // Paraboloid fit
            // CC(x,y)=Ax^2 + By^2 + Cxy + Dx + Ey + F

            const float F= cc[ix  + iy  * nx];
            const float A= (cc[ixp  + iy  * nx] + cc[ixm  + iy  * nx])/2.0f - F;
            const float B= (cc[ix   + iyp * nx] + cc[ix   + iym * nx])/2.0f - F;
            const float D= (cc[ixp  + iy  * nx] - cc[ixm  + iy  * nx])/2.0f;
            const float E= (cc[ix   + iyp * nx] - cc[ix   + iym * nx])/2.0f;
            const float C= (cc[ixp  + iyp * nx] - cc[ixp  + iym * nx] - cc[ixm  + iyp * nx] + cc[ixm  + iym * nx])/4.0f;

            const float dx = (float)ix + fmaxf(fminf( (2*B*D-C*E) / (C*C-4*A*B), 0.5f),-0.5f);
            const float dy = (float)iy + fmaxf(fminf( (2*A*E-C*D) / (C*C-4*A*B), 0.5f),-0.5f);
            cx[i] = dx - nx * (dx>(nx/2)) + nx * (dx<(-nx/2));
            cy[i] = dy - ny * (dy>(ny/2)) + ny * (dy<(-ny/2));
        }

        """
        register_translation_2d_paraboloid_cuda.cu_paraboloid9 = \
            CU_ElK(name='cu_paraboloid9',
                   operation="paraboloid9fit(i, vy, vx, im, cc, ny, nx)",
                   preamble=src_complex + src_argmax + cu_paraboloid_src,  #getks('cuda/complex.cu') + getks("cuda/argmax.cu") + cu_paraboloid_src,
                   options=["-use_fast_math"],
                   arguments="float* vy, float* vx, idx_max * im, float *cc, const int ny, const int nx")

    if register_translation_2d_paraboloid_cuda.cu_cc_fourier_conj_filter is None:
        cu_cc_fourier_conj_filter_src = """
        // Multiply two array by complex conjugate of other & filter
        // This is a half-hermitian array
        // nx should be the length of the complex array
        __device__ void cc_fourier_conj_filter(const int i, complexf* d1, complexf* d2, const float low_cutoff, 
                                      const float low_width, const float high_cutoff, const float high_width,
                                      const int ny, const int nx)
        {
            const int iz = i / (nx*ny);
            const int iy = (i-iz*nx*ny)/nx;
            const int ix = i-nx*(iy + ny*iz);

            const complexf c1 = d1[i];
            const complexf c2 = d2[i];

            float r = 1;
            const float fx = (float)ix/(float)(2*(nx-1));
            const float fy = (float)(iy - ny * (iy>=ny/2)) / (float)(ny);
            const float f = sqrtf(fx*fx + fy*fy);
            if(low_cutoff>=0.0f) r *=1.0f - 0.5f * erfcf((f - low_cutoff) / low_width);
            if(high_cutoff<=0.5f) r *= 0.5f * erfcf((f - high_cutoff) / high_width);
            d1[i] = complexf(c1.real()*c2.real()+c1.imag()*c2.imag(), c1.imag()*c2.real()-c1.real()*c2.imag()) * r;
        }

        """
        register_translation_2d_paraboloid_cuda.cu_cc_fourier_conj_filter = \
            CU_ElK(name='cc_fourier_conj_filter',
                   operation="cc_fourier_conj_filter(i, d1, d2, low_cutoff, low_width, high_cutoff, high_width, ny, nx)",
                   preamble=src_complex + cu_cc_fourier_conj_filter_src, # getks('cuda/complex.cu') + cu_cc_fourier_conj_filter_src,
                   options=["-use_fast_math"],
                   arguments="pycuda::complex<float>* d1, pycuda::complex<float>* d2,"
                             "const float low_cutoff, const float low_width,"
                             "const float high_cutoff, const float high_width, const int ny, const int nx")
    # out-of-place r2c
    d1f = pyvkfft_rfftn(ref_img, ndim=2)
    d2f = pyvkfft_rfftn(img, ndim=2)

    # Filter and d1f * d2f.conj()
    # cc0 = irfftn(d1f * d2f.conj(out=d2f), ndim=2)
    ny, nx = np.int32(img.shape[0]), np.int32(img.shape[1])
    low_cutoff = np.float32(-1) if low_cutoff is None else np.float32(low_cutoff)
    low_width = np.float32(low_width)
    high_cutoff = np.float32(1) if high_cutoff is None else np.float32(high_cutoff)
    high_width = np.float32(high_width)
    register_translation_2d_paraboloid_cuda.cu_cc_fourier_conj_filter(d1f, d2f, low_cutoff, low_width, high_cutoff,
                                                                      high_width, ny, nx)

    # c2r fft to get CC map
    cc0 = pyvkfft_irfftn(d1f, ndim=2)

    # Pixel registration
    idx = register_translation_2d_paraboloid_cuda.cu_argmax_f_red(cc0)

    # how many images ?
    if ref_img.ndim == 2:
        is_2d = True
        sh = 1
    else:
        is_2d = False
        sh = ref_img.shape[:-2]  # Keep the shift shape same as input images extra dimensions

    # Paraboloid 3x3 pixels fit
    cy, cx = cua.empty(sh, dtype=np.float32), cua.empty(sh, dtype=np.float32)
    ny, nx = np.int32(cc0.shape[0]), np.int32(cc0.shape[1])

    register_translation_2d_paraboloid_cuda.cu_paraboloid9(cy, cx, idx, cc0, ny, nx)
    if return_cc:
        if return_gpu_arrays:
            return cy, cx, cc0
        if is_2d:
            return cy.get()[0], cx.get()[0], cc0.get()
        else:
            return cy.get(), cx.get(), cc0.get()
    if return_gpu_arrays:
        return cy, cx
    if is_2d:
        return cy.get()[0], cx.get()[0]
    else:
        return cy.get(), cx.get()


register_translation_2d_paraboloid_cuda.cu_paraboloid9 = None
register_translation_2d_paraboloid_cuda.cu_argmax_f_red = None
register_translation_2d_paraboloid_cuda.cu_cc_fourier_conj_filter = None






def divide_image_into_patches(img, patch_size):
    ps0, ps1 = patch_size, patch_size # TODO non-square patches

    np0, np1 = img.shape[0] // ps0, img.shape[1] // ps1
    patches = np.zeros((np0 * np1, ps0, ps1), dtype=img.dtype)

    for i in range(np0):
        for j in range(np1):
            patches[i * np1 + j] = img[i*ps0:(i+1)*ps0, j*ps1:(j+1)*ps1].copy()
    return patches



from tomoscan.io import HDF5File
def load_proj(fname, data_path, indices, entry="entry"):
    with HDF5File(fname, "r") as f:
        r = f[data_path][indices]
    return r


d0 = load_proj("/scisoft/tomo_data/id16_ctf/ON73_0764_ME_AD_stsh_N4000_125nm_1_.nx", "entry/data/data", 0)
f0 = load_proj("/scisoft/tomo_data/id16_ctf/ON73_0764_ME_AD_stsh_N4000_125nm_1_.nx", "entry/data/data", 40)
p0 = load_proj("/scisoft/tomo_data/id16_ctf/ON73_0764_ME_AD_stsh_N4000_125nm_1_.nx", "entry/data/data", 1000)
pn = (p0*1.-d0).astype("f")

patches_proj = divide_image_into_patches(pn, 100)
patches_flat = divide_image_into_patches(f0.astype("f"), 100)

import pycuda.autoinit
q = register_translation_2d_paraboloid_cuda(patches_proj, patches_flat, low_cutoff=0.01)




from scipy.misc import ascent
from scipy.ndimage import shift as ndshift
img = ascent().astype("f")


def generate_pair_of_patches(min_shift=-2, max_shift=2):
    p = img[200:300, 100:200] # patch_size = 100
    n_i, n_j = 20, 21

    ref = np.tile(p, (n_i * n_j, 1, 1))
    res = np.zeros_like(ref)
    shifts = (max_shift - min_shift) * np.random.rand(n_i, n_j, 2) + min_shift

    for i in range(n_i):
        for j in range(n_j):
            res[i * n_j + j] = ndshift(p, (shifts[i, j][0], shifts[i, j][1]), mode="nearest")
    return res, ref, shifts


from skimage.registration import phase_cross_correlation

p01, p02, sh = generate_pair_of_patches(min_shift=-10, max_shift=10)

upsample_factor = 5
offsets = np.array([phase_cross_correlation(patch1, patch2, upsample_factor=upsample_factor)[0] for (patch1, patch2) in zip(p01, p02)])

n_i, n_j, _ = sh.shape
errors = np.zeros_like(sh)
for i in range(n_i):
    for j in range(n_j):
        errors[i, j] = offsets[i * n_j + j] - sh[i, j]


rtol = 0.2
assert np.max(np.abs(errors)) < 1/upsample_factor * (1 + rtol)


# skimage phase_cross_correlation finds the shifts quite accurately


# A first-order approx (without sub-pixel accuracy):


eps = np.finfo(np.float32).eps

def _find_max(cross_correlation):
    # Locate maximum - from skimage phase_cross_correlation()
    maxima = np.unravel_index(np.argmax(np.abs(cross_correlation)), cross_correlation.shape)
    midpoints = np.array([np.fix(axis_size / 2) for axis_size in cross_correlation.shape])
    shifts = np.stack(maxima).astype("f", copy=False)
    shifts[shifts > midpoints] -= np.array(cross_correlation.shape)[shifts > midpoints]
    #
    return shifts

def my_phase_cross_correlation(img1, img2):
    pro = np.fft.rfft2(img1) * np.conj(np.fft.rfft2(img2))
    pro /= np.maximum(np.abs(pro), 100 * eps)
    cross_correlation = np.fft.irfft2(pro)
    return _find_max(cross_correlation)


def my_phase_cross_correlation_upsampled(img1, img2, oversampling=1):

    if oversampling > 1:
        pad_sizes = [(oversampling - 1) * dim for dim in img1.shape]
        pad_lengths = tuple((s//2, s - s//2) for s in pad_sizes)
        print(pad_sizes)
        print(pad_lengths)
        img1 = np.pad(img1, pad_lengths, mode="constant") # reflect ?
        img2 = np.pad(img2, pad_lengths, mode="constant") # reflect ?

    pro = np.fft.rfft2(img1) * np.conj(np.fft.rfft2(img2))
    pro /= np.maximum(np.abs(pro), 100 * eps)
    cross_correlation = np.fft.irfft2(pro)
    return cross_correlation
    # return _find_max(cross_correlation)

# doing my_phase_cross_correlation() + this works:



m = my_phase_cross_correlation_upsampled(p01[20], p02[20], oversampling=1)
cc = m.ravel()

"""
nx = ny = 100
iy, ix = 91, 5

ixm = ix-1 + nx *(ix==0);
ixp = ix+1 - nx *(ix==(nx-1));
iym = iy-1 + ny *(iy==0);
iyp = iy+1 - ny *(iy==(ny-1));


F= cc[ix  + iy  * nx];
A= (cc[ixp  + iy  * nx] + cc[ixm  + iy  * nx])/2.0 - F;
B= (cc[ix   + iyp * nx] + cc[ix   + iym * nx])/2.0 - F;
D= (cc[ixp  + iy  * nx] - cc[ixm  + iy  * nx])/2.0;
E= (cc[ix   + iyp * nx] - cc[ix   + iym * nx])/2.0;
C= (cc[ixp  + iyp * nx] - cc[ixp  + iym * nx] - cc[ixm  + iyp * nx] + cc[ixm  + iym * nx])/4.0;


dx = ix + max(min( (2*B*D-C*E) / (C*C-4*A*B), 0.5),-0.5);
dy = iy + max(min( (2*A*E-C*D) / (C*C-4*A*B), 0.5),-0.5);

cx = dx - nx * (dx>(nx/2)) + nx * (dx<(-nx/2));
cy = dy - ny * (dy>(ny/2)) + ny * (dy<(-ny/2));
"""




