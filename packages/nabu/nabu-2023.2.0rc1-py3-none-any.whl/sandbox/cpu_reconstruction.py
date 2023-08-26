import numpy as np
from nabu.pipeline.fullfield.processconfig import ProcessConfig
from nabu.pipeline.fullfield.chunked import ChunkedPipeline
from nabu.pipeline.fullfield.grouped import GroupedPipeline, SinoStackPipeline

if __name__ == "__main__":
    proc = ProcessConfig("/data/pierre/benchs/stylo.conf")

    #C = ChunkedPipeline(proc, (0, 400))
    #C.process_chunk()

    G = GroupedPipeline(proc, (0, 7000), sub_region=(None, None, 0, 2160//3))
    G.process_group()
    S = SinoStackPipeline(proc, (0, 7000), G.radios)
    S.process_stack()
