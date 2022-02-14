class FigureSize(object):

    def __init__(self, support="slide", page_columns=2, area_proportion=1, aspect_ratio=(1,1)):
        assert support in ["slide", "paper"], "Available supports are 'slide' and 'paper'"
        assert page_columns in [1, 2], "Page columns can only be 1 (half the width) or 2 (full width)"
        assert area_proportion <= 1, "Area proportion must be between 0 and 1"
        self.support = support        
        self.page_columns = page_columns
        self.area_proportion = area_proportion
        self.aspect_ratio = aspect_ratio
        if self.support == "slide":
            self.set_width_slide()
        else:
            self.set_width_paper()

    @staticmethod
    def _mm_to_inch(x):
        return x*0.0393701

    def set_width_paper(self):
        if self.page_columns == 2:
            self.width = self._mm_to_inch(183) # Nature
        else:
            self.width = self._mm_to_inch(89)

    def set_width_slide(self):
        if self.page_columns == 2:
            self.width = self._mm_to_inch(25.4) # PowerPoint
        else:
            self.width = self._mm_to_inch(25.4/2)

    def set_height_paper(self):
        pass

    def set_height_slide(self):
        pass

    def size(self):
        pass


class AxisManager(object):

    def __init__(self, axs):
        self.axs_flat = axs.flatten()
        self.current_i = 0

    def next(self):
        ax = self.axs_flat[self.current_i]
        self.current_i += 1
        return ax

    def get(self, xy=None):
        if xy is None:
            return self.next()
        else:
            return self.axs[xy[0], xy[1]]



