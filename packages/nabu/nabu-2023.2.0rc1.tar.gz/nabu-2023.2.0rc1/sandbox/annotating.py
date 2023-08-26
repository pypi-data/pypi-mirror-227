#!/usr/bin/env python
# module to ignore when running mypy
import numpy as np
#import pyopencl
#import pycuda
from typing import Union


def func(s: str) -> str:
    return "ok"

def add(a: int, b: int) -> int:
    return a+b

def test():
    func(1) # invalid
    add(2) # invalid

test(oO) # invalid 

def proc(shape: tuple, dtype: Union[str, np.dtype]) -> None:
    print(shape)
    print(np.dtype(dtype))


def main():
    print("hello")
    s = func("test")
    i = add(1, "dsf") # invalid: type
    func(1) # invalid: type
    proc((1, 2), "f") # ok
    proc((2, 3), np.float32) # ok
    proc(1, 2) # invalid: types


#if __name__ == "__main__":
#    main()