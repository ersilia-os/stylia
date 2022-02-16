import palettable
from ..sizes.sizes import FontSize


class FigureSize(object):
    def __init__(
        self, support="slide", page_columns=2, area_proportion=1, aspect_ratio=(1, 1)
    ):
        assert support in [
            "slide",
            "paper",
        ], "Available supports are 'slide' and 'paper'"
        assert page_columns in [
            1,
            2,
        ], "Page columns can only be 1 (half the width) or 2 (full width)"
        assert area_proportion <= 1, "Area proportion must be between 0 and 1"
        self.support = support
        self.page_columns = page_columns
        self.area_proportion = area_proportion
        self.aspect_ratio = aspect_ratio
        if self.support == "slide":
            self.set_width_slide()
            self.set_height_slide()
        else:
            self.set_width_paper()
            self.set_height_paper()
        FontSize(support=self.support)

    @staticmethod
    def _mm_to_inch(x):
        return x * 0.0393701

    def set_width_paper(self):
        if self.page_columns == 2:
            self.width = self._mm_to_inch(183)  # Nature
        else:
            self.width = self._mm_to_inch(89)
        self.width = self.width * self.area_proportion

    def set_width_slide(self):
        if self.page_columns == 2:
            self.width = 10  # PowerPoint standard screen. If widescreen, 13.3
        else:
            self.width = 10 / 2
        self.width = self.width * self.area_proportion

    def set_height_paper(self):
        self.height = self.width * self.aspect_ratio[1] / self.aspect_ratio[0]
        assert self.height <= self._mm_to_inch(
            275
        ), "Specified aspect ratio cannot be fitted into the plotting area"

    def set_height_slide(self):
        self.height = self.width * self.aspect_ratio[1] / self.aspect_ratio[0]
        assert (
            self.height <= 5.625
        ), "Specified aspect ratio cannot be fitted into the plotting area"  # Standard screen. If widescreen, 7.5

    def size(self):
        return self.width, self.height


class AxisManager(object):
    def __init__(self, axs):
        self.axs_flat = axs.flatten()
        self.current_i = 0

    def next(self):
        ax = self.axs_flat[self.current_i]
        self.current_i += 1
        ax.set_prop_cycle(
            "color", palettable.cartocolors.qualitative.Prism_10.mpl_colors
        )  # To-do decide a by-default palette
        ax.set_xlabel("X-axis / Units")
        ax.set_ylabel("Y-axis / Units")
        ax.set_title("Plot title")
        return ax

    def get(self, xy=None):
        if xy is None:
            return self.next()
        else:
            return self.axs[xy[0], xy[1]]
