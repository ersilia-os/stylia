import collections

import matplotlib as mpl
from matplotlib import cm
import numpy as np
from sklearn.preprocessing import QuantileTransformer
import matpltolib.pyplot as plt



class ColorIdeas(object):

    def __init__(self):
        pass

    def ideas(self):
        ideas = {
            "diverging": ["Spectral", "coolwarm"],
            "uniform": ["viridis", "plasma"],
            "sequential": ["YlGnBu"]
        }
        return ideas


class ColorMaps(object):

    def __init__(self, scientific=True):
        self.scientific = scientific

    def sequential(self):
        pass

    def diverging(self):
        pass

    def cyclic(self):
        pass


class NamedColors(ColorIdeas):

    def __init__(self, palette, empty):
        ColorIdeas.__init__(self)
        self._set_bokeh()
        self._empty = empty

    def _set_bokeh(self):
        self._red = '#EC1557'
        self._orange = '#F05223'
        self._yellow = '#F6A91B'
        self._lightgreen = '#A5CD39'
        self._green = '#20B254'
        self._lightblue = '#00AAAE'
        self._blue = '#4998D3'
        self._purple = '#892889'

    @property
    def red(self):
        return self._red()

    @property
    def orange(self):
        return self._orange()

    @property
    def yellow(self):
        return self._yellow()

    @property
    def green(self):
        return self._green()

    @property
    def blue(self):
        return self._blue()


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
        
    def fit_continuous(self, data)
        
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
        values = np.array(values).reshape(-1,1)
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