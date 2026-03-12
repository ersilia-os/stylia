from ..config import get_linewidth, get_fg_color, get_color_cycle, get_fontsize_big


def stylize(ax):
    lw = get_linewidth()
    fg = get_fg_color()

    ax.set_prop_cycle("color", get_color_cycle())
    ax.set_xlabel("X-axis / Units")
    ax.set_ylabel("Y-axis / Units")
    ax.set_title("Plot title")

    # Light grid so it doesn't compete with data
    try:
        ax.grid(visible=True, linewidth=lw, color="#DDDDDD", alpha=0.8)
    except TypeError:
        ax.grid(b=True, linewidth=lw, color="#DDDDDD", alpha=0.8)

    # Full frame with style-aware color
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(lw)
        spine.set_color(fg)

    ax.xaxis.set_tick_params(width=lw, colors=fg)
    ax.yaxis.set_tick_params(width=lw, colors=fg)
    return ax


def label(ax, xlabel=None, ylabel=None, title=None, abc=None):
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)
    if title is not None:
        ax.set_title(title)
    if abc is not None:
        ax.set_title(abc, loc="left", fontweight="bold", fontsize=get_fontsize_big())


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
