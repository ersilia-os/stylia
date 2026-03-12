import random
import numpy as np

import matplotlib as mpl
from matplotlib import colors as mcolors

from sklearn.preprocessing import QuantileTransformer

from ..utils import lighten_color, set_transparency


CONTINUOUS_CMAP_PERCENTILE_CUTS = (1, 99)


def _hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) / 255.0 for i in (0, 2, 4))


# ---------------------------------------------------------------------------
# Named colors
# ---------------------------------------------------------------------------
# Ersilia brand colors (from ersilia.io brand guidelines) take precedence;
# NPG fills in hues the brand palette does not cover (red, teal, green, brown).

# ---------------------------------------------------------------------------
# PaperColors — NPG-derived palette with evocative names for publications
# ---------------------------------------------------------------------------

_PAPER = {
    "crimson":    "#E64B35",  # NPG vermillion-red
    "cobalt":     "#3C5488",  # NPG deep navy-blue
    "sky":        "#4DBBD5",  # NPG sky-teal
    "jade":       "#00A087",  # NPG sea-green
    "coral":      "#F39B7F",  # NPG soft coral
    "periwinkle": "#8491B4",  # NPG muted blue-violet
    "seafoam":    "#91D1C2",  # NPG pale seafoam
    "scarlet":    "#DC0000",  # NPG vivid red
    "umber":      "#7E6148",  # NPG warm brown
    "sand":       "#B09C85",  # NPG light tan
    # neutrals
    "white":      "#FFFFFF",
    "black":      "#2C3E50",  # soft off-black
}

_PAPER_ORDER = [
    "crimson", "cobalt", "sky", "jade", "coral",
    "periwinkle", "seafoam", "scarlet", "umber", "sand",
]


class PaperColors:
    """Individual, semantically named colors for publication-quality figures.

    Colors are drawn from the NPG (Nature Publishing Group) palette and given
    evocative names suited for annotating specific plot elements.

    Example
    -------
    >>> nc = PaperColors()
    >>> ax.scatter(x, y, color=nc.crimson)
    >>> ax.scatter(x, y, color=nc.get("cobalt", alpha=0.6))
    """

    def __init__(self):
        for name, hex_val in _PAPER.items():
            setattr(self, name, _hex_to_rgb(hex_val))

    @property
    def hex(self):
        """Return all colors as a dict of hex strings."""
        return dict(_PAPER)

    def get(self, color_name, alpha=None, lighten=None):
        color = getattr(self, color_name)
        if lighten is not None:
            color = lighten_color(color, factor=lighten)
        if alpha is not None:
            color = set_transparency(color, alpha)
        return color

    def __getitem__(self, idx):
        """Access colors by index or slice, in palette order (excludes white/black)."""
        if isinstance(idx, slice):
            return [getattr(self, name) for name in _PAPER_ORDER[idx]]
        return getattr(self, _PAPER_ORDER[idx])

    def __len__(self):
        return len(_PAPER_ORDER)

    def __iter__(self):
        """Yield colors in palette order (excludes white/black)."""
        for name in _PAPER_ORDER:
            yield getattr(self, name)


# ---------------------------------------------------------------------------
# ErsiliaColors — official Ersilia brand palette
# ---------------------------------------------------------------------------

_ERSILIA_NAMED = {
    "plum":   "#50285A",  # Ersilia primary – deep plum purple
    "purple": "#AA96FA",  # Ersilia accent – soft lavender purple
    "mint":   "#BEE6B4",  # Ersilia mint green
    "blue":   "#8CC8FA",  # Ersilia sky blue
    "yellow": "#FAD782",  # Ersilia warm yellow
    "pink":   "#DCA0DC",  # Ersilia mauve pink
    "orange": "#FAA08C",  # Ersilia soft orange
    "gray":   "#D2D2D0",  # Ersilia light gray
    # neutrals
    "white":  "#FFFFFF",
    "black":  "#2C3E50",  # soft off-black
}

_ERSILIA_ORDER = ["plum", "purple", "mint", "blue", "yellow", "pink", "orange", "gray"]


