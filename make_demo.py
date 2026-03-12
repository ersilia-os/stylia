"""Generate demo figures for README (article style and ersilia style)."""
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
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

# stacked bar data
stack_labels = ["Jan", "Feb", "Mar", "Apr"]
stack_a = np.array([3.1, 2.5, 4.0, 3.6])
stack_b = np.array([1.8, 2.2, 1.5, 2.1])
stack_c = np.array([2.0, 1.7, 2.8, 1.9])

# horizontal bar
hbar_labels = ["Method A", "Method B", "Method C", "Method D"]
hbar_values = np.array([0.87, 0.74, 0.91, 0.65])

# area / filled lines
area_x = np.linspace(0, 10, 200)
area_y1 = 2 + np.cumsum(0.05 * np.random.randn(200))
area_y2 = area_y1 + 0.8 + 0.3 * np.abs(np.sin(area_x))


def make_grid(style, outpath):
    stylia.set_format("print")
    stylia.set_style(style)
    from stylia import CategoricalPalette
    pal = CategoricalPalette(style if style == "ersilia" else "npg")

    lw  = stylia.LINEWIDTH        # thin default
    lwt = stylia.LINEWIDTH_THICK  # for emphasis only

    fig, axs = stylia.create_figure(2, 3, width=1.0, height=0.65)

    # ── panel A: multi-line ──────────────────────────────────────────────────
    ax = axs.next()
    colors = pal.get(4)
    for i, (yi, col) in enumerate(zip(lines_y, colors)):
        ax.plot(x, yi, color=col, linewidth=lw, alpha=0.9, label=f"Series {i+1}")
    ax.set_xlabel("Time / s")
    ax.set_ylabel("Amplitude")
    ax.legend(frameon=False, ncol=2)
    stylia.label(ax, title="Damped oscillations", abc="A")

    # ── panel B: bar + error bars ────────────────────────────────────────────
    ax = axs.next()
    colors_b = pal.get(len(bar_labels))
    ax.bar(bar_labels, bar_values, yerr=bar_err, color=colors_b,
           error_kw=dict(linewidth=lw, capsize=2, capthick=lw))
    ax.set_xlabel("Group")
    ax.set_ylabel("Score")
    stylia.label(ax, title="Group comparison", abc="B")

    # ── panel C: stacked bar ─────────────────────────────────────────────────
    ax = axs.next()
    c3 = pal.get(3)
    ax.bar(stack_labels, stack_a, color=c3[0], label="Component A")
    ax.bar(stack_labels, stack_b, bottom=stack_a, color=c3[1], label="Component B")
    ax.bar(stack_labels, stack_c, bottom=stack_a + stack_b, color=c3[2], label="Component C")
    ax.set_xlabel("Month")
    ax.set_ylabel("Value")
    ax.legend(frameon=False)
    stylia.label(ax, title="Stacked composition", abc="C")

    # ── panel D: area / filled lines ─────────────────────────────────────────
    ax = axs.next()
    c2 = pal.get(2)
    ax.plot(area_x, area_y1, color=c2[0], linewidth=lw)
    ax.plot(area_x, area_y2, color=c2[1], linewidth=lw)
    ax.fill_between(area_x, area_y1, area_y2, color=c2[1], alpha=0.15)
    ax.set_xlabel("Time / s")
    ax.set_ylabel("Signal")
    stylia.label(ax, title="Confidence band", abc="D")

    # ── panel E: horizontal bar ───────────────────────────────────────────────
    ax = axs.next()
    colors_h = pal.get(len(hbar_labels))
    ax.barh(hbar_labels, hbar_values, color=colors_h)
    ax.set_xlabel("AUC-ROC")
    ax.set_xlim(0.5, 1.0)
    stylia.label(ax, title="Model ranking", abc="E")

    # ── panel F: step histogram ───────────────────────────────────────────────
    ax = axs.next()
    c4 = pal.get(3)
    for j, col in enumerate(c4):
        data = np.random.normal(loc=j * 0.8, scale=0.5, size=300)
        ax.hist(data, bins=24, histtype="step", color=col,
                linewidth=lw, label=f"Group {j+1}")
    ax.set_xlabel("Value")
    ax.set_ylabel("Count")
    ax.legend(frameon=False)
    stylia.label(ax, title="Distribution overlap", abc="F")

    stylia.save_figure(outpath)
    print(f"Saved {outpath}")


make_grid("article", "assets/demo_article.png")
make_grid("ersilia", "assets/demo_ersilia.png")
