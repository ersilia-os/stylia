import matplotlib.pyplot as plt
from .figure import FigureSize, AxisManager


def create_figure(
    nrows=1,
    ncols=1,
    support="slide",
    page_columns=2,
    area_proportion=1,
    aspect_ratio=None,
):
    if aspect_ratio is None:
        aspect_ratio = (ncols, nrows)
    figsize = FigureSize(
        support=support,
        page_columns=page_columns,
        area_proportion=area_proportion,
        aspect_ratio=aspect_ratio,
    )
    fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize.size())
    fig.patch.set_facecolor("white")
    if nrows == 1 and ncols == 1:
        axs = [[axs]]
    else:
        axs = axs
    return fig, AxisManager(axs)


def save_figure(filename):
    plt.tight_layout()
    plt.savefig(filename, dpi=600, transparent=False)
