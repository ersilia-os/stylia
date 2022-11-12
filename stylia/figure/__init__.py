import matplotlib.pyplot as plt
from .figure import AxisManager

from ..vars import ONE_COLUMN_WIDTH, TWO_COLUMNS_WIDTH


def create_figure(
    nrows=1, ncols=1, height=None, width=None, width_ratios=None, height_ratios=None,
):
    if height is None:
        height = ONE_COLUMN_WIDTH
    if width is None:
        if ncols == 1:
            width = ONE_COLUMN_WIDTH
        else:
            width = TWO_COLUMNS_WIDTH
    fig, axs = plt.subplots(
        nrows=nrows,
        ncols=ncols,
        figsize=(width, height),
        gridspec_kw={"width_ratios": width_ratios, "height_ratios": height_ratios},
    )
    fig.patch.set_facecolor("white")
    if nrows == 1 and ncols == 1:
        axs = [[axs]]
    else:
        axs = axs
    return fig, AxisManager(axs)


def save_figure(filename, pad=None):
    if pad is None:
        plt.tight_layout()
    else:
        plt.tight_layout()
    plt.savefig(filename, dpi=600, transparent=False, bbox_inches="tight")
