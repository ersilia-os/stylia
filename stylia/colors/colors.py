import random
import numpy as np

import matplotlib as mpl
from matplotlib import cm
from cmcrameri import cm as cms
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

_NAMED = {
    # Ersilia brand colors
    "plum":   "#50285A",  # Ersilia primary – deep plum purple
    "purple": "#AA96FA",  # Ersilia accent – soft lavender purple
    "mint":   "#BEE6B4",  # Ersilia mint green
    "blue":   "#8CC8FA",  # Ersilia sky blue
    "yellow": "#FAD782",  # Ersilia warm yellow
    "pink":   "#DCA0DC",  # Ersilia mauve pink
    "orange": "#FAA08C",  # Ersilia soft orange
    "gray":   "#D2D2D0",  # Ersilia light gray
    # NPG fill-ins (hues not present in Ersilia brand palette)
    "red":    "#E64B35",  # NPG vermillion-red
    "teal":   "#4DBBD5",  # NPG sky-teal
    "green":  "#00A087",  # NPG sea-green
    "brown":  "#7E6148",  # NPG warm brown
    # neutrals
    "white":  "#FFFFFF",
    "black":  "#2C3E50",  # soft off-black
}

_COLOR_ORDER = [
    "plum", "purple", "mint", "blue", "yellow",
    "pink", "orange", "gray", "red", "teal", "green", "brown",
]


class NamedColors:
    """Individual, semantically named colors for common plot elements.

    Colors are drawn from the NPG (Nature Publishing Group) palette and
    supplemented with clean modern neutrals.

    Example
    -------
    >>> nc = NamedColors()
    >>> ax.scatter(x, y, color=nc.red)
    >>> ax.scatter(x, y, color=nc.get("blue", alpha=0.6))
    """

    def __init__(self):
        for name, hex_val in _NAMED.items():
            setattr(self, name, _hex_to_rgb(hex_val))

    @property
    def hex(self):
        """Return all colors as a dict of hex strings."""
        return dict(_NAMED)

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
            return [getattr(self, name) for name in _COLOR_ORDER[idx]]
        return getattr(self, _COLOR_ORDER[idx])

    def __len__(self):
        return len(_COLOR_ORDER)

    def __iter__(self):
        """Yield colors in palette order (excludes white/black)."""
        for name in _COLOR_ORDER:
            yield getattr(self, name)


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
# Named colormaps (continuous)
# ---------------------------------------------------------------------------
#
# All colormaps are chosen so that every data value is visible on a white
# background.  The main failure mode of the old set (roma/vik/broc) was a
# near-white center on diverging maps, making zero-valued points invisible.
#
# Design principles applied here:
#   Sequential  – avoid pure-white endpoints; clip problematic cmaps.
#   Diverging   – use DARK-CENTER maps (center L ≈ 0.07–0.25) so mid-range
#                 values appear as dark/saturated colors, always visible.
#   Cyclic      – wrap smoothly with consistent mid-range lightness.


def _clip_cmap(cmap, lo=0.0, hi=1.0, name=None):
    """Return a new colormap that uses only the [lo, hi] fraction of *cmap*.

    Used to trim near-white endpoints from otherwise good sequential maps.
    """
    colors = [cmap(x) for x in np.linspace(lo, hi, 256)]
    return mcolors.LinearSegmentedColormap.from_list(
        name or getattr(cmap, "name", "cmap"), colors
    )


# Sequential – built once at import time so NamedColorMaps is cheap to
# instantiate.
#
#   viridis : imola         dark blue  → bright yellow-green  (L 0.40→0.70)
#   heat    : lajolla[0,78] near-black → orange-red           (L 0.05→0.62)
#             clipping removes the invisible cream-white end (#fffecb)
#   ocean   : oslo[0,72]    dark navy  → steel blue           (L 0.00→0.55)
#             clipping removes the invisible white end (#ffffff)
#   earth   : nuuk          cold blue  → warm yellow-green    (L 0.28→0.85)
#
_CMAP_VIRIDIS = cms.imola
_CMAP_HEAT    = _clip_cmap(cms.lajolla, 0.0, 0.78, "heat")
_CMAP_OCEAN   = _clip_cmap(cms.oslo,   0.0, 0.72, "ocean")
_CMAP_EARTH   = cms.nuuk

