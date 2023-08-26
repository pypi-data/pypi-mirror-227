from itertools import product
from functools import lru_cache
import numpy as np
from nabu.utils import get_num_threads

from benchmarker import Benchmark

from silx.math.fft.fftw import FFTW
from scipy.fft import rfft, rfft2


small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 73]
some_primes = [
    179,
    283,
    419,
    547,
    661,
    811,
    947,
    1087,
    1229,
    1381,
    1523,
    1663,
    1823,
    1993,
    2131,
    2293,
    2437,
    2621,
    2749,
    2909,
    3083,
    3259,
    3433,
]

@lru_cache(maxsize=5)
def generate_sizes(primes, maxpows, min_val=100, max_val=1e9):
    """
    Generate a list of powers of prime numbers.
    For example, if 'primes_with_maxpows' is {2: 3, 3*2, 5:1},
    it will generates 2**a * 3**b * 5**c with a <= 3, b <= 2, c <= 1
    """
    valuations = []
    for maxpow in maxpows:
        minval = 0
        valuations.append(range(minval, maxpow + 1))
    powers = product(*valuations)
    res = []
    for pw in powers:
        l = [prime_ ** power_ for prime_, power_ in zip(primes, pw)]
        val = np.prod(l)
        if val < min_val or val > max_val:
            continue
        res.append(val)
        # res.append(np.prod(list(map(lambda x: x[0] ** x[1], zip(primes, pw)))))
    return np.unique(res)




sizes1D = generate_sizes(tuple(small_primes), tuple([10, 8, 5, 3, 2, 2, 1, 1, 1, 1, 1]), min_val=1000)
sizes1D = sizes1D[::100]



def bench_fft(sizes, n_threads=None, verbose=False):

    if n_threads is None:
        n_threads = get_num_threads()

    bench = Benchmark()
    bench.new_figure("rfft 2D", xlims=(sizes[0], sizes[-1]), xlabel="size", ylabel="time (ms)", xlog=False, ylog=False)


    bench.new_curve("numpy")
    bench.new_curve("scipy")
    # bench.new_curve("FFTW")

    for s in sizes:

        data = np.random.rand(s).astype("f")

        fftw = FFTW(template=data, num_threads=n_threads)

        bench.add_bench_result(
            "numpy", s, np.fft.rfft2, nexec=3, mode="best", command_args=(data, ), verbose=verbose
        )
        bench.add_bench_result(
            "scipy", s, rfft2, nexec=3, mode="best", command_args=(data, ), command_kwargs={"workers": n_threads}, verbose=verbose
        )
        bench.add_bench_result(
            "FFTW", s, fftw.fft, nexec=3, mode="best", command_args=(data, ), verbose=verbose
        )

    bench.fit_plots_to_fig()
    bench.legend()



def bench_fft2D(sizes, n_threads=None, verbose=False):

    if n_threads is None:
        n_threads = get_num_threads()

    bench = Benchmark()
    bench.new_figure("rfft 2D", xlims=(np.product(sizes, axis=1).min(), np.product(sizes, axis=1).max()), xlabel="size", ylabel="time (ms)", xlog=False, ylog=False)


    bench.new_curve("numpy")
    bench.new_curve("scipy")
    bench.new_curve("FFTW")

    for s in sizes:

        data = np.random.rand(np.prod(s)).reshape(s).astype("f")

        fftw = FFTW(template=data, num_threads=n_threads)

        bench.add_bench_result(
            "numpy", np.prod(s), np.fft.rfft2, nexec=3, mode="best", command_args=(data, ), verbose=verbose
        )
        bench.add_bench_result(
            "scipy", np.prod(s), rfft2, nexec=3, mode="best", command_args=(data, ), command_kwargs={"workers": n_threads}, verbose=verbose
        )
        bench.add_bench_result(
            "FFTW", np.prod(s), fftw.fft, nexec=3, mode="best", command_args=(data, ), verbose=verbose
        )

    bench.fit_plots_to_fig()
    bench.legend()
















