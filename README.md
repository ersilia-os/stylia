# Stylia: decent scientific plot styles

Stylia provides predefined [Matplotlib](https://matplotlib.org/) styles, color palettes, and figure utilities for producing publication-quality scientific figures. Designed for the [Ersilia Open Source Initiative](https://ersilia.io), but works for any scientific Python project.

![demo](assets/demo.png)

---

## Installation

```bash
pip install stylia
```

Or from source:

```bash
git clone https://github.com/ersilia-os/stylia.git
cd stylia
pip install -e .
```

Importing `stylia` automatically applies global Matplotlib style settings (font, grid, DPI-ready PDF output):

```python
import stylia
```

---

## Table of Contents

- [Format and style](#format-and-style)
- [Named colors](#named-colors)
- [Categorical palettes](#categorical-palettes)
- [Continuous colormaps](#continuous-colormaps)
- [Figures](#figures)
- [Sizes and constants](#sizes-and-constants)

---

## Format and style

Two orthogonal settings control the global appearance of all figures.

**Format** sets the size and density suited to the output medium:

```python
stylia.set_format("print")   # default — 7.09 in wide, compact fonts and thin lines
stylia.set_format("slide")   # 13 in wide, slightly larger fonts for screen
```

**Style** sets the color theme for structural elements (axes, ticks, text):

```python
stylia.set_style("article")  # default — all structural elements in black
stylia.set_style("ersilia")  # structural elements in Ersilia plum (#50285A)
```

Both settings update `matplotlib.rcParams` globally and can be changed at any point.

---

## Named colors

### PaperColors

NPG-derived palette with evocative names, suited for annotating specific plot elements in publications.

| | Name | Hex |
|---|---|---|
| ![](https://placehold.co/40x18/E64B35/E64B35.png) | `crimson` | `#E64B35` |
| ![](https://placehold.co/40x18/3C5488/3C5488.png) | `cobalt` | `#3C5488` |
| ![](https://placehold.co/40x18/4DBBD5/4DBBD5.png) | `sky` | `#4DBBD5` |
| ![](https://placehold.co/40x18/00A087/00A087.png) | `jade` | `#00A087` |
| ![](https://placehold.co/40x18/F39B7F/F39B7F.png) | `coral` | `#F39B7F` |
| ![](https://placehold.co/40x18/8491B4/8491B4.png) | `periwinkle` | `#8491B4` |
| ![](https://placehold.co/40x18/91D1C2/91D1C2.png) | `seafoam` | `#91D1C2` |
| ![](https://placehold.co/40x18/DC0000/DC0000.png) | `scarlet` | `#DC0000` |
| ![](https://placehold.co/40x18/7E6148/7E6148.png) | `umber` | `#7E6148` |
| ![](https://placehold.co/40x18/B09C85/B09C85.png) | `sand` | `#B09C85` |

```python
from stylia import PaperColors

nc = PaperColors()

nc.crimson     # #E64B35
nc.cobalt      # #3C5488
nc.sky         # #4DBBD5
nc.jade        # #00A087
nc.coral       # #F39B7F
nc.periwinkle  # #8491B4
nc.seafoam     # #91D1C2
nc.scarlet     # #DC0000
nc.umber       # #7E6148
nc.sand        # #B09C85
nc.white       # #FFFFFF
nc.black       # #2C3E50

# index or slice (palette order, excludes white/black)
nc[0]          # crimson
nc[-1]         # sand
nc[0:3]        # [crimson, cobalt, sky]
len(nc)        # 10
list(nc)       # all 10 as a list

# modifiers
nc.get("crimson", alpha=0.4)    # semi-transparent
nc.get("cobalt",  lighten=0.3)  # lightened

# all hex values
nc.hex   # {'crimson': '#E64B35', 'cobalt': '#3C5488', ...}
```

### ErsiliaColors

Official [Ersilia brand palette](https://ersilia.gitbook.io/ersilia-book/styles/brand-guidelines).

| | Name | Hex |
|---|---|---|
| ![](https://placehold.co/40x18/50285A/50285A.png) | `plum` | `#50285A` |
| ![](https://placehold.co/40x18/AA96FA/AA96FA.png) | `purple` | `#AA96FA` |
| ![](https://placehold.co/40x18/BEE6B4/BEE6B4.png) | `mint` | `#BEE6B4` |
| ![](https://placehold.co/40x18/8CC8FA/8CC8FA.png) | `blue` | `#8CC8FA` |
| ![](https://placehold.co/40x18/FAD782/FAD782.png) | `yellow` | `#FAD782` |
| ![](https://placehold.co/40x18/DCA0DC/DCA0DC.png) | `pink` | `#DCA0DC` |
| ![](https://placehold.co/40x18/FAA08C/FAA08C.png) | `orange` | `#FAA08C` |
| ![](https://placehold.co/40x18/D2D2D0/D2D2D0.png) | `gray` | `#D2D2D0` |

```python
from stylia import ErsiliaColors

ec = ErsiliaColors()

ec.plum    # #50285A – Ersilia primary
ec.purple  # #AA96FA – Ersilia accent
ec.mint    # #BEE6B4
ec.blue    # #8CC8FA
ec.yellow  # #FAD782
ec.pink    # #DCA0DC
ec.orange  # #FAA08C
ec.gray    # #D2D2D0
```

---

## Categorical palettes

`CategoricalPalette` cycles through a set of distinct colors for categorical data.

```python
from stylia import CategoricalPalette

pal = CategoricalPalette()             # default: npg
pal = CategoricalPalette("npg")
pal = CategoricalPalette("ersilia")
pal = CategoricalPalette("okabe")   # colorblind-safe
pal = CategoricalPalette("tol")     # colorblind-safe, ≤7
pal = CategoricalPalette("pastel")

# usage
colors = pal.sample(5)    # list of 5 RGB tuples
color  = pal.next()       # draw one (advances internal counter)
pal.reset()               # restart counter

# shuffle order on creation
pal = CategoricalPalette("npg", shuffle=True)

# custom list of hex colors
pal = CategoricalPalette(["#E64B35", "#4DBBD5", "#00A087"])

# list all presets
CategoricalPalette.available()
# ['npg', 'ersilia', 'okabe', 'tol', 'pastel']
```

**npg** — Nature Publishing Group

![](https://placehold.co/40x18/E64B35/E64B35.png) ![](https://placehold.co/40x18/4DBBD5/4DBBD5.png) ![](https://placehold.co/40x18/00A087/00A087.png) ![](https://placehold.co/40x18/3C5488/3C5488.png) ![](https://placehold.co/40x18/F39B7F/F39B7F.png) ![](https://placehold.co/40x18/8491B4/8491B4.png) ![](https://placehold.co/40x18/91D1C2/91D1C2.png) ![](https://placehold.co/40x18/DC0000/DC0000.png) ![](https://placehold.co/40x18/7E6148/7E6148.png) ![](https://placehold.co/40x18/B09C85/B09C85.png)

**ersilia** — Ersilia brand

![](https://placehold.co/40x18/50285A/50285A.png) ![](https://placehold.co/40x18/BEE6B4/BEE6B4.png) ![](https://placehold.co/40x18/AA96FA/AA96FA.png) ![](https://placehold.co/40x18/FAA08C/FAA08C.png) ![](https://placehold.co/40x18/8CC8FA/8CC8FA.png) ![](https://placehold.co/40x18/FAD782/FAD782.png) ![](https://placehold.co/40x18/DCA0DC/DCA0DC.png) ![](https://placehold.co/40x18/D2D2D0/D2D2D0.png)

**okabe** — Okabe–Ito (colorblind-safe)

![](https://placehold.co/40x18/E69F00/E69F00.png) ![](https://placehold.co/40x18/56B4E9/56B4E9.png) ![](https://placehold.co/40x18/009E73/009E73.png) ![](https://placehold.co/40x18/F0E442/F0E442.png) ![](https://placehold.co/40x18/0072B2/0072B2.png) ![](https://placehold.co/40x18/D55E00/D55E00.png) ![](https://placehold.co/40x18/CC79A7/CC79A7.png) ![](https://placehold.co/40x18/999999/999999.png)

**tol** — Paul Tol Bright (colorblind-safe)

![](https://placehold.co/40x18/4477AA/4477AA.png) ![](https://placehold.co/40x18/EE6677/EE6677.png) ![](https://placehold.co/40x18/228833/228833.png) ![](https://placehold.co/40x18/CCBB44/CCBB44.png) ![](https://placehold.co/40x18/66CCEE/66CCEE.png) ![](https://placehold.co/40x18/AA3377/AA3377.png) ![](https://placehold.co/40x18/BBBBBB/BBBBBB.png)

**pastel** — soft pastels

![](https://placehold.co/40x18/AEC6CF/AEC6CF.png) ![](https://placehold.co/40x18/FFD1DC/FFD1DC.png) ![](https://placehold.co/40x18/B5EAD7/B5EAD7.png) ![](https://placehold.co/40x18/FFDAC1/FFDAC1.png) ![](https://placehold.co/40x18/C7CEEA/C7CEEA.png) ![](https://placehold.co/40x18/E2F0CB/E2F0CB.png) ![](https://placehold.co/40x18/F3E5F5/F3E5F5.png) ![](https://placehold.co/40x18/FFF9C4/FFF9C4.png)

| Preset | Colors | Notes |
|---|---|---|
| `npg` | 10 | Nature Publishing Group standard |
| `ersilia` | 8 | Official Ersilia brand palette |
| `okabe` | 8 | Colorblind-safe (Okabe–Ito) |
| `tol` | 7 | Colorblind-safe (Paul Tol Bright) |
| `pastel` | 8 | Soft pastels for low-emphasis use |

---

## Continuous colormaps

Four colormap families, all built from PaperColors tones. Each supports the same `fit` / `transform` / `get` / `sample` interface.

### FadingColormap

Fades from near-white to a single PaperColors hue — good for density, intensity, or any strictly positive value.

| | Preset | Range |
|---|---|---|
| ![](https://placehold.co/20x18/E8EAF5/E8EAF5.png)![](https://placehold.co/20x18/9BA8C9/9BA8C9.png)![](https://placehold.co/20x18/3C5488/3C5488.png) | `cobalt` | pale blue → deep navy |
| ![](https://placehold.co/20x18/FDECEA/FDECEA.png)![](https://placehold.co/20x18/F29060/F29060.png)![](https://placehold.co/20x18/E64B35/E64B35.png) | `crimson` | blush → vermillion |
| ![](https://placehold.co/20x18/E0F5F1/E0F5F1.png)![](https://placehold.co/20x18/50C8B8/50C8B8.png)![](https://placehold.co/20x18/00A087/00A087.png) | `jade` | pale mint → deep jade |
| ![](https://placehold.co/20x18/E5F6FB/E5F6FB.png)![](https://placehold.co/20x18/79D5E5/79D5E5.png)![](https://placehold.co/20x18/4DBBD5/4DBBD5.png) | `sky` | near-white → sky teal |
| ![](https://placehold.co/20x18/F0EDE8/F0EDE8.png)![](https://placehold.co/20x18/B4A898/B4A898.png)![](https://placehold.co/20x18/7E6148/7E6148.png) | `umber` | warm cream → umber brown |

```python
from stylia import FadingColormap

ccm = FadingColormap()              # default: "cobalt"
ccm = FadingColormap("crimson")
ccm = FadingColormap("jade")
ccm = FadingColormap("sky")
ccm = FadingColormap("umber")
```

### SpectralColormap

Walks through multiple PaperColors hues warm → cool — good for ordered continuous data where the full range matters.

| | Preset | Range |
|---|---|---|
| ![](https://placehold.co/20x18/E64B35/E64B35.png)![](https://placehold.co/20x18/F39B7F/F39B7F.png)![](https://placehold.co/20x18/91D1C2/91D1C2.png)![](https://placehold.co/20x18/4DBBD5/4DBBD5.png)![](https://placehold.co/20x18/3C5488/3C5488.png) | `npg` | crimson → coral → seafoam → sky → cobalt |

```python
from stylia import SpectralColormap

scm = SpectralColormap()   # default: "npg"
```

### DivergingColormap

Two PaperColors hues through a light center — suited for data that diverges around a meaningful midpoint.

| | Preset | Range |
|---|---|---|
| ![](https://placehold.co/20x18/E64B35/E64B35.png)![](https://placehold.co/20x18/F8F8F8/F8F8F8.png)![](https://placehold.co/20x18/3C5488/3C5488.png) | `crimson_cobalt` | vermillion ↔ navy through near-white |
| ![](https://placehold.co/20x18/F39B7F/F39B7F.png)![](https://placehold.co/20x18/FAFAFA/FAFAFA.png)![](https://placehold.co/20x18/4DBBD5/4DBBD5.png) | `coral_sky` | coral ↔ sky teal through near-white |

```python
from stylia import DivergingColormap

dcm = DivergingColormap()                      # default: "crimson_cobalt"
dcm = DivergingColormap("coral_sky")
```

### CyclicColormap

Wraps smoothly back to its starting color — for phase, angle, or periodic data.

| | Preset | Cycle |
|---|---|---|
| ![](https://placehold.co/20x18/E64B35/E64B35.png)![](https://placehold.co/20x18/8491B4/8491B4.png)![](https://placehold.co/20x18/4DBBD5/4DBBD5.png)![](https://placehold.co/20x18/00A087/00A087.png)![](https://placehold.co/20x18/F39B7F/F39B7F.png) | `npg` | crimson → periwinkle → sky → jade → coral → crimson |

```python
from stylia import CyclicColormap

ccm = CyclicColormap()   # default: "npg"
```

### Fitting to data

All four classes share the same interface:

```python
import numpy as np
from stylia import FadingColormap, DivergingColormap

data = np.random.randn(200)

ccm = FadingColormap("cobalt")                             # uniform quantile (default)
ccm = FadingColormap("jade", transformation="normal")     # normal quantile
ccm = FadingColormap("sky",  transformation=None)         # raw percentile clip
dcm = DivergingColormap("crimson_cobalt", ascending=False)

ccm.fit(data)
colors   = ccm.transform(data)     # list of RGBA tuples, one per point
colors   = ccm.get(data, alpha=0.6)
swatches = ccm.sample(8)           # 8 evenly-spaced swatches
```

---

## Figures

### Creating a figure

`create_figure` returns a styled `(fig, axes)` pair with Stylia rcParams applied.

```python
from stylia import create_figure, save_figure

# single panel
fig, axes = create_figure()
ax = axes[0]

# multi-panel
fig, axes = create_figure(nrows=1, ncols=3)

# two-column width (7.09 in) instead of one-column (3.45 in)
fig, axes = create_figure(ncols=2, one_column=False)

# custom width ratios
fig, axes = create_figure(ncols=3, width_ratios=[2, 1, 1])
```

### Labels and styling

```python
from stylia.figure.axes import label, stylize

label(ax, xlabel="Time (h)", ylabel="OD600", title="Growth curve")
stylize(ax)   # removes top/right spines, tightens tick padding
```

### Saving

```python
save_figure(fig, "figure1.pdf")    # 600 DPI, tight layout, PDF-safe fonts
save_figure(fig, "figure1.png")
```

---

## Quick start

```python
import numpy as np
import stylia
from stylia import PaperColors, CategoricalPalette, ContinuousColormap
from stylia import create_figure, save_figure

nc  = PaperColors()
pal = CategoricalPalette()        # NPG by default

fig, axes = create_figure(nrows=1, ncols=3)

# scatter – single named color
ax = axes[0]
ax.scatter(np.random.randn(50), np.random.randn(50), color=nc.crimson)

# bar – categorical palette
ax = axes[1]
groups = ["A", "B", "C", "D", "E"]
values = np.random.rand(5)
ax.bar(groups, values, color=pal.sample(len(groups)))

# scatter – continuous colormap
ax = axes[2]
data = np.random.randn(200)
ccm  = ContinuousColormap("cobalt")
ccm.fit(data)
ax.scatter(range(len(data)), data, c=ccm.transform(data))

save_figure(fig, "quickstart.pdf")
```

---

## Sizes and constants

```python
from stylia import (
    FONTSIZE_SMALL,    # 5 pt
    FONTSIZE,          # 6 pt
    FONTSIZE_BIG,      # 8 pt
    MARKERSIZE_SMALL,  # 5
    MARKERSIZE,        # 10
    MARKERSIZE_BIG,    # 30
    LINEWIDTH,         # 0.5
    LINEWIDTH_THICK,   # 1
    ONE_COLUMN_WIDTH,  # 3.45 in
    TWO_COLUMNS_WIDTH, # 7.09 in
)
```

| Constant | Value | Use |
|---|---|---|
| `FONTSIZE_SMALL` | 5 pt | axis tick labels, annotations |
| `FONTSIZE` | 6 pt | axis labels, legend |
| `FONTSIZE_BIG` | 8 pt | panel titles |
| `MARKERSIZE_SMALL` | 5 | dense scatter |
| `MARKERSIZE` | 10 | standard scatter |
| `MARKERSIZE_BIG` | 30 | highlighted points |
| `LINEWIDTH` | 0.5 | standard lines, spines |
| `LINEWIDTH_THICK` | 1 | emphasis lines |
| `ONE_COLUMN_WIDTH` | 3.45 in | single-column journal figure |
| `TWO_COLUMNS_WIDTH` | 7.09 in | double-column journal figure |

---

## Disclaimer

Stylia is designed for internal use across Ersilia projects and is shared openly in case it is useful to others. It is not a general-purpose plotting library — for that, see [Matplotlib](https://matplotlib.org/) or [seaborn](https://seaborn.pydata.org/).

## About Us

Learn about the [Ersilia Open Source Initiative](https://ersilia.io)!
