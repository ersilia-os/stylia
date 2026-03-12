import os
import shutil
import matplotlib as mpl
import matplotlib.font_manager as _fm

os.environ["LC_CTYPE"] = "en_US.UTF-8"

shutil.rmtree(mpl.get_cachedir())

# Register bundled fonts (Arial, Ersilia) so they work even without system install
_fonts_dir = os.path.join(os.path.dirname(__file__), "fonts")
if os.path.isdir(_fonts_dir):
    for _f in os.listdir(_fonts_dir):
        if _f.endswith((".ttf", ".otf")):
            _fm.fontManager.addfont(os.path.join(_fonts_dir, _f))

mpl.rcParams["font.family"] = "sans-serif"
mpl.rcParams["font.sans-serif"] = "Arial"
mpl.rcParams["pdf.fonttype"] = 42
mpl.rcParams["ps.fonttype"] = 42
mpl.rcParams.update({
    "axes.grid": True,
    "axes.axisbelow": True,
    "figure.autolayout": True,
    "axes.spines.top": True,
    "axes.spines.right": True,
})

# Apply default format (print) + style (article) settings
from .config import _apply_settings, set_format, set_style, get_markersize, get_size
_apply_settings()

from .figure import create_figure, save_figure
from .figure.figure import label
from .colors.colors import ArticleColors, ErsiliaColors, CategoricalPalette
from .colors.colors import FadingColormap, SpectralColormap, DivergingColormap, CyclicColormap
from .colors.colors import ContinuousColormap, ContinuousColorMap  # backward compat
from .vars import *

# Remove static bindings for format-sensitive names so __getattr__ can
# resolve them dynamically whenever set_format() changes the active format.
import sys as _sys
for _n in (
    "SIZE",
    "FONTSIZE_SMALL", "FONTSIZE", "FONTSIZE_BIG",
    "MARKERSIZE_SMALL", "MARKERSIZE", "MARKERSIZE_BIG",
    "LINEWIDTH", "LINEWIDTH_THICK",
):
    try:
        delattr(_sys.modules[__name__], _n)
    except AttributeError:
        pass
del _sys, _n


def __getattr__(name):
    if name == "NamedColors":
        from .config import get_named_colors_class
        return get_named_colors_class()
    if name == "SIZE":
        from .config import get_size
        return get_size()
    if name in ("FONTSIZE_SMALL", "FONTSIZE", "FONTSIZE_BIG",
                "LINEWIDTH", "LINEWIDTH_THICK"):
        from .config import get_format
        from . import vars as _v
        prefix = "SLIDE_" if get_format() == "slide" else ""
        return getattr(_v, prefix + name)
    if name in ("MARKERSIZE_SMALL", "MARKERSIZE", "MARKERSIZE_BIG"):
        from .config import get_markersize
        tier = {"MARKERSIZE_SMALL": "small", "MARKERSIZE": "normal", "MARKERSIZE_BIG": "big"}[name]
        return get_markersize(tier)
    raise AttributeError(f"module 'stylia' has no attribute {name!r}")
