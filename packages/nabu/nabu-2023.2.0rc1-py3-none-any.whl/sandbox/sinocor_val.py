from nabu.estimation.cor import (
    CenterOfRotationSlidingWindow,
    CenterOfRotationGrowingWindow,
)
from nabu.estimation.cor_sino import SinoCor
from nabu.resources.logger import LoggerOrPrint
from nabu.utils import check_supported
from nabu.pipeline.estimators import update_func_kwargs

class SinoCORFinderHalfAcquisition:
    """
    A class for finding Center of Rotation based on 360 degrees sinograms.
    This class handles the steps of building the sinogram from raw radios.
    """

    search_methods = ["sino-coarse-to-fine", "sliding-window", "growing-window"]
    default_method = "sino-coarse-to-fine"
    _default_cor_options = {"side": "right"} # half-acquisition

    def __init__(self, sinogram, cor_options=None, logger=None):
        """
        Initialize a SinoCORFinder object.
        This class estimates the center of rotation (CoR) using a variety of available methods.
        It assumes a 360 degrees sinogram with half-acquisition.

        Parameters
        ---------
        cor_options: str
            User options for the auto-CoR method.
        logger: Logger, optional
            Logging object
        """
        self.logger = LoggerOrPrint(logger)
        self.sinogram = sinogram
        self._get_cor_options(cor_options)

    def _get_cor_options(self, cor_options):
        self.cor_options = self._default_cor_options.copy()
        self.cor_options.update(cor_options or {})

    @staticmethod
    def _split_sinogram(sinogram):
        n_a_2 = sinogram.shape[0] // 2
        img_1, img_2 = sinogram[:n_a_2], sinogram[n_a_2:]
        return img_1, img_2

    def _find_cor_sliding_window(self):
        cor_finder = CenterOfRotationSlidingWindow(logger=self.logger)

        img_1, img_2 = self._split_sinogram(self.sinogram)
        kwargs = update_func_kwargs(cor_finder.find_shift, self.cor_options)
        side = self.cor_options.get("side", "right")
        kwargs.pop("side", None)
        self.logger.debug("CenterOfRotationSlidingWindow.find_shift(%s)" % str(kwargs))
        cor = cor_finder.find_shift(img_1, img_2, side, **kwargs)
        return cor + self.sinogram.shape[1] / 2.0

    def _find_cor_growing_window(self):
        cor_finder = CenterOfRotationGrowingWindow(logger=self.logger)

        img_1, img_2 = self._split_sinogram(self.sinogram)
        kwargs = update_func_kwargs(cor_finder.find_shift, self.cor_options)
        self.logger.debug("CenterOfRotationGrowingWindow.find_shift(%s)" % str(kwargs))
        cor = cor_finder.find_shift(img_1, img_2, **kwargs)

        return cor + self.sinogram.shape[1] / 2.0

    def _find_cor_coarse2fine(self):
        side = self.cor_options.get("side", "right")
        window_width = self.cor_options.get("window_width", None)
        neighborhood = self.cor_options.get("neighborhood", 7)
        shift_value = self.cor_options.get("shift_value", 0.1)
        cor_finder = SinoCor(self.sinogram, logger=self.logger)
        self.logger.debug("SinoCor.estimate_cor_coarse(side=%s, window_width=%s)" % (str(side), str(window_width)))
        cor_finder.estimate_cor_coarse(side=side, window_width=window_width)
        self.logger.debug("SinoCor.estimate_cor_fine(neighborhood=%s, shift_value=%s)" % (str(neighborhood), str(shift_value)))
        cor = cor_finder.estimate_cor_fine(neighborhood=neighborhood, shift_value=shift_value)
        return cor

    def find_cor(self, method=None):
        method = method or self.default_method
        cor_estimation_function = {
            "sino-coarse-to-fine": self._find_cor_coarse2fine,
            "sliding-window": self._find_cor_sliding_window,
            "growing-window": self._find_cor_growing_window,
        }
        check_supported(method, cor_estimation_function.keys(), "sinogram-based CoR estimation method")
        res = cor_estimation_function[method]()
        return res

