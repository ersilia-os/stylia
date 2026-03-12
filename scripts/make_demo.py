"""Generate demo figures for README (article style and ersilia style)."""
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import stylia

np.random.seed(42)

# ── shared synthetic data ────────────────────────────────────────────────────

x = np.linspace(0, 4 * np.pi, 120)

# line data: 4 smooth curves
lines_y = [
    np.sin(x) * np.exp(-0.08 * x) + 0.06 * np.random.randn(len(x)),
    np.cos(x) * np.exp(-0.06 * x) + 0.06 * np.random.randn(len(x)),
    np.sin(x + 1) * np.exp(-0.10 * x) + 0.06 * np.random.randn(len(x)),
    np.cos(x + 1) * np.exp(-0.05 * x) + 0.06 * np.random.randn(len(x)),
]

# bar data
bar_labels = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon"]
bar_values = np.array([4.2, 2.8, 5.1, 3.5, 1.9])
bar_err    = np.array([0.3, 0.4, 0.2, 0.5, 0.3])

# area / filled lines
area_x = np.linspace(0, 10, 200)
area_y1 = 2 + np.cumsum(0.05 * np.random.randn(200))
area_y2 = area_y1 + 0.8 + 0.3 * np.abs(np.sin(area_x))

# scatter / colormap data
n_scatter = 150
sc_x = np.random.randn(n_scatter)
sc_y = np.random.randn(n_scatter)
sc_z = sc_x * 0.7 + np.random.randn(n_scatter) * 0.5  # diverges around 0

# random walk for spectral colormap demo
n_walk = 300
walk_x = np.cumsum(np.random.randn(n_walk)) * 0.15
walk_y = np.cumsum(np.random.randn(n_walk)) * 0.15
walk_t = np.linspace(0, 1, n_walk)


def make_grid(style, outpath):
    stylia.set_format("print")
    stylia.set_style(style)
    from stylia import CategoricalPalette, DivergingColormap, SpectralColormap
    pal = CategoricalPalette(style if style == "ersilia" else "npg")

    lw  = stylia.LINEWIDTH        # thin default

    fig, axs = stylia.create_figure(2, 3, width=1.0, height=0.65)

    # ── panel A: multi-line ──────────────────────────────────────────────────
    ax = axs.next()
    colors = pal.get(4)
    for i, (yi, col) in enumerate(zip(lines_y, colors)):
        ax.plot(x, yi, color=col, linewidth=lw, alpha=0.9, label=f"Series {i+1}")
    ax.set_xlabel("Time / s")
    ax.set_ylabel("Amplitude")
    ax.legend(loc="lower right")
    stylia.label(ax, title="Damped oscillations", abc="A")

    # ── panel B: bar + error bars ────────────────────────────────────────────
    ax = axs.next()
    colors_b = pal.get(len(bar_labels))
    ax.bar(bar_labels, bar_values, yerr=bar_err, color=colors_b,
           error_kw=dict(linewidth=lw, capsize=2, capthick=lw))
    ax.set_xlabel("Group")
    ax.set_ylabel("Score")
    stylia.label(ax, title="Group comparison", abc="B")

    # ── panel C: step histogram ───────────────────────────────────────────────
    ax = axs.next()
    c4 = pal.get(3)
    for j, col in enumerate(c4):
        data = np.random.normal(loc=j * 0.8, scale=0.5, size=300)
        ax.hist(data, bins=24, histtype="stepfilled", color=col, alpha=0.25, linewidth=0)
        ax.hist(data, bins=24, histtype="step", color=col, linewidth=lw, label=f"Group {j+1}")
    ax.set_xlabel("Value")
    ax.set_ylabel("Count")
    ax.legend()
    stylia.label(ax, title="Distribution overlap", abc="C")

    # ── panel D: area / filled lines ─────────────────────────────────────────
    ax = axs.next()
    c2 = pal.get(2)
    ax.plot(area_x, area_y1, color=c2[0], linewidth=lw)
    ax.plot(area_x, area_y2, color=c2[1], linewidth=lw)
    ax.fill_between(area_x, area_y1, area_y2, color=c2[1], alpha=0.15)
    ax.set_xlabel("Time / s")
    ax.set_ylabel("Signal")
    stylia.label(ax, title="Confidence band", abc="D")

    # ── panel E: spectral colormap (random walk colored by time) ─────────────
    ax = axs.next()
    scm_name = "ersilia" if style == "ersilia" else "npg"
    scm = SpectralColormap(scm_name)
    scm.fit(walk_t)
    colors_e = scm.transform(walk_t)
    for i in range(len(walk_t) - 1):
        ax.plot(walk_x[i:i+2], walk_y[i:i+2], color=colors_e[i], linewidth=lw * 1.5)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    stylia.label(ax, title="Spectral colormap", abc="E")

    # ── panel F: diverging colormap ──────────────────────────────────────────
    ax = axs.next()
    dcm_name = "plum_mint" if style == "ersilia" else "crimson_cobalt"
    dcm = DivergingColormap(dcm_name)
    dcm.fit(sc_z)
    colors_f = dcm.transform(sc_z)
    ax.scatter(sc_x, sc_y, c=colors_f, s=stylia.MARKERSIZE_SMALL, zorder=3)
    ax.set_xlabel("Feature 1")
    ax.set_ylabel("Feature 2")
    stylia.label(ax, title="Diverging colormap", abc="F")

    stylia.save_figure(outpath)
    print(f"Saved {outpath}")


_root = os.path.dirname(os.path.dirname(__file__))
make_grid("article", os.path.join(_root, "assets", "demo_article.png"))
make_grid("ersilia", os.path.join(_root, "assets", "demo_ersilia.png"))
