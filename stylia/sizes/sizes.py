import matplotlib.pyplot as plt

from . import SUPPORT_TWO_COLUMN_LIMITS


class FontSize(object):
    def __init__(self, support):
        if support == "paper":
            self.SMALL_SIZE = 5
            self.MEDIUM_SIZE = 7
            self.BIGGER_SIZE = 8
        else:
            self.SMALL_SIZE = 8
            self.MEDIUM_SIZE = 10
            self.BIGGER_SIZE = 12
        self._set_rc_params()

    def _set_rc_params(self):
        plt.rc("font", size=self.SMALL_SIZE)
        plt.rc("axes", titlesize=self.MEDIUM_SIZE)
        plt.rc("axes", labelsize=self.MEDIUM_SIZE)
        plt.rc("xtick", labelsize=self.MEDIUM_SIZE)
        plt.rc("ytick", labelsize=self.MEDIUM_SIZE)
        plt.rc("legend", fontsize=self.MEDIUM_SIZE)
        plt.rc("figure", titlesize=self.MEDIUM_SIZE)


class SupportSize(object):
    def __init__(self, support):
        self.support = support

    def get_limits(self):
        return SUPPORT_TWO_COLUMN_LIMITS[self.support]
