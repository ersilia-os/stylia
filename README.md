# Stylia: decent scientific plot styles

This repository contains predefined MatPlotLib styles to be used by all projects within the [Ersilia Open Source Initiative](https://ersilia.io).

* By default, [scientific color schemes](https://www.nature.com/articles/s41467-020-19160-7) are used. Learn more [here](https://www.fabiocrameri.ch/colourmaps/).
* Sizes are guided by *Nature* journals formats, as described in their [guidelines](https://www.nature.com/documents/nature-final-artwork.pdf).

## Installation
First make sure that you have the Arial font installed in your computer.

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
fig, axs = stylia.create_figure(nrows=2, ncols=1, support="slide")

# define your plots with matplotlib
def my_histogram(ax, x):
    ax.histogram(x,y)

def my_scatter(ax, x, y):
    ax.scatter(x, y)

# get data
x = np.random.normal(100)
y = x**2

# first plot
ax = axs.next()
my_histogram(ax, x)

# work on the second plot
ax = axs.next()
my_scatter(ax, x)

# save figure
stylia.save_figure("my_first_figure.png")
```

### Colors

```python
from stylia import Colors

```

#### From categorical data


#### From continuous data


#### From 

### Sizes
