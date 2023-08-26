from distributed import Client, LocalCluster
from dask_jobqueue import SLURMCluster
from ...resources.processconfig import ProcessConfig
from ...resources.tasks import build_processing_steps
from ...distributed.worker import get_workers_resources, estimate_workers_chunk_size

# TODO move
def spawn_slurm_cluster(resources_config, spawn_workers=True):
    cfg = resources_config
    project_name = cfg["project_name"]
    if project_name == "":
        project_name = None
    cluster = SLURMCluster(
        queue=cfg["queue"],
        project=project_name,
        # ~ walltime=None, # TODO cfg["walltime"]
        cores=12, # TODO cfg["cores_per_node"]
        memory="10g", # TODO cfg["memory_per_node"]
        job_extra=[str("--gres=gpu:%d" % cfg["gpus_per_node"])],
    )
    if spawn_workers:
        cluster.scale(cfg["nodes"])
    return cluster


# TODO move
def spawn_local_cluster(resources_config):
    cfg = resources_config
    cluster = LocalCluster(
        n_workers=cfg["nodes"],
        # ~ threads_per_worker=None,
        processes=True,
        # ~ scheduler_port=0,
    )
    return cluster


# TODO move
def spawn_cluster(resources_config):
    """
    Spawn the computing resources requested by the current configuration file.

    Parameters
    -----------
    resources_config: dict
        Subset of the nabu_config dictionary (section "resources")
    """
    if resources_config["method"] == "slurm":
        cluster = spawn_slurm_cluster(resources_config)
    else: # local
        cluster = spawn_local_cluster(resources_config)
    return cluster




class NabuMasterProcess:

    def __init__(self, conf_file=None, process_config=None, try_cuda=True, try_opencl=False):
        """
        Parameters
        -----------
        conf_file: str
            Path to the nabu `.conf` file.
            Mutually exclusive with the `process_config` parameter.
        process_config: `ProcessConfig` instance
            Instance of `nabu.resources.processconfig.ProcessConfig`
            Mutually exclusive with the `conf_file` parameter.
        try_cuda: bool
            Whether to query for CUDA-compatible gpus when discovering workers resources.
        try_opencl: bool
            Whether to query for OpenCL-compatible gpus when discovering workers resources.
        """
        if not((conf_file is not None) ^ (process_config is not None)):
            raise ValueError("Please provide either 'conf_file' or 'process_config'")
        if conf_file is not None:
            process_config = ProcessConfig(conf_fname=conf_file) # TODO more args

        self.process_config = process_config
        self.nabu_config = process_config.nabu_config

        self.cluster = spawn_cluster(self.nabu_config["resources"])
        self.client = Client(self.cluster.scheduler_address)
        tasks, options = build_processing_steps(process_config)
        self.processing_steps = tasks
        self.processing_options = options

        self._get_workers_resources(try_cuda, try_opencl)

    def _get_workers_resources(self, try_cuda, try_opencl):
        self.workers_resources = get_workers_resources(
            self.client, try_cuda=try_cuda, try_opencl=try_opencl
        )


    def __del__(self):
        self.client.close()
        self.cluster.close()



































# move to worker.py ?
# TODO use_cuda and use_opencl are mutually exclusive for now. See #72.
class NabuWorkerProcess:
    def __init__(self):
        self._get_processing_steps_and_options()


    def _get_processing_steps_and_options(self):
        self.processing_steps = get_dataset("processing_steps")
        # TODO this is likely to be customized for each worker
        self.processing_options = get_dataset("processing_options")
        self.current_chunk = 0 # TODO

    def read_chunk(self):
        self.chunk_reader = ChunkReader(
            self.options["links"],
            sub_region=self.sub_region,
        )
        self.chunk_reader.load_files()


    def flat_field(self):
        # TODO self.options, and get links
        flatfield_cls = FlatField
        flatfield_args = [
            radios,
            flats_links,
            darks_links,
        ]
        flatfield_kwargs = {
            "interpolation": "linear",
            "sub_region": self.sub_region,
        }
        if self.options["use_cuda"]:
            flatfield_cls = CudaFlatField
            flatfield_kwargs["cuda_options"] = None # TODO
        elif self.options["use_opencl"]:
            print("use_opencl: OpenCL backend is not available yet for flat-field")
        self.flatfield = flatfield_cls(
            *flatfield_args,
            **flatfield_kwargs
        )
        print("Flatfield object created") # debug
        print("Flat-field normalization on chunk %d: start" % self.current_chunk) # info
        self.flatfield.normalize_radios()
        print("Flat-field normalization on chunk %d: end" % self.current_chunk) # info












