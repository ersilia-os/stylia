import matplotlib.pyplot as plt
from .figure import AxisManager
from ..config import get_size, get_default_height_ratio


def create_figure(
    nrows=1,
    ncols=1,
    height=None,
    width=None,
    width_ratios=None,
    height_ratios=None,
):
    """Create a styled matplotlib figure.

    Parameters
    ----------
    nrows, ncols : int
        Number of subplot rows and columns.
    width : float, optional
        Figure width as a fraction of SIZE (default 1.0 = full SIZE).
    height : float, optional
        Figure height as a fraction of SIZE.  Defaults to the format's
        height ratio (0.3 for slide, 0.5 for paper).
    width_ratios, height_ratios : list, optional
        Relative sizes of subplot columns / rows (passed to gridspec).

    Returns
    -------
    fig : matplotlib.figure.Figure
    axs : AxisManager
    """
    size = get_size()
    if width is None:
        width = 1.0
    if height is None:
        height = get_default_height_ratio()

    width_inches = width * size
    height_inches = height * size

    fig, axs = plt.subplots(
        nrows=nrows,
        ncols=ncols,
        figsize=(width_inches, height_inches),
        gridspec_kw={"width_ratios": width_ratios, "height_ratios": height_ratios},
    )
    fig.patch.set_facecolor("white")
    if nrows == 1 and ncols == 1:
        axs = [[axs]]
    return fig, AxisManager(axs)


def save_figure(filename, pad=None):
    if pad is None:
        plt.tight_layout()
    else:
        plt.tight_layout()
    plt.savefig(filename, dpi=600, transparent=False, bbox_inches="tight")
