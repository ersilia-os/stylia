# Stylia: decent scientific plot styles

Stylia provides predefined [Matplotlib](https://matplotlib.org/) styles, color palettes, and figure utilities for producing publication-quality scientific figures. Designed for the [Ersilia Open Source Initiative](https://ersilia.io), but works for any scientific Python project.

![demo](assets/demo.png)

---

## Installation

```bash
pip install stylia
```

Importing `stylia` automatically applies global Matplotlib style settings:

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

```python
stylia.set_format("print")   # default — compact, 7.09 in wide
stylia.set_format("slide")   # larger fonts and markers, 13 in wide

stylia.set_style("article")  # default — structural elements in black
stylia.set_style("ersilia")  # structural elements in Ersilia plum
```

Both update `matplotlib.rcParams` globally and can be changed at any point.

---

## Named colors

### ArticleColors

NPG-derived palette. Also aliased as `PaperColors`.

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
from stylia import ArticleColors

nc = ArticleColors()
ax.scatter(x, y, color=nc.crimson)
ax.scatter(x, y, color=nc.get("cobalt", alpha=0.4))
ax.scatter(x, y, color=nc.get("jade", lighten=0.3))
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

### NamedColors (style-aware)

`NamedColors` resolves to `ArticleColors` or `ErsiliaColors` based on the active style:

```python
nc = stylia.NamedColors()   # ArticleColors or ErsiliaColors depending on set_style()
```

---

## Categorical palettes

```python
from stylia import CategoricalPalette

pal = CategoricalPalette()              # default: npg
pal = CategoricalPalette("ersilia")
pal = CategoricalPalette("okabe")       # colorblind-safe
pal = CategoricalPalette("tol")         # colorblind-safe, ≤7
pal = CategoricalPalette("pastel")

colors = pal.get(5)     # 5 maximally distinguishable colors
colors = pal.get(20)    # >palette size: interpolated as a colormap
color  = pal.next()     # draw one (advances internal counter)
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

---

## Continuous colormaps

Four families, all built from ArticleColors tones. All share `fit(data)` / `transform(data)` / `get(data, alpha=)` / `sample(n)`.

### FadingColormap

Near-white → single hue. Good for density or strictly positive data.

| | Preset | Range |
|---|---|---|
| ![](https://placehold.co/20x18/E8EAF5/E8EAF5.png)![](https://placehold.co/20x18/9BA8C9/9BA8C9.png)![](https://placehold.co/20x18/3C5488/3C5488.png) | `cobalt` | pale blue → deep navy |
| ![](https://placehold.co/20x18/FDECEA/FDECEA.png)![](https://placehold.co/20x18/F29060/F29060.png)![](https://placehold.co/20x18/E64B35/E64B35.png) | `crimson` | blush → vermillion |
| ![](https://placehold.co/20x18/E0F5F1/E0F5F1.png)![](https://placehold.co/20x18/50C8B8/50C8B8.png)![](https://placehold.co/20x18/00A087/00A087.png) | `jade` | pale mint → deep jade |
| ![](https://placehold.co/20x18/E5F6FB/E5F6FB.png)![](https://placehold.co/20x18/79D5E5/79D5E5.png)![](https://placehold.co/20x18/4DBBD5/4DBBD5.png) | `sky` | near-white → sky teal |
| ![](https://placehold.co/20x18/F0EDE8/F0EDE8.png)![](https://placehold.co/20x18/B4A898/B4A898.png)![](https://placehold.co/20x18/7E6148/7E6148.png) | `umber` | warm cream → umber brown |

### SpectralColormap

Multi-hue warm → cool. Good for ordered data where the full range matters.

| | Preset | Range |
|---|---|---|
| ![](https://placehold.co/20x18/E64B35/E64B35.png)![](https://placehold.co/20x18/F39B7F/F39B7F.png)![](https://placehold.co/20x18/91D1C2/91D1C2.png)![](https://placehold.co/20x18/4DBBD5/4DBBD5.png)![](https://placehold.co/20x18/3C5488/3C5488.png) | `npg` | crimson → coral → seafoam → sky → cobalt |

### DivergingColormap

Two hues through a light center. Good for data diverging around a meaningful midpoint.

| | Preset | Range |
|---|---|---|
| ![](https://placehold.co/20x18/E64B35/E64B35.png)![](https://placehold.co/20x18/F8F8F8/F8F8F8.png)![](https://placehold.co/20x18/3C5488/3C5488.png) | `crimson_cobalt` | vermillion ↔ navy |
| ![](https://placehold.co/20x18/F39B7F/F39B7F.png)![](https://placehold.co/20x18/FAFAFA/FAFAFA.png)![](https://placehold.co/20x18/4DBBD5/4DBBD5.png) | `coral_sky` | coral ↔ sky teal |

### CyclicColormap

Wraps back to its starting color. Good for phase or angle data.

| | Preset | Cycle |
|---|---|---|
| ![](https://placehold.co/20x18/E64B35/E64B35.png)![](https://placehold.co/20x18/8491B4/8491B4.png)![](https://placehold.co/20x18/4DBBD5/4DBBD5.png)![](https://placehold.co/20x18/00A087/00A087.png)![](https://placehold.co/20x18/F39B7F/F39B7F.png) | `npg` | crimson → periwinkle → sky → jade → coral → crimson |

### Usage

```python
from stylia import FadingColormap, DivergingColormap

ccm = FadingColormap("cobalt")
ccm.fit(data)
colors = ccm.transform(data)        # list of RGBA tuples
colors = ccm.get(data, alpha=0.6)   # with alpha modifier
swatches = ccm.sample(8)            # 8 evenly-spaced swatches

dcm = DivergingColormap("crimson_cobalt", ascending=False)
dcm.fit(data)
colors = dcm.transform(data)
```

---

## Figures

```python
import stylia

stylia.set_format("print")
stylia.set_style("article")

fig, axs = stylia.create_figure(2, 1, width=0.8, height=0.3)

ax = axs.next()
ax.scatter(x, y, color=nc.crimson, s=stylia.get_markersize())

ax = axs.next()
ax.bar(groups, values, color=pal.get(len(groups)))

stylia.save_figure("figure.pdf")
```

`create_figure` accepts `width` and `height` as fractions of the format's base size. `axs.next()` steps through panels in order.

---

## Sizes and constants

All parameters have `print` and `slide` variants applied automatically by `set_format()`.

| Constant | print | slide | Use |
|---|---|---|---|
| `FONTSIZE_SMALL` / `SLIDE_FONTSIZE_SMALL` | 5 pt | 8 pt | tick labels, annotations |
| `FONTSIZE` / `SLIDE_FONTSIZE` | 6 pt | 10 pt | axis labels, legend |
| `FONTSIZE_BIG` / `SLIDE_FONTSIZE_BIG` | 8 pt | 13 pt | panel titles |
| `MARKERSIZE_SMALL` / `SLIDE_MARKERSIZE_SMALL` | 5 | 8 | dense scatter (`s=`) |
| `MARKERSIZE` / `SLIDE_MARKERSIZE` | 10 | 15 | standard scatter (`s=`) |
| `MARKERSIZE_BIG` / `SLIDE_MARKERSIZE_BIG` | 30 | 45 | highlighted points (`s=`) |
| `LINEWIDTH` / `SLIDE_LINEWIDTH` | 0.5 | 0.75 | lines, spines |
| `LINEWIDTH_THICK` / `SLIDE_LINEWIDTH_THICK` | 1 | 1.5 | emphasis lines |
| `ONE_COLUMN_WIDTH` | 3.45 in | — | single-column journal figure |
| `TWO_COLUMNS_WIDTH` | 7.09 in | — | double-column journal figure |

Use `stylia.get_markersize()` to get the format-aware value at runtime (`"small"`, `"normal"`, or `"big"`).

---

## Disclaimer

Stylia is designed for internal use across Ersilia projects and is shared openly in case it is useful to others. It is not a general-purpose plotting library — for that, see [Matplotlib](https://matplotlib.org/) or [seaborn](https://seaborn.pydata.org/).

## About Us

Learn about the [Ersilia Open Source Initiative](https://ersilia.io)!
