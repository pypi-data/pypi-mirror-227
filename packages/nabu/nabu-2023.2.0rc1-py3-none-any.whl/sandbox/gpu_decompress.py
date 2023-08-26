from tomoscan.io import HDF5File
from time import time

from integrator.app.utils import get_distributed_integrator_params
conf, ai_config, cluster, datasets, outputs = get_distributed_integrator_params("integrator.conf")


fname1 = "/data/id11/nanoscope/ihma195/id11/goldBall/goldBall_r2_Z063/scan0004/eiger_0463.h5"
t0 = time()
with HDF5File(fname1, "r") as f:
    ds = f["/entry_0000/ESRF-ID11/eiger/data"]
    chunks = []
    for i in range(ds.id.get_num_chunks()): 
        _, chunk = ds.id.read_direct_chunk(ds.id.get_chunk_info(i).chunk_offset)
        chunks.append(chunk)
el = time() - t0
print("Read raw data in", el)

import numpy as np
from silx.opencl.codec.bitshuffle_lz4 import BitshuffleLz4

d1 = datasets[0]
B = BitshuffleLz4(max([len(c) for c in chunks]), np.prod(d1.data_shape[1:]), np.uint16)




def read_uncompressed_data(fname, data_h5_path, profile=False):
    chunks = []
    t0 = time()
    with HDF5File(fname, "r") as f:
        ds = f[data_h5_path]
        for i in range(ds.id.get_num_chunks()): 
            _, chunk = ds.id.read_direct_chunk(ds.id.get_chunk_info(i).chunk_offset)
            chunks.append(chunk)
    if profile:
        el = time() - t0
        print("Read uncompressed data in %.4f s" % el)
    return chunks


def decompress_chunks(gpu_decompressor, chunks, reshape_to=None, profile=False):
    out = gpu_decompressor.cl_mem["dec"] # be sure to use dec_size large enough to avoid re-allocation
    for chunk in chunks:
        gpu_decompressor.decompress(chunk, out=out)
    return out







from integrator.integrator import StackIntegrator
S = StackIntegrator(ai_config)

for fname, h5path in d1.get_virtual_sources().items():
    chunks = read_uncompressed_data(fname, h5path)

    gpu_decompressor.decompress(chunk, out=out)




# --------------------------------------
# --------------------------------------
# --------------------------------------

from integrator.utils import partition_list
from multiprocessing import Process


class NewStackIntegrator:
    def __init__(self, ai_config, n_proc):
        self.ai_config = ai_config
        self.n_proc = n_proc


    def set_new_dataset(self, dataset, output_dir):
        self.fnames = []
        for fname, h5path in dataset.get_virtual_sources().items():
            self.fnames.append((fname, h5path))



    def process_dataset(self, dataset, output_dir):
        self.set_new_dataset(dataset, output_dir)
        datasets = partition_list(self.fnames, self.n_proc)
        self.processes = []
        for i in range(self.n_proc):
            p = Process(
                target=worker_integrate,
                args=(self.ai_config, datasets[i]),
                kwargs={"device_num": i % 2}, # TODO len(n_devices)
            )
            p.start()
            self.processes.append(p)




import numpy as np
import os
from time import time
from tomoscan.io import HDF5File

from pyopencl import create_some_context
from integrator.app.utils import get_distributed_integrator_params
conf, ai_config, cluster, datasets, outputs = get_distributed_integrator_params("integrator.conf")
d1 = datasets[0]

def read_uncompressed_data(fname, data_h5_path, profile=False):
    chunks = []
    t0 = time()
    with HDF5File(fname, "r") as f:
        ds = f[data_h5_path]
        for i in range(ds.id.get_num_chunks()):
            _, chunk = ds.id.read_direct_chunk(ds.id.get_chunk_info(i).chunk_offset)
            chunks.append(chunk)
    if profile:
        el = time() - t0
        print("Read uncompressed data in %.4f s" % el)
    return chunks



def worker_integrate(ai_config, datasets, device_num=None):


    print("[%d] Will integrate %d datasets" % (os.getpid(), len(datasets)))

    from integrator.integrator import StackIntegrator
    from silx.opencl.codec.bitshuffle_lz4 import BitshuffleLz4

    ctx = None

    # Initialize AI
    extra_options = {}
    if device_num is not None:
        from integrator.utils import get_opencl_devices
        opencl_device = get_opencl_devices()[device_num]
        ctx = create_some_context(answers=list(opencl_device))
        extra_options["target_device"] = opencl_device
        print("Using %s" % (str(opencl_device)))
    S = StackIntegrator(ai_config, extra_options=extra_options)
    ai_engine = S.ai.engines["ocl_csr_integr"].engine # TODO better

    # Initialize decompressor
    # gpu_decompressor = BitshuffleLz4(4471016, 4471016, np.uint16, ctx=ctx) # TODO better
    gpu_decompressor = BitshuffleLz4(4471016, 4471016, np.uint16, ctx=ai_engine.ctx) # TODO better
    out_decomp = gpu_decompressor.cl_mem["dec"] # be sure to use dec_size large enough to avoid re-allocation

    for fname, h5path in datasets:
        chunks = read_uncompressed_data(fname, h5path)
        res = np.zeros((len(chunks), ai_config.n_pts), "f")
        t0 = time()
        for img_idx, chunk in enumerate(chunks):
            gpu_decompressor.decompress(chunk, out=out_decomp)
            d_img = out_decomp.reshape((2162, 2068)) # TODO better
            ai_result = ai_engine.integrate_ng(d_img)
            res[img_idx] = ai_result.intensity
        el = time() - t0
        print("[%d] Processed %d images in %.3fs (%.1f FPS)" % (os.getpid(), len(chunks), el, len(chunks)/el))












