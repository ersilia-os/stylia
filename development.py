import stylia as st
import numpy as np


# create a figure to be used in a slide
fig, axs = st.create_figure(
    nrows=2, ncols=2, width_ratios=[2, 1]
)

# get data
x = np.random.normal(size=100)
y = np.random.normal(size=100)

# first plot, access with flat subplots coordinates (0)
ax = axs[0]
# a default color is used
ax.scatter(x, y)
# write labels to axis, title and numbering of the subplot
st.label(ax, title="My first plot", xlabel="This is the X axis", ylabel="This is the Y axis", abc="A")

# second plot, acces with subplots 2D coordinates (0,1)
ax = axs[0,1]
# use a named color
colors = st.NamedColors()
def my_scatterplot(ax, x, y):
    ax.scatter(x, y, color=colors.red)
my_scatterplot(ax, x, y)
# write only a new title (the rest are defaults)
st.label(ax, title="My second plot")

# third plot, access with next() method
ax = axs.next()
ax.scatter(x, y, color=colors.blue)
cmap = st.ContinuousColorMap()
cmap.fit(x)
colors = cmap.get(x)
ax.scatter(x, y, color=colors)


# save figure
st.save_figure("my_first_figure.png")
