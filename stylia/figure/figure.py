from ..colors.colors import Palette
from ..vars import LINEWIDTH, FONTSIZE_BIG


def stylize(ax):
    ax.set_prop_cycle("color", Palette().colors)
    ax.set_xlabel("X-axis / Units")
    ax.set_ylabel("Y-axis / Units")
    ax.set_title("Plot title")
    try:
        ax.grid(b=True, linewidth=LINEWIDTH)
    except:
        ax.grid(visible=True, linewidth=LINEWIDTH)
    ax.xaxis.set_tick_params(width=LINEWIDTH)
    ax.yaxis.set_tick_params(width=LINEWIDTH)
    return ax


def label(ax, xlabel=None, ylabel=None, title=None, abc=None):
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if xlabel is not None:
        ax.set_ylabel(ylabel)
    if title is not None:
        ax.set_title(title)
    if abc is not None:
        ax.set_title(abc, loc="left", fontweight="bold", fontsize=FONTSIZE_BIG)


class AxisManager(object):
    def __init__(self, axs):
        if type(axs) is list:
            self.axs_flat = axs[0]
        else:
            self.axs_flat = axs.flatten()
        self.axs = axs
        self.current_i = 0

    def __getitem__(self, key):
        if type(key) is int:
            i = key
            ax = self.axs_flat[i]
            self.current_i = i + 1
        else:
            i, j = key
            ax = self.axs[i, j]
            self.current_i = j * (i + 1) + 1
        ax = stylize(ax)
        return ax

    def restart(self):
        self.current_i = 0

    def next(self):
        ax = self.axs_flat[self.current_i]
        self.current_i += 1
        ax = stylize(ax)
        return ax
