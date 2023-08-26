import numpy as np
try:
    import astra
    __have_astra__ = True
except ImportError:
    __have_astra__ = False
try:
    import pycuda.gpuarray as garray
    __have_pycuda__ = True
except ImportError:
    __have_pycuda__ = False


class ConebeamReconstructor:
    """
    A wrapper around the Astra toolbox for cone-beam reconstruction.
    """
    def __init__(self, sinos_shape, source_origin_dist, origin_det_dist, angles=None):
        """
        Parameters
        -----------
        sinos_shape: tuple
            Shape of the sinograms stack, in the form (n_angles, n_y, n_x).
        angles: array, optional
            Rotation angles in radians. If provided, its length should be equal to sinos_shape[0].
        """
        self._init_geometry(sinos_shape, source_origin_dist, origin_det_dist, angles)
        self._output = None
        self._output_allocated = False
        self._alg_id = None
        self._vol_id = None
        self._proj_id = None

    def _set_sino_shape(self, sinos_shape):
        if len(sinos_shape) != 3:
            raise ValueError("Expected a 3D shape")
        self.sinos_shape = sinos_shape
        # self.n_angles, self.n_sinos, self.dwidth = sinos_shape
        self.n_sinos, self.n_angles, self.dwidth = sinos_shape

    def _init_geometry(self, sinos_shape, source_origin_dist, origin_det_dist, angles):
        self._set_sino_shape(sinos_shape)
        if angles is None:
            self.angles = np.linspace(0, 2*np.pi, self.n_angles, endpoint=True)
        else:
            self.angles = angles
        self.source_origin_dist = source_origin_dist
        self.origin_det_dist = origin_det_dist
        self.proj_geom = astra.create_proj_geom(
            "cone",
            # detector spacing in each dimension.
            # Normalized to 1, so probably source_origin and origin_dest have to be put wrt this unit ?
            1., 1.,
            self.n_sinos,
            self.dwidth,
            self.angles,
            self.source_origin_dist, self.origin_det_dist
        )
        self.n_x = self.dwidth # tune ?
        self.n_z = self.n_sinos # ?
        self.n_y = self.n_x
        self.vol_geom = astra.create_vol_geom(self.n_y, self.n_x, self.n_z)  # y <-> x ?


    def _allocate_output(self):
        self._output = garray.zeros(astra.geom_size(self.vol_geom), "f")
        self._output_allocated = True
        return self._output

    def _set_output(self, volume):
        if volume is None:
            volume = self._allocate_output()
        # TODO check type (pycuda.gpuarray), shape and dtype
        self._output = volume
        z, y, x = volume.shape
        self._vol_link = astra.data3d.GPULink(volume.ptr, x, y, z, volume.strides[-2])
        self._vol_id = astra.data3d.link('-vol', self.vol_geom, self._vol_link)

    def _reset_output(self):
        if not(self._output_allocated):
            self._output = None


    def _set_input(self, sinos):
        if np.dtype(sinos.dtype) != np.dtype(np.float32):
            raise ValueError("Expected float32 array")
        if sinos.shape != self.sinos_shape:
            raise ValueError("Expected array with shape %s" % str(self.sinos_shape))
        # TODO don't create new link/proj_id if ptr is the same
        self._proj_data_link = astra.data3d.GPULink(sinos.ptr, self.dwidth, self.n_angles, self.n_z, sinos.strides[-2])
        self._proj_id = astra.data3d.link('-sino', self.proj_geom, self._proj_data_link)


    def _update_reconstruction(self):
        cfg = astra.astra_dict("FDK_CUDA")

        cfg['ReconstructionDataId'] = self._vol_id # rec_id
        cfg['ProjectionDataId'] = self._proj_id

        self._alg_id = astra.algorithm.create(cfg)


    def reconstruct(self, sinos, output=None):
        self._set_input(sinos)
        self._set_output(output)
        self._update_reconstruction()
        astra.algorithm.run(self._alg_id)
        res = self._output
        self._reset_output()
        return res


    def __del__(self):
        if self._alg_id is not None:
            astra.algorithm.delete(self._alg_id)
        if self._vol_id is not None:
            astra.data3d.delete(self._vol_id)
        if self._proj_id is not None:
            astra.data3d.delete(self._proj_id)





if __name__ == "__main__":

    n_y, n_x, n_z = (128, 127, 126)
    n_angles = 180
    source_orig = 1000
    orig_detec = 50

    vol_geom = astra.create_vol_geom(n_y, n_x, n_z)
    angles = np.linspace(0, 2*np.pi, n_angles, True)
    dwidth = n_x # or n_y
    proj_geom = astra.create_proj_geom('cone', 1.0, 1.0, n_z, dwidth, angles, source_orig, orig_detec)
    # proj_geom = astra.create_proj_geom('parallel3d', 1.0, 1.0, n_z, dwidth, angles)


    # hollow cube
    cube = np.zeros(astra.geom_size(vol_geom), dtype="f")
    cube[17:113,17:113,17:113] = 1
    cube[33:97,33:97,33:97] = 0

    proj_id, proj_data = astra.create_sino3d_gpu(cube, proj_geom, vol_geom)

    sinos = astra.data3d.get(proj_id) # (n_z, n_angles, n_x)

    # np.save("/tmp/cube_proj.npy", sinos)



    rec_geom = astra.create_vol_geom(n_x, n_x, n_z)

    import pycuda.autoinit
    d_sinos = garray.to_gpu(sinos)
    d_out = garray.zeros(astra.geom_size(rec_geom), "f")
    C = ConebeamReconstructor(sinos.shape, source_orig, orig_detec, angles=angles)

    d_out = C.reconstruct(d_sinos, output=d_out)
    out = d_out.get()
    np.save("/tmp/out.npy", out)



