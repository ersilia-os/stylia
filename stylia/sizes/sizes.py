import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

from ..vars import FONTSIZE_SMALL, FONTSIZE, LINEWIDTH, MARKERSIZE


class FontSize(object):
    def __init__(self):
        self._set_rc_params()

    def _set_rc_params(self):
        plt.rc("font", size=FONTSIZE_SMALL)
        plt.rc("axes", titlesize=FONTSIZE)
        plt.rc("axes", labelsize=FONTSIZE)
        plt.rc("xtick", labelsize=FONTSIZE)
        plt.rc("ytick", labelsize=FONTSIZE)
        plt.rc("legend", fontsize=FONTSIZE)
        plt.rc("figure", titlesize=FONTSIZE)


class MarkerSize(object):
    def __init__(self):
        self._set_rc_params()

    def _set_rc_params(self):
        mpl.rcParams["axes.linewidth"] = LINEWIDTH
        mpl.rcParams["lines.markersize"] = np.sqrt(MARKERSIZE)
        mpl.rcParams["lines.linewidth"] = LINEWIDTH
