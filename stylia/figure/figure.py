from ..sizes.sizes import FontSize
from ..sizes import SUPPORT_TWO_COLUMN_LIMITS, to_one_column
from ..colors.colors import Palette


def stylize(ax):
    ax.set_prop_cycle("color", Palette().colors)
    ax.set_xlabel("X-axis / Units")
    ax.set_ylabel("Y-axis / Units")
    ax.set_title("Plot title")
    return ax


# predefined


class FigureSize(object):
    def __init__(
        self, support="slide", page_columns=2, area_proportion=1, aspect_ratio=None
    ):
        assert support in [
            "slide",
            "widescreen",
            "paper",
            "poster",
        ], "Available supports are 'slide', 'widescreen', 'paper', 'poster'"
        assert page_columns in [
            1,
            2,
        ], "Page columns can only be 1 (half the width) or 2 (full width)"
        self.support = support
        self.page_columns = page_columns
        self.area_proportion = area_proportion
        self.aspect_ratio = aspect_ratio
        width, height = SUPPORT_TWO_COLUMN_LIMITS[support]
        if page_columns == 1:
            width = to_one_column(width)
        width = width * area_proportion
        if area_proportion > 1:
            height = height * area_proportion
        if aspect_ratio is None:
            self.width = width
            self.height = height
        else:
            height_ = width * aspect_ratio[1] / aspect_ratio[0]
            if height_ < height:
                self.width = width
                self.height = height_
            else:
                self.height = height
                self.width = height * aspect_ratio[0] / aspect_ratio[1]
        FontSize(support=self.support)

    def size(self):
        return self.width, self.height


class AxisManager(object):
    def __init__(self, axs):
        if type(axs) is list:
            self.axs_flat = axs[0]
        else:
            self.axs_flat = axs.flatten()
        self.axs = axs
        self.current_i = 0

    def __getitem__(self, key):
        if type(key) is int:
            i = key
            ax = self.axs_flat[i]
        else:
            i, j = key
            ax = self.axs[i, j]
        ax = stylize(ax)
        return ax

    def next(self):
        ax = self.axs_flat[self.current_i]
        self.current_i += 1
        ax = stylize(ax)
        return ax
