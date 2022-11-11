import random
import numpy as np

import matplotlib as mpl
from matplotlib import cm
from cmcrameri import cm as cms
import palettable
from matplotlib import colors

from sklearn.preprocessing import QuantileTransformer

from ..utils import lighten_color, set_transparency


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
        self.white = tuple(list(colors.to_rgba("white"))[:3])
        self.black = tuple(list(colors.to_rgba("black"))[:3])

    def _get(self, color_name, alpha=None, lighten=None):
        if color_name == "red":
            return self.red
        if color_name == "blue":
            return self.blue
        if color_name == "green":
            return self.green
        if color_name == "orange":
            return self.orange
        if color_name == "purple":
            return self.purple
        if color_name == "yellow":
            return self.yellow
        if color_name == "gray":
            return self.gray
        if color_name == "white":
            return self.white
        if color_name == "black":
            return self.black

    def get(self, color_name, alpha=None, lighten=None):
        color = self._get(color_name)
        if lighten is not None:
            color = lighten_color(color, factor=lighten)
        if alpha is not None:
            color = set_transparency(color, alpha)
        return color


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

    def get(self, cmap_name):
        if cmap_name == "viridis":
            return self.viridis
        if cmap_name == "spectral":
            return self.spectral
        if cmap_name == "coolwarm":
            return self.coolwarm


class Palette(object):
    def __init__(self, shuffle=False):
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
    def __init__(self, cmap="spectral", transformation="uniform", ascending=True):
        if type(cmap) is str:
            self.cmap = NamedColorMaps().get(cmap)
        else:
            self.cmap = cmap
        self.transformation = transformation
        self.ascending = ascending

    def fit(self, data):
        data = np.array(data)
        if not self.ascending:
            data = -data
        if self.transformation is not None:
            values = np.array(data).reshape(-1, 1)
            self.transformer = QuantileTransformer(
                n_quantiles=min(len(values), 1000),
                output_distribution=self.transformation,
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
        data = np.array(data)
        if not self.ascending:
            data = -data
        if self.transformer:
            values = np.array(data).reshape(-1, 1)
            values = self.transformer.transform(values).ravel()
        else:
            values = np.array(data)
        colors = [self.cmap(self.color_normalizer(v)) for v in values]
        return colors

    def get(self, data, alpha=None, lighten=None):
        colors = self.transform(data)
        if lighten is not None:
            colors = [lighten_color(c) for c in colors]
        if alpha is not None:
            colors = [set_transparency(c) for c in colors]
        return colors

    def sample(self, n, shuffle=False):
        values = np.linspace(0, 1, n)
        norm = mpl.colors.Normalize(vmin=0, vmax=1)
        values = [norm(x) for x in values]
        if shuffle:
            random.shuffle(values)
        return [self.cmap(x) for x in values]


class CategoricalColorMap(object):
    pass
