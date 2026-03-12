# Stylia: decent scientific plot styles

Stylia provides predefined [Matplotlib](https://matplotlib.org/) styles, color palettes, and figure utilities for producing publication-quality scientific figures. Designed for the [Ersilia Open Source Initiative](https://ersilia.io), but works for any scientific Python project.

**Article style** (default — NPG palette, black structural elements)

![article style demo](assets/demo_article.png)

**Ersilia style** (Ersilia brand palette, plum structural elements)

![ersilia style demo](assets/demo_ersilia.png)

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

Modern palette spanning the full hue wheel for maximum distinctness. Also aliased as `PaperColors`.

| | Name | Hex |
|---|---|---|
| ![](https://placehold.co/40x18/E63946/E63946.png) | `crimson` | `#E63946` |
| ![](https://placehold.co/40x18/F4845F/F4845F.png) | `tangerine` | `#F4845F` |
| ![](https://placehold.co/40x18/FCBF49/FCBF49.png) | `amber` | `#FCBF49` |
| ![](https://placehold.co/40x18/6BBF59/6BBF59.png) | `lime` | `#6BBF59` |
| ![](https://placehold.co/40x18/2EC4B6/2EC4B6.png) | `turquoise` | `#2EC4B6` |
| ![](https://placehold.co/40x18/457B9D/457B9D.png) | `cobalt` | `#457B9D` |
| ![](https://placehold.co/40x18/6C5CE7/6C5CE7.png) | `periwinkle` | `#6C5CE7` |
| ![](https://placehold.co/40x18/B05CC8/B05CC8.png) | `orchid` | `#B05CC8` |
| ![](https://placehold.co/40x18/E91E8C/E91E8C.png) | `fuchsia` | `#E91E8C` |
| ![](https://placehold.co/40x18/A0A0A0/A0A0A0.png) | `silver` | `#A0A0A0` |

```python
from stylia import ArticleColors

nc = ArticleColors()
ax.scatter(x, y, color=nc.crimson)
ax.scatter(x, y, color=nc.get("cobalt", alpha=0.4))
ax.scatter(x, y, color=nc.get("turquoise", lighten=0.3))
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

**npg** — redesigned for maximum hue coverage

![](https://placehold.co/40x18/E63946/E63946.png) ![](https://placehold.co/40x18/F4845F/F4845F.png) ![](https://placehold.co/40x18/FCBF49/FCBF49.png) ![](https://placehold.co/40x18/6BBF59/6BBF59.png) ![](https://placehold.co/40x18/2EC4B6/2EC4B6.png) ![](https://placehold.co/40x18/457B9D/457B9D.png) ![](https://placehold.co/40x18/6C5CE7/6C5CE7.png) ![](https://placehold.co/40x18/B05CC8/B05CC8.png) ![](https://placehold.co/40x18/E91E8C/E91E8C.png) ![](https://placehold.co/40x18/A0A0A0/A0A0A0.png)

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

Four families, all built from ArticleColors tones. All share `fit(data)` / `transform(data, alpha=, lighten=)` / `sample(n)`.

### FadingColormap

Near-white → single hue. Good for density or strictly positive data.

| | Preset | Range |
|---|---|---|
| ![](https://placehold.co/20x18/FDECEA/FDECEA.png)![](https://placehold.co/20x18/F08090/F08090.png)![](https://placehold.co/20x18/E63946/E63946.png) | `crimson` | blush → vivid red (default) |
| ![](https://placehold.co/20x18/E3ECF4/E3ECF4.png)![](https://placehold.co/20x18/8BAFC6/8BAFC6.png)![](https://placehold.co/20x18/457B9D/457B9D.png) | `cobalt` | pale sky → steel blue |
| ![](https://placehold.co/20x18/E0F8F7/E0F8F7.png)![](https://placehold.co/20x18/87DCD6/87DCD6.png)![](https://placehold.co/20x18/2EC4B6/2EC4B6.png) | `turquoise` | pale mint → teal-cyan |
| ![](https://placehold.co/20x18/F5E8FA/F5E8FA.png)![](https://placehold.co/20x18/D2A8E1/D2A8E1.png)![](https://placehold.co/20x18/B05CC8/B05CC8.png) | `orchid` | pale lavender → orchid |
| ![](https://placehold.co/20x18/EDF6E9/EDF6E9.png)![](https://placehold.co/20x18/ADDA9C/ADDA9C.png)![](https://placehold.co/20x18/6BBF59/6BBF59.png) | `lime` | pale green → lime |

### SpectralColormap

Multi-hue warm → cool. Good for ordered data where the full range matters.

| | Preset | Range |
|---|---|---|
| ![](https://placehold.co/20x18/E63946/E63946.png)![](https://placehold.co/20x18/FCBF49/FCBF49.png)![](https://placehold.co/20x18/2EC4B6/2EC4B6.png)![](https://placehold.co/20x18/6C5CE7/6C5CE7.png)![](https://placehold.co/20x18/E91E8C/E91E8C.png) | `npg` | crimson → amber → turquoise → periwinkle → fuchsia |

### DivergingColormap

Two hues through a light center. Good for data diverging around a meaningful midpoint.

| | Preset | Range |
|---|---|---|
| ![](https://placehold.co/20x18/E63946/E63946.png)![](https://placehold.co/20x18/F8F8F8/F8F8F8.png)![](https://placehold.co/20x18/457B9D/457B9D.png) | `crimson_cobalt` | red ↔ steel blue |
| ![](https://placehold.co/20x18/FCBF49/FCBF49.png)![](https://placehold.co/20x18/FAFAFA/FAFAFA.png)![](https://placehold.co/20x18/6C5CE7/6C5CE7.png) | `amber_periwinkle` | amber ↔ blue-violet |

### CyclicColormap

Wraps back to its starting color. Good for phase or angle data.

| | Preset | Cycle |
|---|---|---|
| ![](https://placehold.co/20x18/E63946/E63946.png)![](https://placehold.co/20x18/F4845F/F4845F.png)![](https://placehold.co/20x18/6BBF59/6BBF59.png)![](https://placehold.co/20x18/2EC4B6/2EC4B6.png)![](https://placehold.co/20x18/B05CC8/B05CC8.png) | `npg` | crimson → tangerine → lime → turquoise → orchid → crimson |

### Usage

```python
from stylia import FadingColormap, DivergingColormap

ccm = FadingColormap("turquoise")
ccm.fit(data)
colors = ccm.transform(data)                 # list of RGBA tuples
colors = ccm.transform(data, alpha=0.6)     # with alpha
colors = ccm.transform(data, lighten=0.3)   # lightened
swatches = ccm.sample(8)                    # 8 evenly-spaced swatches

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

`SIZE` is the figure width basis — `7.09 in` for `print`, `13 in` for `slide`. Use `stylia.get_size()` to read it at runtime. `width` and `height` in `create_figure` are fractions of `SIZE`.

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

Use `stylia.get_markersize()` to get the format-aware value at runtime (`"small"`, `"normal"`, or `"big"`).

---

## Disclaimer

Stylia is designed for internal use across Ersilia projects and is shared openly in case it is useful to others. It is not a general-purpose plotting library — for that, see [Matplotlib](https://matplotlib.org/) or [seaborn](https://seaborn.pydata.org/).

---

## About Us

<a href="https://ersilia.io" target="_blank"><img src="https://raw.githubusercontent.com/ersilia-os/ersilia/master/assets/Ersilia_Plum.png" height="80" alt="Ersilia logo"/></a>

Stylia is developed and maintained by the [Ersilia Open Source Initiative](https://ersilia.io), a non-profit organisation dedicated to providing open-source AI/ML tools for infectious disease research in the Global South.

[Visit us](https://ersilia.io) · [GitHub](https://github.com/ersilia-os) · [Twitter](https://twitter.com/ersiliaio)