class ErsiliaColors:
    """Official Ersilia brand colors for use in Ersilia-branded figures.

    Colors follow the Ersilia brand guidelines (ersilia.gitbook.io/ersilia-book).

    Example
    -------
    >>> ec = ErsiliaColors()
    >>> ax.scatter(x, y, color=ec.plum)
    >>> ax.scatter(x, y, color=ec.get("blue", alpha=0.6))
    """

    def __init__(self):
        for name, hex_val in _ERSILIA_NAMED.items():
            setattr(self, name, _hex_to_rgb(hex_val))

    @property
    def hex(self):
        """Return all colors as a dict of hex strings."""
        return dict(_ERSILIA_NAMED)

    def get(self, color_name, alpha=None, lighten=None):
        color = getattr(self, color_name)
        if lighten is not None:
            color = lighten_color(color, factor=lighten)
        if alpha is not None:
            color = set_transparency(color, alpha)
        return color

    def __getitem__(self, idx):
        """Access colors by index or slice, in palette order (excludes white/black)."""
        if isinstance(idx, slice):
            return [getattr(self, name) for name in _ERSILIA_ORDER[idx]]
        return getattr(self, _ERSILIA_ORDER[idx])

    def __len__(self):
        return len(_ERSILIA_ORDER)

    def __iter__(self):
        """Yield colors in palette order (excludes white/black)."""
        for name in _ERSILIA_ORDER:
            yield getattr(self, name)


# backward-compat alias
NamedColors = PaperColors


# ---------------------------------------------------------------------------
# Categorical palettes
# ---------------------------------------------------------------------------

# NPG – Nature Publishing Group (ggsci)
_NPG = [
    "#E64B35", "#4DBBD5", "#00A087", "#3C5488",
    "#F39B7F", "#8491B4", "#91D1C2", "#DC0000",
    "#7E6148", "#B09C85",
]

# Okabe–Ito: rigorously colorblind-safe, widely used in Nature / Science
_OKABE_ITO = [
    "#E69F00", "#56B4E9", "#009E73", "#F0E442",
    "#0072B2", "#D55E00", "#CC79A7", "#999999",
]

# Paul Tol "Bright" – optimised for colorblind readers (≤ 7 categories)
_TOL_BRIGHT = [
    "#4477AA", "#EE6677", "#228833", "#CCBB44",
    "#66CCEE", "#AA3377", "#BBBBBB",
]

# Paul Tol "Muted" – softer, good for filled areas (≤ 10 categories)
_TOL_MUTED = [
    "#332288", "#88CCEE", "#44AA99", "#117733",
    "#999933", "#DDCC77", "#CC6677", "#882255",
    "#AA4499", "#DDDDDD",
]

# Flat pastels – subtle, nice for backgrounds or low-emphasis categories
_PASTEL = [
    "#AEC6CF", "#FFD1DC", "#B5EAD7", "#FFDAC1",
    "#C7CEEA", "#E2F0CB", "#F3E5F5", "#FFF9C4",
]

# Ersilia official brand palette (brand guidelines, ersilia.io)
# Ordered for maximum contrast between adjacent categories
_ERSILIA = [
    "#50285A",  # plum
    "#BEE6B4",  # mint
    "#AA96FA",  # purple
    "#FAA08C",  # orange
    "#8CC8FA",  # blue
    "#FAD782",  # yellow
    "#DCA0DC",  # pink
    "#D2D2D0",  # gray
]

_CATEGORICAL_PRESETS = {
    "ersilia":   _ERSILIA,
    "npg":       _NPG,
    "okabe":     _OKABE_ITO,
    "tol":       _TOL_BRIGHT,
    "tol_muted": _TOL_MUTED,
    "pastel":    _PASTEL,
}


class CategoricalPalette:
    """A cycling palette of distinct colors for categorical data.

    Presets
    -------
    ``npg``        Nature Publishing Group – 10 colors (default)
    ``ersilia``    Official Ersilia brand palette – 8 colors
    ``okabe``      Okabe–Ito, colorblind-safe – 8 colors
    ``tol``        Paul Tol Bright, colorblind-safe – 7 colors
    ``tol_muted``  Paul Tol Muted, colorblind-safe – 10 colors
    ``pastel``     Flat pastels – 8 colors

    Parameters
    ----------
    palette : str or list
        Preset name or an explicit list of hex/RGB colors.
    shuffle : bool
        Randomise color order on construction.

    Example
    -------
    >>> pal = CategoricalPalette("npg")
    >>> colors = pal.sample(5)
    >>> color  = pal.next()
    """

    def __init__(self, palette="npg", shuffle=False):
        if isinstance(palette, str):
            if palette not in _CATEGORICAL_PRESETS:
                raise ValueError(
                    f"Unknown palette '{palette}'. "
                    f"Choose from: {list(_CATEGORICAL_PRESETS)}"
                )
            raw = _CATEGORICAL_PRESETS[palette]
        else:
            raw = list(palette)

        self.colors = [_hex_to_rgb(c) if isinstance(c, str) else c for c in raw]
        if shuffle:
            random.shuffle(self.colors)
        self._cur = 0

    def next(self):
        color = self.colors[self._cur % len(self.colors)]
        self._cur += 1
        return color

    def sample(self, n):
        return [self.colors[i % len(self.colors)] for i in range(n)]

    def reset(self):
        self._cur = 0

    def __len__(self):
        return len(self.colors)

    def __iter__(self):
        return iter(self.colors)

    @staticmethod
    def available():
        return list(_CATEGORICAL_PRESETS)


