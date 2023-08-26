#!/usr/bin/env python
from nabu.pipeline.fullfield.processconfig import ProcessConfig
from nabu.pipeline.fullfield.local_reconstruction import GroupedReconstructor, ChunkedReconstructor
from nabu.pipeline.fullfield.chunked_cuda import CudaChunkedPipeline
from nabu.preproc.ccd_cuda import CudaLog


proc = ProcessConfig("/data/pierre/benchs/stylo.conf", create_logger=True)
#C = CudaChunkedPipeline(proc, (218, 448), phase_margin=((0, 0), (0, 0)), logger=proc.logger)
#C = CudaChunkedPipeline(proc, (218, 318), phase_margin=((0, 0), (0, 0)), logger=proc.logger)
C = CudaChunkedPipeline(proc, (218, 220), phase_margin=((0, 0), (0, 0)), logger=proc.logger)
C.process_chunk()
