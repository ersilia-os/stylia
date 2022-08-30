import random
import numpy as np

import matplotlib as mpl
from matplotlib import cm
from cmcrameri import cm as cms  # scientific colormaps
import palettable
from matplotlib import colors

from sklearn.preprocessing import QuantileTransformer


CONTINUOUS_CMAP_PERCENITLE_CUTS = (1, 99)


class NamedColors(object):
    def __init__(self):
        self._colors = palettable.cartocolors.qualitative.Prism_9.mpl_colors
        self.red = self._colors[7]
        self.blue = self._colors[1]
        self.green = self._colors[3]
        self.orange = self._colors[6]
        self.purple = self._colors[8]
        self.yellow = self._colors[5]
        self.gray = tuple(list(colors.to_rgba("lightgray"))[:3])


class NamedColorMaps(object):
    def __init__(self, scientific=True):
        self._scientific = scientific
        if scientific:
            self.viridis = cms.imola
            self.spectral = cms.roma
            self.coolwarm = cms.vik
        else:
            self.viridis = cm.get_cmap("viridis")
            self.spectral = cm.get_cmap("Spectral")
            self.coolwarm = cm.get_cmap("coolwarm")


class Palette(object):
    def __init__(self, shuffle=True):
        self.colors = palettable.cartocolors.qualitative.Prism_10.mpl_colors
        self.is_shuffled = shuffle
        if shuffle:
            idxs = [i for i in range(len(self.colors))]
            random.shuffle(idxs)
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


class ContinuousColorMap(object):
    def __init__(self, cmap, transformation="uniform"):
        self.cmap = cmap
        self.transformation = transformation

    def fit(self, data):
        if self.transformation is not None:
            values = np.array(data).reshape(-1, 1)
            self.transformer = QuantileTransformer(
                output_distribution=self.transformation
            )
            self.transformer.fit(values)
            if self.transformation == "uniform":
                self.vmin = 0
                self.vmax = 1
            else:
                values = self.transformer.transform(values).ravel()
                self.vmin = np.percentile(values, CONTINUOUS_CMAP_PERCENITLE_CUTS[0])
                self.vmax = np.percentile(values, CONTINUOUS_CMAP_PERCENITLE_CUTS[1])
        else:
            self.transformer = None
            values = np.array(data)
            self.vmin = np.percentile(values, CONTINUOUS_CMAP_PERCENITLE_CUTS[0])
            self.vmax = np.percentile(values, CONTINUOUS_CMAP_PERCENITLE_CUTS[1])
        self.color_normalizer = mpl.colors.Normalize(vmin=self.vmin, vmax=self.vmax)

    def transform(self, data):
        if self.transformer:
            values = np.array(data).reshape(-1, 1)
            values = self.transformer.transform(values).ravel()
        else:
            values = np.array(data)
        colors = [self.cmap(self.color_normalizer(v)) for v in values]
        return colors

    def sample(self, n, shuffle=False):
        values = np.linspace(0, 1, n)
        norm = mpl.colors.Normalize(vmin=0, vmax=1)
        values = [norm(x) for x in values]
        if shuffle:
            random.shuffle(values)
        return [self.cmap(x) for x in values]


""""

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

"""
