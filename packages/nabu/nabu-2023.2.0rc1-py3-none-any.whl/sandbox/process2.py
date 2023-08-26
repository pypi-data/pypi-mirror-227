#!/usr/bin/env python

from nabu.resources.processconfig import ProcessConfig
from nabu.app.process import WorkerProcess
from nabu.resources.tasks import build_processing_steps


if __name__ == "__main__":
    conf = ProcessConfig("/home/pierre/notebooks/nabu/nabu.conf")
    steps, options = build_processing_steps(conf)
    for stuff in ["unsharp_mask", "reconstruction", "save"]: # ['read_chunk', 'flatfield', 'ccd_correction', 'phase', 'take_log']
        steps.remove(stuff)
        options.pop(stuff)
    Wp = WorkerProcess(steps, options, conf.dataset_infos, (None, None, None, 400), chunk_size=400)
    Wp.process_chunk()

