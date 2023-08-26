import os
import numpy as np
from nabu.utils import view_as_images_stack
from nabu.pipeline.fullfield.processconfig import ProcessConfig
from nabu.pipeline.fullfield.reconstruction import FullFieldReconstructor


def whoami():
    ret = None
    try:
        ret = os.getlogin()
    except OSError: # can happen eg. in a SLURM reservation
        ret = os.environ.get("LOGNAME", None)
    return ret


def reset_backprojector_cor(backprojector, cor):
    """
    Hack a backprojector to reset the CoR
    """
    backprojector.rot_center = cor
    backprojector.axis_pos = cor
    backprojector.kern_proj_args[3] = cor
    if backprojector.extra_options["centered_axis"]:
        backprojector.offsets = {
            "x": round(backprojector.rot_center - (backprojector.n_x - 1) / 2.0),
            "y": round(backprojector.rot_center - (backprojector.n_y - 1) / 2.0),
        }
        backprojector.kern_proj_args[6] = backprojector.offsets["x"]
        backprojector.kern_proj_args[7] = backprojector.offsets["y"]


def reconstruct_multicor(conf_fname, cors, return_all_recs=False):
    proc = ProcessConfig(conf_fname)
    reconstructor = FullFieldReconstructor(proc)

    if reconstructor.delta_z > 1:
        raise ValueError("Only slice reconstruction can be used (have delta_z = %d)" % reconstructor.delta_z)

    reconstructor.reconstruct() # warm-up, spawn pipeline
    pipeline = reconstructor.pipeline
    file_prefix = pipeline.processing_options["save"]["file_prefix"]

    all_recs = []

    for cor in cors:
        # Re-configure with new CoR
        pipeline.processing_options["reconstruction"]["rotation_axis_position"] = cor
        pipeline.processing_options["save"]["file_prefix"] = file_prefix + "_%.03f" % cor
        reset_backprojector_cor(pipeline.reconstruction, cor)
        pipeline._init_writer()

        # Get sinogram
        sino = pipeline.sino_builder.get_sino(pipeline._d_radios, 0)

        # Run reconstruction
        rec = pipeline.reconstruction.fbp(sino)
        if return_all_recs:
            all_recs.append(rec)
        rec_3D = view_as_images_stack(rec) # writer wants 3D data

        # Write
        pipeline.writer.write_data(rec_3D)
        print("Wrote %s" % pipeline.writer.fname)

    if return_all_recs:
        return np.array(all_recs)