# ---------------------------------------------------------------------------
# Colormap definitions — built from PaperColors tones
# ---------------------------------------------------------------------------
#
# Three colormap families, each with named presets derived from PaperColors:
#   ContinuousColormap  – sequential, pale → saturated
#   DivergingColormap   – two hues through a light center
#   CyclicColormap      – wraps smoothly back to start


def _make_cmap(colors, name):
    return mcolors.LinearSegmentedColormap.from_list(name, colors, N=256)


# Sequential: pale tint of the hue → full PaperColors saturation
_SEQUENTIAL_CMAPS = {
    "cobalt":  _make_cmap(["#E8EAF5", "#3C5488"], "cobalt"),   # pale blue → navy cobalt
    "crimson": _make_cmap(["#FDECEA", "#E64B35"], "crimson"),  # blush → vermillion
    "jade":    _make_cmap(["#E0F5F1", "#00A087"], "jade"),     # pale mint → deep jade
    "sky":     _make_cmap(["#E5F6FB", "#4DBBD5"], "sky"),      # near-white → sky teal
    "umber":   _make_cmap(["#F0EDE8", "#7E6148"], "umber"),    # warm cream → umber brown
}

# Diverging: two PaperColors hues through a near-white center
_DIVERGING_CMAPS = {
    "crimson_cobalt": _make_cmap(["#E64B35", "#F8F8F8", "#3C5488"], "crimson_cobalt"),  # warm red ↔ navy blue
    "coral_sky":      _make_cmap(["#F39B7F", "#FAFAFA", "#4DBBD5"], "coral_sky"),       # coral ↔ sky teal
    "umber_sky":      _make_cmap(["#7E6148", "#F5F2EF", "#4DBBD5"], "umber_sky"),       # warm brown ↔ cool sky
}

# Cyclic: cycles through PaperColors hues, ending where it started
_CYCLIC_CMAPS = {
    "paper": _make_cmap(
        ["#E64B35", "#8491B4", "#4DBBD5", "#00A087", "#F39B7F", "#E64B35"],
        "paper",
    ),  # crimson → periwinkle → sky → jade → coral → crimson
}


# ---------------------------------------------------------------------------
# Shared fit/transform base class
# ---------------------------------------------------------------------------

class _ColormapBase:
    _PRESETS = {}
    _DEFAULT = None

    def __init__(self, name=None, transformation="uniform", ascending=True):
        if name is None:
            name = self._DEFAULT
        if isinstance(name, str):
            if name not in self._PRESETS:
                raise ValueError(
                    f"Unknown colormap '{name}'. "
                    f"Available: {list(self._PRESETS)}"
                )
            self.cmap = self._PRESETS[name]
        else:
            self.cmap = name  # raw matplotlib colormap object
        self.transformation = transformation
        self.ascending = ascending

    @classmethod
    def available(cls):
        return list(cls._PRESETS)

    def fit(self, data):
        data = np.array(data)
        if not self.ascending:
            data = -data
        if self.transformation is not None:
            values = data.reshape(-1, 1)
            self.transformer = QuantileTransformer(
                n_quantiles=min(len(values), 1000),
                output_distribution=self.transformation,
            )
            self.transformer.fit(values)
            if self.transformation == "uniform":
                self.vmin, self.vmax = 0, 1
            else:
                values = self.transformer.transform(values).ravel()
                self.vmin = np.percentile(values, CONTINUOUS_CMAP_PERCENTILE_CUTS[0])
                self.vmax = np.percentile(values, CONTINUOUS_CMAP_PERCENTILE_CUTS[1])
        else:
            self.transformer = None
            self.vmin = np.percentile(data, CONTINUOUS_CMAP_PERCENTILE_CUTS[0])
            self.vmax = np.percentile(data, CONTINUOUS_CMAP_PERCENTILE_CUTS[1])
        self.color_normalizer = mpl.colors.Normalize(vmin=self.vmin, vmax=self.vmax)

    def transform(self, data):
        data = np.array(data)
        if not self.ascending:
            data = -data
        if self.transformer is not None:
            values = self.transformer.transform(data.reshape(-1, 1)).ravel()
        else:
            values = data
        return [self.cmap(self.color_normalizer(v)) for v in values]

    def get(self, data, alpha=None, lighten=None):
        result = self.transform(data)
        if lighten is not None:
            result = [lighten_color(c, factor=lighten) for c in result]
        if alpha is not None:
            result = [set_transparency(c, alpha) for c in result]
        return result

    def sample(self, n, shuffle=False):
        values = list(np.linspace(0, 1, n))
        if shuffle:
            random.shuffle(values)
        norm = mpl.colors.Normalize(vmin=0, vmax=1)
        return [self.cmap(norm(v)) for v in values]


