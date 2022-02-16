import collections
import palettable

import matplotlib as mpl
from matplotlib import cm
import numpy as np
from sklearn.preprocessing import QuantileTransformer
import matplotlib.pyplot as plt


class NamedColors(object):
    def __init__(self):
        self._colors = palettable.cartocolors.qualitative.Prism_9.mpl_colors
        self.red = self._colors[7]
        self.blue = self._colors[1]
        self.green = self._colors[3]
        self.orange = self._colors[6]
        self.purple = self._colors[8]
        self.yellow = self._colors[5]
        self.gray = (211, 211, 211)


class Palette(object):
    def __init__(self, shuffle=True):
        self.colors = palettable.cartocolors.qualitative.Prism_10.mpl_colors
        self.is_shuffled = shuffle
        if shuffle:
            idxs = [i for i in range(len(self.colors))]
            self.colors = [self.colors[i] for i in idxs]
        self.cur_i = 0

    def next(self):
        if self.cur_i > len(self.colors):
            self.cur_i = 0
        color = self.colors[self.cur_i]
        self.cur_i += 1
        return color

    def sample(self, n):
        colors = []
        for _ in range(n):
            colors += [self.next()]
        return colors


class ColorMap(object):
    def __init__(self, scientific=True):
        self.scientific = scientific

    def uniform(self):
        pass

    def sequential(self):
        pass

    def diverging(self):
        pass


class Colors(NamedColors):
    def __init__(self, cmap_name="Spectral", empty=None):
        NamedColors.__init__(self, empty=empty)
        self.cmap_name = cmap_name
        self.empty = empty
        self.cmap = cm.get_cmap(self.cmap_name)
        self.transformer = None
        self.fit_type = None

    def _maximally_different_values(self):
        pass

    def fit_categorical(self, data, spread=True):

        self.fit_type = "categorical"

    def fit_continuous(self, data):

        self.fit_type = "continuous"

    def fit_limits(self, vmin, vmax):

        self.fit_type = "limits"

    def sample(self, n, spread=True):
        values = np.linspace(0, 1, n)
        norm = mpl.colors.Normalize(vmin=0, vmax=1)
        values = [norm(x) for x in values]
        return [self.cmap(x) for x in values]

    def transform(self, data):
        pass

    def sample(self, n):
        values = np.linspace(0, 1, n)
        norm = mpl.colors.Normalize(vmin=0, vmax=1)
        values = [norm(x) for x in values]
        return [self.cmap(x) for x in values]

    def from_categories(self, categories, spread_by_counts=True, empty_category=-1):
        categories_counts = collections.defaultdict(int)
        for c in categories:
            categories_counts[c] += 1
        cats = sorted(categories_counts.keys())
        colors = self.sample(len(cats))
        cat2col = {}
        for cat, col in zip(cats, colors):
            if cat == empty_category:
                cat2col[cat] = self.empty
            else:
                cat2col[cat] = col
        return [cat2col[c] for c in categories]

    def from_values(self, values, method="uniform"):
        values = np.array(values).reshape(-1, 1)
        if self.transformer is None:
            self.transformer = QuantileTransformer(output_distribution=method)
            self.transformer.fit(values)
            if method == "uniform":
                vmin = 0
                vmax = 1
            else:
                values = self.transformer.transform(values).ravel()
                vmin = np.percentile(values, 1)
                vmax = np.percentile(values, 99)
            self.from_values_norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
        values = self.transformer.transform(values).ravel()
        values = [self.from_values_norm(x) for x in values]
        colors = self.cmap(values)
        return colors
