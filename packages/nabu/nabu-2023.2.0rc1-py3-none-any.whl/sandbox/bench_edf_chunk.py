from time import time
import numpy as np
from silx.third_party.EdfFile import EdfFile as silx_EdfImage
from fabio.edfimage import EdfImage as fabio_EdfImage

def bench_read_chunk_fabio(files, chunk):
    reader = fabio_EdfImage()
    shp = reader.read(files[0])
    data = np.zeros(
        (len(files), ) + (chunk[0].stop - chunk[0].start, chunk[1].stop - chunk[1].start),
        dtype="f"
    )
    t0 = time()
    for i, fname in enumerate(files):
        data[i] = reader.fast_read_roi(fname, chunk)
    el = time() - t0
    return el, data

def bench_read_chunk_silx(files, chunk):
    pos = (chunk[1].start, chunk[0].start)
    size = (chunk[1].stop - chunk[1].start, chunk[0].stop - chunk[0].start)
    data = np.zeros(
        (len(files), ) + size[::-1],
        "f"
    )
    t0 = time()
    for i, fname in enumerate(files):
        reader = silx_EdfImage(fname, access="r", fastedf=True)
        data[i] = reader.GetData(0, Pos=pos, Size=size)
    el = time() - t0
    return el, data
