import os
import shutil
import matplotlib as mpl
import matplotlib.font_manager  # noqa: F401 — side-effect: registers fonts

os.environ["LC_CTYPE"] = "en_US.UTF-8"

shutil.rmtree(mpl.get_cachedir())

mpl.rcParams["font.family"] = "sans-serif"
mpl.rcParams["font.sans-serif"] = "Arial"
mpl.rcParams["pdf.fonttype"] = 42
mpl.rcParams["ps.fonttype"] = 42
mpl.rcParams.update({
    "axes.grid": True,
    "figure.autolayout": True,
    "axes.spines.top": True,
    "axes.spines.right": True,
})

# Apply default format (print) + style (article) settings
from .config import _apply_settings, set_format, set_style, get_markersize, get_size
_apply_settings()

from .figure import create_figure, save_figure
from .figure.figure import label
from .colors.colors import ArticleColors, PaperColors, ErsiliaColors, CategoricalPalette
from .colors.colors import FadingColormap, SpectralColormap, DivergingColormap, CyclicColormap
from .colors.colors import ContinuousColormap, ContinuousColorMap  # backward compat
from .vars import *


def __getattr__(name):
    if name == "NamedColors":
        from .config import get_named_colors_class
        return get_named_colors_class()
    raise AttributeError(f"module 'stylia' has no attribute {name!r}")