# Diverging – dark-center maps so mid-range (≈0) values are never invisible.
#
#   spectral : berlin    periwinkle-blue ↔ salmon-red through near-black
#              center L = 0.07 (was 0.84 with roma – nearly invisible!)
#   coolwarm : managua   golden-yellow   ↔ sky-cyan  through dark-purple
#              center L = 0.25 (was 0.90 with vik – nearly invisible!)
#
_CMAP_SPECTRAL = cms.berlin
_CMAP_COOLWARM = cms.managua

# Cyclic
_CMAP_CYCLIC = cms.romaO


_CMAP_NAMES = ["viridis", "heat", "ocean", "earth",
               "spectral", "coolwarm", "cyclic"]

_SCIENTIFIC_CMAPS_OBJ = {
    "viridis":  _CMAP_VIRIDIS,
    "heat":     _CMAP_HEAT,
    "ocean":    _CMAP_OCEAN,
    "earth":    _CMAP_EARTH,
    "spectral": _CMAP_SPECTRAL,
    "coolwarm": _CMAP_COOLWARM,
    "cyclic":   _CMAP_CYCLIC,
}

_STANDARD_CMAPS = {
    "viridis":  "viridis",
    "heat":     "hot",
    "ocean":    "Blues",
    "earth":    "YlGn",
    "spectral": "Spectral",
    "coolwarm": "coolwarm",
    "cyclic":   "hsv",
}


class NamedColorMaps:
    """Continuous colormaps accessible by semantic name.

    All colormaps are chosen so that **every data value is visible on a white
    background**.  In particular, diverging maps use a dark center (near-black)
    rather than the conventional white center, so mid-range values are never
    invisible.

    Parameters
    ----------
    scientific : bool
        Use perceptually-uniform cmcrameri colormaps (default ``True``).
        Set ``False`` for standard Matplotlib colormaps.

    Attributes
    ----------
    Sequential
        ``viridis``   dark blue → bright yellow-green  (cmcrameri: imola)
        ``heat``      near-black → orange-red           (cmcrameri: lajolla, clipped)
        ``ocean``     dark navy → steel blue            (cmcrameri: oslo, clipped)
        ``earth``     cold blue → warm yellow-green     (cmcrameri: nuuk)

    Diverging  *(dark-center — mid-range values are always visible)*
        ``spectral``  periwinkle-blue ↔ salmon-red, center ≈ black  (cmcrameri: berlin)
        ``coolwarm``  golden-yellow ↔ sky-cyan, center ≈ dark purple (cmcrameri: managua)

    Cyclic
        ``cyclic``    smooth wrap for phase / angle data  (cmcrameri: romaO)

    Example
    -------
    >>> ncm = NamedColorMaps()
    >>> ax.scatter(x, y, c=values, cmap=ncm.spectral)
    >>> ax.scatter(x, y, c=values, cmap=ncm.get("coolwarm"))
    """

    def __init__(self, scientific=True):
        self._scientific = scientific
        if scientific:
            for name, cmap in _SCIENTIFIC_CMAPS_OBJ.items():
                setattr(self, name, cmap)
        else:
            for name, cmap_id in _STANDARD_CMAPS.items():
                setattr(self, name, cm.get_cmap(cmap_id))

        # legacy aliases
        self.imola = self.viridis
        self.roma  = self.spectral
        self.vik   = self.coolwarm

    def get(self, name):
        if not hasattr(self, name):
            raise ValueError(
                f"Unknown colormap '{name}'. Available: {self.available}"
            )
        return getattr(self, name)

    @property
    def available(self):
        return list(_CMAP_NAMES)


# ---------------------------------------------------------------------------
# Continuous colormap (fit/transform over data)
# ---------------------------------------------------------------------------

class ContinuousColorMap:
    """Map a data array to colors using a continuous colormap.

    Parameters
    ----------
    cmap : str or colormap
        Named colormap (see ``NamedColorMaps``) or a raw matplotlib colormap.
    transformation : ``"uniform"`` | ``"normal"`` | ``None``
        Quantile-normalise data before mapping.
    ascending : bool
        If ``False``, reverse the mapping direction.

    Example
    -------
    >>> ccm = ContinuousColorMap("spectral")
    >>> ccm.fit(data)
    >>> colors = ccm.transform(data)
    """

    def __init__(self, cmap="spectral", transformation="uniform", ascending=True):
        if isinstance(cmap, str):
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
# Backward-compat aliases
# ---------------------------------------------------------------------------
Palette = CategoricalPalette
CategoricalColorMap = CategoricalPalette
