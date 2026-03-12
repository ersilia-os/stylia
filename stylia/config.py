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
    "#E64B35", "#4DBBD5", "#00A087", "#3C5488",
    "#F39B7F", "#8491B4", "#91D1C2", "#DC0000",
    "#7E6148", "#B09C85",
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


def get_size():
    """Return the current SIZE in inches (width basis for relative figure dims)."""
    from .vars import SIZE, WIDE_SLIDE_WIDTH
    return WIDE_SLIDE_WIDTH if _current_format == "slide" else SIZE


def get_default_height_ratio():
    """Return the default figure height as a fraction of SIZE."""
    from .vars import PAPER_HEIGHT_RATIO, SLIDE_HEIGHT_RATIO
    return SLIDE_HEIGHT_RATIO if _current_format == "slide" else PAPER_HEIGHT_RATIO


def get_linewidth():
    """Return the thin linewidth for the current format."""
    from .vars import LINEWIDTH, SLIDE_LINEWIDTH
    return SLIDE_LINEWIDTH if _current_format == "slide" else LINEWIDTH


def get_named_colors_class():
    """Return PaperColors for article style, ErsiliaColors for ersilia style."""
    from .colors.colors import PaperColors, ErsiliaColors
    return PaperColors if _current_style == "article" else ErsiliaColors


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

def _apply_settings():
    from .vars import (
        FONTSIZE_SMALL, FONTSIZE,
        SLIDE_FONTSIZE_SMALL, SLIDE_FONTSIZE,
        LINEWIDTH, SLIDE_LINEWIDTH,
        MARKERSIZE,
    )

    if _current_format == "slide":
        fs_small = SLIDE_FONTSIZE_SMALL
        fs = SLIDE_FONTSIZE
        lw = SLIDE_LINEWIDTH
    else:
        fs_small = FONTSIZE_SMALL
        fs = FONTSIZE
        lw = LINEWIDTH

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
        # Line / marker widths
        "axes.linewidth":   lw,
        "lines.linewidth":  lw,
        "lines.markersize": np.sqrt(MARKERSIZE),
        # Foreground colors
        "text.color":       fg,
        "axes.labelcolor":  fg,
        "xtick.color":      fg,
        "ytick.color":      fg,
        "axes.edgecolor":   fg,
        "legend.edgecolor": fg,
        # Color cycle
        "axes.prop_cycle":  mpl.cycler("color", cycle_hex),
    }

    # axes.titlecolor was added in matplotlib 3.2; guard against older versions
    if "axes.titlecolor" in mpl.rcParams:
        params["axes.titlecolor"] = fg

    mpl.rcParams.update(params)
