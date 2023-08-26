#!/usr/bin/env python
import numpy as np
from nabu.reconstruction.fbp import Backprojector
from nabu.testutils import get_data

if __name__ == "__main__":
    s = get_data("mri_sino500.npz")["data"]
    B = Backprojector(s.shape)
    B.fbp(s)