# ---------------------------------------------------------------------------
# Public colormap classes
# ---------------------------------------------------------------------------

class ContinuousColormap(_ColormapBase):
    """Sequential colormap mapping low → high values in a single PaperColors hue.

    Presets
    -------
    ``cobalt``   pale blue → deep navy cobalt   (default)
    ``crimson``  blush → vermillion crimson
    ``jade``     pale mint → deep jade green
    ``sky``      near-white → bright sky teal
    ``umber``    warm cream → umber brown

    Parameters
    ----------
    name : str
        Preset name (see above).
    transformation : ``"uniform"`` | ``"normal"`` | ``None``
        Quantile-normalise data before mapping.
    ascending : bool
        If ``False``, reverse the mapping direction.

    Example
    -------
    >>> ccm = ContinuousColormap("cobalt")
    >>> ccm.fit(data)
    >>> colors = ccm.transform(data)
    """

    _PRESETS = _SEQUENTIAL_CMAPS
    _DEFAULT = "cobalt"

    def __init__(self, name="cobalt", transformation="uniform", ascending=True):
        super().__init__(name, transformation, ascending)


class DivergingColormap(_ColormapBase):
    """Diverging colormap with two PaperColors hues through a light center.

    Presets
    -------
    ``crimson_cobalt``  vermillion red ↔ navy blue through near-white   (default)
    ``coral_sky``       soft coral ↔ sky teal through near-white
    ``umber_sky``       warm brown ↔ sky teal through warm cream

    Parameters
    ----------
    name : str
        Preset name (see above).
    transformation : ``"uniform"`` | ``"normal"`` | ``None``
        Quantile-normalise data before mapping.
    ascending : bool
        If ``False``, reverse the mapping direction.

    Example
    -------
    >>> dcm = DivergingColormap("crimson_cobalt")
    >>> dcm.fit(data)
    >>> colors = dcm.transform(data)
    """

    _PRESETS = _DIVERGING_CMAPS
    _DEFAULT = "crimson_cobalt"

    def __init__(self, name="crimson_cobalt", transformation="uniform", ascending=True):
        super().__init__(name, transformation, ascending)


class CyclicColormap(_ColormapBase):
    """Cyclic colormap for phase or angle data, wrapping smoothly.

    Presets
    -------
    ``paper``   crimson → periwinkle → sky → jade → coral → crimson   (default)

    Parameters
    ----------
    name : str
        Preset name (see above).
    transformation : ``"uniform"`` | ``"normal"`` | ``None``
        Quantile-normalise data before mapping.
    ascending : bool
        If ``False``, reverse the mapping direction.

    Example
    -------
    >>> ccm = CyclicColormap()
    >>> ccm.fit(angles)
    >>> colors = ccm.transform(angles)
    """

    _PRESETS = _CYCLIC_CMAPS
    _DEFAULT = "paper"

    def __init__(self, name="paper", transformation="uniform", ascending=True):
        super().__init__(name, transformation, ascending)


# ---------------------------------------------------------------------------
# Backward-compat aliases
# ---------------------------------------------------------------------------
Palette = CategoricalPalette
CategoricalColorMap = CategoricalPalette
ContinuousColorMap = ContinuousColormap
NamedColorMaps = None  # removed; use ContinuousColormap/DivergingColormap/CyclicColormap
