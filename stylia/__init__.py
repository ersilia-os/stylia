import matplotlib as mpl
import seaborn as sns
import shutil
import os

sns.set_style("ticks", {"axes.spines.top": True, "axes.spines.right": True})

os.environ["LC_CTYPE"] = "en_US.UTF-8"
import matplotlib.font_manager

FONT = "Arial"

shutil.rmtree(mpl.get_cachedir())

mpl.rcParams["font.family"] = "sans-serif"
mpl.rcParams["font.sans-serif"] = FONT
mpl.rcParams["pdf.fonttype"] = 42
mpl.rcParams["ps.fonttype"] = 42
mpl.rcParams.update({"axes.grid": True})

# Apply default format (paper) + style (article) settings
from .config import _apply_settings, set_format, set_style, get_markersize
_apply_settings()

# Relative imports

from .figure import create_figure, save_figure
from .figure.figure import label
from .colors.colors import ArticleColors, PaperColors, ErsiliaColors, CategoricalPalette
from .colors.colors import FadingColormap, SpectralColormap, DivergingColormap, CyclicColormap
from .colors.colors import ContinuousColormap, ContinuousColorMap  # backward compat


def __getattr__(name):
    if name == "NamedColors":
        from .config import get_named_colors_class
        return get_named_colors_class()
    raise AttributeError(f"module 'stylia' has no attribute {name!r}")
from .vars import *
