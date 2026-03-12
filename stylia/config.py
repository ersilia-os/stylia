"""
Global format and style configuration for stylia.

Usage
-----
    import stylia
    stylia.set_format("slide")   # or "print" (default)
    stylia.set_style("ersilia")  # or "article" (default)

Formats
-------
print  : SIZE = 7.09" (Nature two-column width). Default height ratio 0.5.
         Compact fonts and thin lines suited for print.
slide  : SIZE = 13" (wide slide width). Default height ratio 0.3.
         Slightly larger fonts and lines for screen presentation.

Styles
------
article : Publication color palette; all structural elements in black.
ersilia  : Ersilia brand palette; black elements replaced by plum (#50285A).
"""

import matplotlib as mpl
import numpy as np

# Ersilia primary color — replaces black in ersilia style
_PLUM = "#50285A"

# Categorical color lists (hex) — kept local to avoid circular imports
_ARTICLE_COLORS = [
    "#E63946", "#F4845F", "#FCBF49", "#6BBF59", "#2EC4B6",
    "#457B9D", "#6C5CE7", "#B05CC8", "#E91E8C", "#A0A0A0",
]

_ERSILIA_COLORS = [
    "#50285A", "#BEE6B4", "#AA96FA", "#FAA08C",
    "#8CC8FA", "#FAD782", "#DCA0DC", "#D2D2D0",
]

# ---------------------------------------------------------------------------
# Module-level state
# ---------------------------------------------------------------------------

_current_format = "print"
_current_style = "article"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def set_format(fmt):
    """Set the output format: ``'print'`` (default) or ``'slide'``."""
    global _current_format
    if fmt not in ("print", "slide"):
        raise ValueError("Format must be 'print' or 'slide'")
    _current_format = fmt
    _apply_settings()


def set_style(style):
    """Set the visual style: ``'article'`` (default) or ``'ersilia'``."""
    global _current_style
    if style not in ("article", "ersilia"):
        raise ValueError("Style must be 'article' or 'ersilia'")
    _current_style = style
    _apply_settings()


def get_format():
    """Return the current format string."""
    return _current_format


def get_style():
    """Return the current style string."""
    return _current_style


_PRINT_SIZE        = 7.09   # Nature two-column width, inches
_SLIDE_SIZE        = 13.0   # Wide slide width, inches
_PRINT_HEIGHT_RATIO = 0.5
_SLIDE_HEIGHT_RATIO = 0.3


def get_size():
    """Return SIZE for the current format (7.09 for print, 13 for slide)."""
    return _SLIDE_SIZE if _current_format == "slide" else _PRINT_SIZE


def get_default_height_ratio():
    """Return the default figure height as a fraction of SIZE."""
    return _SLIDE_HEIGHT_RATIO if _current_format == "slide" else _PRINT_HEIGHT_RATIO


def get_linewidth():
    """Return the thin linewidth for the current format."""
    from .vars import LINEWIDTH, SLIDE_LINEWIDTH
    return SLIDE_LINEWIDTH if _current_format == "slide" else LINEWIDTH


def get_named_colors_class():
    """Return ArticleColors for article style, ErsiliaColors for ersilia style."""
    from .colors.colors import ArticleColors, ErsiliaColors
    return ArticleColors if _current_style == "article" else ErsiliaColors


def get_fg_color():
    """Return the foreground color: plum for ersilia style, black for article."""
    return _PLUM if _current_style == "ersilia" else "black"


def get_color_cycle():
    """Return the color cycle as a list of hex strings for the current style."""
    return _ERSILIA_COLORS if _current_style == "ersilia" else _ARTICLE_COLORS


def get_fontsize_big():
    """Return the large font size used for panel labels (abc)."""
    from .vars import FONTSIZE_BIG, SLIDE_FONTSIZE_BIG
    return SLIDE_FONTSIZE_BIG if _current_format == "slide" else FONTSIZE_BIG


# ---------------------------------------------------------------------------
# Internal: apply all rcParams for current format + style
# ---------------------------------------------------------------------------

def get_markersize(size="normal"):
    """Return the marker size for the current format.

    Parameters
    ----------
    size : ``"small"`` | ``"normal"`` | ``"big"``
        Which size tier to return (for use as ``s=`` in scatter calls).
    """
    from .vars import (
        MARKERSIZE_SMALL, MARKERSIZE, MARKERSIZE_BIG,
        SLIDE_MARKERSIZE_SMALL, SLIDE_MARKERSIZE, SLIDE_MARKERSIZE_BIG,
    )
    if _current_format == "slide":
        return {"small": SLIDE_MARKERSIZE_SMALL, "normal": SLIDE_MARKERSIZE, "big": SLIDE_MARKERSIZE_BIG}[size]
    return {"small": MARKERSIZE_SMALL, "normal": MARKERSIZE, "big": MARKERSIZE_BIG}[size]


def _apply_settings():
    from .vars import (
        FONTSIZE_SMALL, FONTSIZE,
        SLIDE_FONTSIZE_SMALL, SLIDE_FONTSIZE,
        LINEWIDTH, SLIDE_LINEWIDTH,
        MARKERSIZE, SLIDE_MARKERSIZE,
    )

    if _current_format == "slide":
        fs_small = SLIDE_FONTSIZE_SMALL
        fs = SLIDE_FONTSIZE
        lw = SLIDE_LINEWIDTH
        ms = SLIDE_MARKERSIZE
    else:
        fs_small = FONTSIZE_SMALL
        fs = FONTSIZE
        lw = LINEWIDTH
        ms = MARKERSIZE

    fg = _PLUM if _current_style == "ersilia" else "black"
    cycle_hex = get_color_cycle()

    params = {
        # Font sizes
        "font.size":        fs_small,
        "axes.titlesize":   fs,
        "axes.labelsize":   fs,
        "xtick.labelsize":  fs,
        "ytick.labelsize":  fs,
        "legend.fontsize":  fs,
        "figure.titlesize": fs,
        # Line / marker / patch widths
        "axes.linewidth":   lw,
        "lines.linewidth":  lw,
        "lines.markersize": np.sqrt(ms),
        "patch.linewidth":  0,          # no border on bars/patches
        # Foreground colors
        "text.color":       fg,
        "axes.labelcolor":  fg,
        "xtick.color":      fg,
        "ytick.color":      fg,
        "axes.edgecolor":   fg,
        # Legend — framed with semi-transparent white background, top-right by default
        "legend.frameon":      True,
        "legend.facecolor":    "white",
        "legend.framealpha":   0.8,
        "legend.edgecolor":    "none",
        "legend.loc":          "upper right",
        # Color cycle
        "axes.prop_cycle":  mpl.cycler("color", cycle_hex),
    }

    # axes.titlecolor was added in matplotlib 3.2; guard against older versions
    if "axes.titlecolor" in mpl.rcParams:
        params["axes.titlecolor"] = fg

    mpl.rcParams.update(params)
