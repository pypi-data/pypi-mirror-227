import numpy as np
from os import path, getpid
from spire.io import tiff_read #
from sidi.remote import RemoteClass
from nabu.reconstruction.fbp import Backprojector
from distributed import Client


class FileBackprojector(Backprojector):
    def __init__(
        self, slice_shape, angles, file_prefix, dwidth_x=None, dwidth_z=None,
        rot_center=None, extra_options={}, cuda_options={}
    ):
        super().__init__(slice_shape, angles, dwidth_x=dwidth_x,
            dwidth_z=dwidth_z, rot_center=rot_center,
            extra_options=extra_options, cuda_options=cuda_options
        )
        self.file_prefix = file_prefix
        self.pid = getpid()
        self.debug("FileBackprojector initiated")


    # TODO proper logger
    def debug(self, msg):
        print("[%d] %s" % (self.pid, msg))


    def get_sino(self, num):
        fname = str("%s%04d.tif" % (self.file_prefix, num))
        if not(path.isfile(fname)):
            return None
        return tiff_read(fname)


    def reconstruct(self, num):
        self.debug("Reconstructing %d" % num)
        sino = self.get_sino(num)
        if sino is None:
            self.debug("Could not get sino %d" % num)
            return None
        rec = self.fbp(sino)
        return rec




class DistributedFBP(object):

    # TODO more flexibility in options
    def __init__(self, client_addr, n_workers, slice_shape, angles, file_prefix):
        self.client = Client(client_addr)

        # This assumes that there is one different GPU ID per worker
        fbp_kwargs_list = []
        for i in range(n_workers):
            fbp_kwargs_list.append({"cuda_options": {"device_id": i}})
        #
        self.remote_reconstructors = RemoteClass(
            self.client, FileBackprojector,
            class_args=(slice_shape, angles, file_prefix),
            class_kwargs_list=fbp_kwargs_list,
        )

        # Important to push context
        # Keep results in futures ! Even if None.
        self._contexts = self.remote_reconstructors.submit_task("push_context", who="all")

        #
        self.workers = list(self.client.has_what().keys())


    def reconstruct(self, n_slices, callback=None):
        n_workers = len(self.workers)
        results = []
        for i in range(n_slices):
            # Dispatch work
            # TODO implement this in sidi ?
            worker = self.workers[i % n_workers]
            future_result = self.remote_reconstructors.submit_task(
                "reconstruct", method_args=(i,), workers=[worker]
            )[0]
            if callback is not None:
                future_result.add_done_callback(callback)
            results.append(future_result)
        return results



