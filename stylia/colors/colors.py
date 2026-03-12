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
    "crimson":    "#E63946",  # vivid red
    "tangerine":  "#F4845F",  # warm orange
    "amber":      "#FCBF49",  # golden yellow
    "lime":       "#6BBF59",  # fresh green
    "turquoise":  "#2EC4B6",  # teal-cyan
    "cobalt":     "#457B9D",  # steel blue
    "periwinkle": "#6C5CE7",  # blue-violet
    "orchid":     "#B05CC8",  # purple-pink
    "fuchsia":    "#E91E8C",  # hot magenta
    "silver":     "#A0A0A0",  # neutral gray
    # neutrals
    "white":      "#FFFFFF",
    "black":      "#2C3E50",  # soft off-black
}

_PAPER_ORDER = [
    "crimson", "tangerine", "amber", "lime", "turquoise",
    "cobalt", "periwinkle", "orchid", "fuchsia", "silver",
]


class ArticleColors:
    """Individual, semantically named colors for publication-quality figures.

    Colors are drawn from the NPG (Nature Publishing Group) palette and given
    evocative names suited for annotating specific plot elements.

    Example
    -------
    >>> nc = ArticleColors()
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
PaperColors = ArticleColors


# ---------------------------------------------------------------------------
# Categorical palettes
# ---------------------------------------------------------------------------

# NPG – redesigned for maximum hue coverage and perceptual distinctness
# Ordered around the hue wheel (red → orange → amber → green → teal →
# steel → periwinkle → orchid → fuchsia → neutral) so the sequence also
# works as a spectral colormap.
_NPG = [
    "#E63946",  # crimson    355°
    "#F4845F",  # tangerine   18°
    "#FCBF49",  # amber       42°
    "#6BBF59",  # lime       100°
    "#2EC4B6",  # turquoise  175°
    "#457B9D",  # cobalt     205°
    "#6C5CE7",  # periwinkle 255°
    "#B05CC8",  # orchid     280°
    "#E91E8C",  # fuchsia    325°
    "#A0A0A0",  # silver     neutral
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
    "ersilia": _ERSILIA,
    "npg":     _NPG,
    "okabe":   _OKABE_ITO,
    "tol":     _TOL_BRIGHT,
    "pastel":  _PASTEL,
}


class CategoricalPalette:
    """A cycling palette of distinct colors for categorical data.

    Presets
    -------
    ``npg``      Nature Publishing Group – 10 colors (default)
    ``ersilia``  Official Ersilia brand palette – 8 colors
    ``okabe``    Okabe–Ito, colorblind-safe – 8 colors
    ``tol``      Paul Tol Bright, colorblind-safe – 7 colors
    ``pastel``   Flat pastels – 8 colors

    Parameters
    ----------
    palette : str or list
        Preset name or an explicit list of hex/RGB colors.
    shuffle : bool
        Randomise color order on construction.

    Example
    -------
    >>> pal = CategoricalPalette("npg")
    >>> colors = pal.get(5)
    >>> color  = pal.next()
    """

    # Perceptual luminance weights for distance in RGB space
    _W = np.array([0.299, 0.587, 0.114])

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

    def get(self, n):
        """Return n maximally distinguishable colors.

        For n <= palette size: greedy farthest-point selection in perceptual
        RGB space — each successive pick maximises its minimum distance to all
        already-chosen colors.

        For n > palette size: the palette is treated as a continuous colormap
        and n evenly-spaced points are sampled from it, giving the original
        hues plus perceptually interpolated in-betweens.
        """
        if n <= len(self.colors):
            return self._greedy_farthest(n)
        return self._interpolated(n)

    def _greedy_farthest(self, n):
        pts = np.array(self.colors)  # shape (k, 3)
        selected = [0]
        for _ in range(n - 1):
            remaining = [i for i in range(len(pts)) if i not in selected]
            # distance of each candidate to its nearest already-selected color
            dists = [
                min(
                    np.sqrt(np.sum(self._W * (pts[i] - pts[j]) ** 2))
                    for j in selected
                )
                for i in remaining
            ]
            selected.append(remaining[int(np.argmax(dists))])
        return [self.colors[i] for i in selected]

    def _interpolated(self, n):
        cmap = mcolors.LinearSegmentedColormap.from_list("_pal", self.colors, N=256)
        return [cmap(v)[:3] for v in np.linspace(0, 1, n)]

    def next(self):
        color = self.colors[self._cur % len(self.colors)]
        self._cur += 1
        return color

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


# Sequential: near-white tint → full saturation of the hue
_SEQUENTIAL_CMAPS = {
    "crimson":    _make_cmap(["#FDECEA", "#E63946"], "crimson"),    # blush → vivid red
    "cobalt":     _make_cmap(["#E3ECF4", "#457B9D"], "cobalt"),     # pale sky → steel blue
    "turquoise":  _make_cmap(["#E0F8F7", "#2EC4B6"], "turquoise"),  # pale mint → teal-cyan
    "orchid":     _make_cmap(["#F5E8FA", "#B05CC8"], "orchid"),     # pale lavender → orchid
    "lime":       _make_cmap(["#EDF6E9", "#6BBF59"], "lime"),       # pale green → lime
}

# Diverging: two hues through a near-white center
_DIVERGING_CMAPS = {
    "crimson_cobalt":    _make_cmap(["#E63946", "#F8F8F8", "#457B9D"], "crimson_cobalt"),     # red ↔ steel blue
    "amber_periwinkle":  _make_cmap(["#FCBF49", "#FAFAFA", "#6C5CE7"], "amber_periwinkle"),   # amber ↔ blue-violet
}

# Spectral: walks warm → cool through the hue wheel, no wrap
_SPECTRAL_CMAPS = {
    "npg": _make_cmap(
        ["#E63946", "#FCBF49", "#2EC4B6", "#6C5CE7", "#E91E8C"],
        "npg_spectral",
    ),  # crimson → amber → turquoise → periwinkle → fuchsia
}

# Cyclic: evenly-spaced hues around the wheel, wraps back to start
_CYCLIC_CMAPS = {
    "npg": _make_cmap(
        ["#E63946", "#F4845F", "#6BBF59", "#2EC4B6", "#B05CC8", "#E63946"],
        "npg_cyclic",
    ),  # crimson → tangerine → lime → turquoise → orchid → crimson
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

class FadingColormap(_ColormapBase):
    """Sequential colormap fading from near-white to a single ArticleColors hue.

    Presets
    -------
    ``crimson``    blush → vivid red            (default)
    ``cobalt``     pale sky → steel blue
    ``turquoise``  pale mint → teal-cyan
    ``orchid``     pale lavender → purple-pink
    ``lime``       pale green → lime

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
    >>> ccm = FadingColormap("cobalt")
    >>> ccm.fit(data)
    >>> colors = ccm.transform(data)
    """

    _PRESETS = _SEQUENTIAL_CMAPS
    _DEFAULT = "cobalt"

    def __init__(self, name="crimson", transformation="uniform", ascending=True):
        super().__init__(name, transformation, ascending)


class SpectralColormap(_ColormapBase):
    """Multi-hue colormap walking through ArticleColors hues warm → cool.

    Presets
    -------
    ``npg``   crimson → amber → turquoise → periwinkle → fuchsia   (default)

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
    >>> scm = SpectralColormap()
    >>> scm.fit(data)
    >>> colors = scm.transform(data)
    """

    _PRESETS = _SPECTRAL_CMAPS
    _DEFAULT = "npg"

    def __init__(self, name="npg", transformation="uniform", ascending=True):
        super().__init__(name, transformation, ascending)


class DivergingColormap(_ColormapBase):
    """Diverging colormap with two ArticleColors hues through a light center.

    Presets
    -------
    ``crimson_cobalt``    vivid red ↔ steel blue through near-white   (default)
    ``amber_periwinkle``  warm amber ↔ blue-violet through near-white

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
    ``npg``   crimson → tangerine → lime → turquoise → orchid → crimson   (default)

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
    _DEFAULT = "npg"

    def __init__(self, name="npg", transformation="uniform", ascending=True):
        super().__init__(name, transformation, ascending)


# ---------------------------------------------------------------------------
# Backward-compat aliases
# ---------------------------------------------------------------------------
Palette = CategoricalPalette
CategoricalColorMap = CategoricalPalette
ContinuousColormap = FadingColormap   # renamed; old name kept as alias
ContinuousColorMap = FadingColormap
NamedColorMaps = None  # removed; use FadingColormap/DivergingColormap/CyclicColormap/SpectralColormap
