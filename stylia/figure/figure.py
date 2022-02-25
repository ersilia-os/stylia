from ..sizes.sizes import FontSize
from ..colors.colors import Palette


def mm_to_inch(x):
    return x * 0.0393701


def to_one_column(width):
    return width * 89 / 183  # Nature two:one column ratio


SUPPORT_TWO_COLUMN_LIMITS = {
    "paper": (mm_to_inch(183), mm_to_inch(275)),  # Nature
    "slide": (10, 5.625),  # Standard slide
    "widescreen": (13.3, 7.5),  # Widescreen
    "poster": (mm_to_inch(420), mm_to_inch(594)),  # A2
}


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
        self.current_i = 0

    def next(self):
        ax = self.axs_flat[self.current_i]
        self.current_i += 1
        ax = stylize(ax)
        return ax

    def get(self, xy=None):
        if xy is None:
            return self.next()
        else:
            return self.axs[xy[0], xy[1]]


def stylize(ax):
    ax.set_prop_cycle("color", Palette().colors)
    ax.set_xlabel("X-axis / Units")
    ax.set_ylabel("Y-axis / Units")
    ax.set_title("Plot title")
    return ax
