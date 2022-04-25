import matplotlib as mpl
import seaborn as sns
import shutil

sns.set_style("ticks")

import matplotlib.font_manager

FONT = "Arial"


def is_font_available():
    flist = matplotlib.font_manager.get_fontconfig_fonts()
    names = [
        matplotlib.font_manager.FontProperties(fname=fname).get_name()
        for fname in flist
    ]
    if FONT not in names:
        return False
    else:
        return True


if not is_font_available():
    raise Exception(
        "{0} font is not available! Please install it in your system".format(FONT)
    )

shutil.rmtree(mpl.get_cachedir())

mpl.rcParams["font.family"] = "sans-serif"
mpl.rcParams["font.sans-serif"] = FONT
mpl.rcParams.update({"font.size": 10})
mpl.rcParams["pdf.fonttype"] = 42
mpl.rcParams["ps.fonttype"] = 42
mpl.rcParams.update({"axes.grid": True})

# Relative imports

from .figure import create_figure, save_figure
from .colors.colors import NamedColors
