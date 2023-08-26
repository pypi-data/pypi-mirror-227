from nabu.resources.computations import estimate_chunk_size
from nabu.preproc.phase import compute_paganin_margin
from nabu.cuda.utils import get_gpu_memory
from nabu.resources.processconfig import ProcessConfig
from nabu.app.fullfield_cuda import CudaFullFieldPipeline, CudaFullFieldPipelineLimitedMemory


"""
fname = "/scratch/paleo/bamboo/nabu.conf"
z_start = 0
z_end = 500
gpu_id = 0
gpu_mem_fraction = 0.9



proc = ProcessConfig(fname)
# For bamboo
proc.dataset_infos.dataset_scanner._energy = 19.
proc.processing_options["phase"]["energy_kev"] = 19.



chunk_size = estimate_chunk_size(
    get_gpu_memory(gpu_id) * gpu_mem_fraction,
    process_config,
    chunk_step=10
)

if "phase" in proc.processing_steps:
    margin_v, margin_h = compute_paganin_margin(
        radio_shape,
        distance=opts["distance_cm"],
        energy=opts["energy_kev"],
        delta_beta=opts["delta_beta"],
        pixel_size=opts["pixel_size_microns"],
        padding=opts["padding_type"]
    )



F = CudaFullFieldPipeline(proc, (start_z, start_z + delta_z))
#F = CudaFullFieldPipelineLimitedMemory(proc, (start_z, start_z + delta_z), chunk_size=chunk_size

"""

"""

Logic/flow
------------

get the requested GPU, or take "0"

estimate chunk size
estimate paganin margin

if paganin margin > chunk size:
    CudaFullFieldPipelineLimitedMemory
default: CudaFullFieldPipeline

if (z_end - z_start) > chunk_size:
    cut by chunks, with overlap
else:
    chunk_size = (z_end - z_start) + margin

spawn pipeline
exec


Architecture
-------------

WorkersManager:
  Gère la logique: ressources, découpage en chunks, ...
  Instancie les Workers (local, slurm, ...)


"""


from psutil import virtual_memory
from nabu.resources.logger import LoggerOrPrint
from nabu.cuda.utils import collect_cuda_gpus


def get_gpus_ids(resources_cfg):
    gpus_ids = resources_cfg["gpu_id"]
    if gpus_ids != []:
        return gpus_ids
    # TODO (?) heuristic to pick the best gpus
    return list(range(resources_cfg["gpus"]))



class SimpleWorkersManager:

    gpu_mem_fraction = 0.9
    cpu_mem_fraction = 0.9
    phase_processing_mode = "accurate"
    pipeline_cls = CudaFullFieldPipeline


    def __init__(self, process_config, logger=None):
        self.process_config = process_config
        self.logger = LoggerOrPrint(logger)
        self._get_reconstruction_range()
        self._get_resources()
        self._compute_chunk_size()
        self._compute_phase_margin()
        self._compute_volume_chunks()


    def _get_reconstruction_range(self):
        rec_cfg = self.process_config.nabu_config["reconstruction"]
        self.z_min = rec_cfg["start_z"]
        self.z_max = rec_cfg["end_z"]
        self.delta_z = self.z_max - self.z_min


    def _get_resources(self):
        self.resources = {}
        self._get_gpu()
        self._get_memory()


    def _get_memory(self):
        vm = virtual_memory()
        self.resources["mem_avail_GB"] = vm.available / 1e9


    def _get_gpu(self):
        gpus = get_gpus_ids(self.process_config.nabu_config["resources"])
        if len(gpus) == 0:
            raise ValueError("Need at least one GPU")
        if len(gpus) > 1:
            raise ValueError("This class does not support more than one GPU")
        self.resources["gpu_id"] = self._gpu_id = gpus[0]
        self.resources["gpus"] = collect_cuda_gpus()


    def _compute_chunk_size(self):
        gpu_mem = self.resources["gpus"][self._gpu_id]["memory_GB"] * self.gpu_mem_fraction
        cpu_mem = self.resources["mem_avail_GB"] * self.cpu_mem_fraction
        mem_avail = min(gpu_mem, cpu_mem)
        self.max_chunk_size = estimate_chunk_size(
            mem_avail,
            self.process_config,
            chunk_step=10
        )


    def _compute_phase_margin(self):
        if "phase" not in proc.processing_steps:
            self._phase_margin = (0, 0)
            return
        radio_shape = self.process_config.dataset_infos.radio_dims[::-1]
        opts = self.process_config.processing_options["phase"]
        margin_v, margin_h = compute_paganin_margin(
            radio_shape,
            distance=opts["distance_cm"],
            energy=opts["energy_kev"],
            delta_beta=opts["delta_beta"],
            pixel_size=opts["pixel_size_microns"],
            padding=opts["padding_type"]
        )
        self._phase_margin = (margin_v, margin_h)



    def _compute_volume_chunks(self):
        n_z = self.process_config.dataset_infos._radio_dims_notbinned[1]
        margin_v = self._phase_margin[0]
        self.margin_up = min(margin_v, self.z_min)
        self.margin_down = min(margin_v, n_z - self.z_max)

        chunk_size = self.delta_z + self.margin_up + self.margin_down
        if chunk_size > self.max_chunk_size:
            self.logger.warning(
                "Phase margin is %d, so we need to process at least %d detector rows. \
                However, the available memory enables to process only %d rows at once"
                % (margin_v, 2 * margin_v + 1, self.max_chunk_size)
            )
            if self.phase_processing_mode == "accurate": # TODO normalize the names
                self._pipeline_cls = CudaFullFieldPipelineLimitedMemory
                self.logger.debug("Using CudaFullFieldPipelineLimitedMemory")
            else:
                self._phase_margin = (0, 0)
                self._pipeline_cls = CudaFullFieldPipeline
                self.logger.debug("Using CudaFullFieldPipeline without margin")

















