"""
The UFO forward projector is very simple.
The kernel had to be modified to account for variable angles.


Cons:
  - It's still not clear it can work with data outside the "inner circle" (local tomography).
  - LGPL license


"""



"""

/*
 * Copyright (C) 2011-2013 Karlsruhe Institute of Technology
 *
 * This file is part of Ufo.
 *
 * This library is free software: you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation, either
 * version 3 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library.  If not, see <http://www.gnu.org/licenses/>.
 */

__global__ void line_projector(
    float* sinogram,
    int slice_width,
    int n_angles,
    float axis_pos,
    float* cos_angles,
    float* sin_angles
) {
    const int idx = blockDim.x * blockIdx.x + threadIdx.x;
    const int idy = blockDim.y * blockIdx.y + threadIdx.y;

    if (idx >= slice_width || idy >= n_angles) return;

    /* radius of object circle */
    const float r = fminf (axis_pos, slice_width - axis_pos);
    /* positive/negative distance from detector center */
    const float d = idx - axis_pos; // + 0.5f;
    /* length of the cut through the circle */
    const float l = sqrtf(4.0f*r*r - 4.0f*d*d);

    /* vector in detector direction */
    float2 D = make_float2(cos_angles[idy], sin_angles[idy]);

    /* vector perpendicular to the detector */
    const float2 N = make_float2(D.y, -D.x);

    /* sample point in the circle traveling along N */
    // float2 sample = d * D - l/2.0f * N + make_float2(axis_pos, axis_pos);
    float x = d * D.x - l/2.0f * N.x + axis_pos;
    float y = d * D.y - l/2.0f * N.y + axis_pos;
    float sum = 0.0f;

    for (int i = 0; i < l; i++) {
        // sum += read_imagef(slice, sampler, sample).x;
        sum += tex2D(texSlice, x, y);
        x += N.x;
        y += N.y;
    }

    sinogram[idy * slice_width + idx] = sum;
}
"""


class LineProjector(Projector):

    _projector_name = "line_projector"
    _projector_signature = "PiifPP"

    def _allocate_memory(self):
        self.d_sino = garray.zeros(self.sino_shape, "f")
        self._d_cos = garray.to_gpu(np.cos(self.angles).astype("f"))
        self._d_sin = garray.to_gpu(np.sin(self.angles).astype("f"))
        # Textures
        self.d_image_cua = cuda.np_to_array(
            np.zeros((self.shape[0], self.shape[1]), "f"),
            "C"
        )

    def _proj_precomputations(self):
        pass

    def _compile_kernels(self):

        self.gpu_projector = CudaKernel(
            self._projector_name,
            filename=get_cuda_srcfile("proj.cu"),
        )
        self.texref_slice = self.gpu_projector.module.get_texref("texSlice")
        self.texref_slice.set_array(self.d_image_cua)
        self.texref_slice.set_filter_mode(cuda.filter_mode.LINEAR)
        self.gpu_projector.prepare(self._projector_signature, [self.texref_slice])

        self.kernel_args = (
            self.d_sino.gpudata,
            np.int32(self.dwidth),
            np.int32(self.nprojs),
            np.float32(self.axis_pos),
            self._d_cos.gpudata,
            self._d_sin.gpudata,
        )
        self._proj_kernel_blk = (32, 32, 1) # TODO tune
        self._proj_kernel_grd = (
            updiv(self.dwidth, self._proj_kernel_blk[0]),
            updiv(self.nprojs, self._proj_kernel_blk[1]),
            1
        )


    def _compute_angles(self):
        pass

    def set_image(self, image, check=True):
        if check:
            self._check_input_array(image)
        copy_array(
            self.d_image_cua, image,
            check=True
        )




"""
# Warning: don't forget to reverse order: L(image)[::-1, ::-1]    to compare with pyhst projector.
"""