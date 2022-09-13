# Stylia: decent scientific plot styles

This repository contains predefined [MatPlotLib](https://matplotlib.org/) styles to be used by all projects within the [Ersilia Open Source Initiative](https://ersilia.io).

* By default, [scientific color schemes](https://www.nature.com/articles/s41467-020-19160-7) are used. Learn more [here](https://www.fabiocrameri.ch/colourmaps/).
* Sizes are guided by *Nature* journals formats, as described in their [guidelines](https://www.nature.com/documents/nature-final-artwork.pdf).

## Installation
First make sure that you have the Arial font installed in your computer (Linux systems do not have it preinstalled). The best is to install Arial in the conda environment you are using:

```conda install -c conda-forge mscorefonts```

You can read more about fonts and matplotlib in this excellent [blogpost](https://alexanderlabwhoi.github.io/post/2021-03-missingfont/) from the Alexander Lab

### From source
```bash
git clone https://github.com/ersilia-os/stylia.git
cd stylia
pip install -e . 
```

### With pip
```bash
pip install git+https://github.com/ersilia-os/stylia.git
```

## Usage
### Create figures

```python
import stylia
import numpy as np

# create a figure to be used in a slide
fig, axs = stylia.create_figure(nrows=1, ncols=2, area_proportion=1, aspect_ratio=(2,1), support="paper")

# define your plots with matplotlib
def my_histogram(ax, x):
    ax.hist(x)

def my_scatterplot(ax, x, y):
    ax.scatter(x, y)

# get data
x = np.random.normal(size=100)
y = x**2

# first plot
ax = axs.next()
my_histogram(ax, x)

# work on the second plot
ax = axs.next()
my_scatterplot(ax, x, y)

# save figure
stylia.save_figure("my_first_figure.png")
```

### Colors

#### Color maps

You can use color maps in [Scikit-Learn](https://scikit-learn.org/stable/) fit-transform style.

```python
from stylia.colors import ContinuousColorMap
import numpy as np

data = np.random.sample(100)

cmap = ContinuousColorMap()
cmap.fit(data)
colors = cmap.transform(data)
```

## About us
Learn more about the Ersilia Open Source Initiative [here](https://ersilia.io)!
