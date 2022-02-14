# Stylia: decent scientific plot styles

This repository contains predefined MatPlotLib styles to be used by all projects within the [Ersilia Open Source Initiative](https://ersilia.io).

* By default, [scientific color schemes](https://www.nature.com/articles/s41467-020-19160-7) are used.
* Sizes are guided by *Nature* journals formats, as described in their [guidelines](https://www.nature.com/documents/nature-final-artwork.pdf).

## Installation
First make sure that you have the Arial font installed in your computer.

```bash
pip install stylia
```

## Usage
### Create figures

```python
import sytlia

# create a figure to be used in a slide
fig, axs = stylia.create_figure(nrows=2, ncols=1, support="slide")

# define your plots with matplotlib
def my_first_plot(ax, x, y):
    ax.scatter(x, y)

def my_second_histogram(ax, x):
    ax.histogram(x,y)

# work on the first plot
ax = axs.next()
my_first_plot(ax)

# work on the second plot
ax = axs.next()
my_second_plot(ax)

# save figure
stylia.save_figure("my_first_figure.png")
```

### Colors

```python


```
