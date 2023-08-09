""" Example: plotting an elliptic Riley slice.

    If you take θ = 0 and η = επ for ε small, and then plot
    the zeros of the standard Farey polynomials, then the 1/2 cusp
    looks like it should be at 2i. But if you plot the limit sets,
    you see that the group is non-discrete. Why is this?
"""

from bella import slices
import holoviews as hv
hv.extension('bokeh')
import panel as pn
from mpmath import mp

depth = 30
p = mp.inf
q = 10

df = slices.elliptic_exterior(p, q, depth)

# We need to make a new category column in the dataframe for the holoview.
df['category'] = "X^" + df.pow_x.astype(str) + ", Y^" + df.pow_y.astype(str)

# Now plot it in a scatter plot with Holoviews, using the new category column as the colour dimension.
roots = hv.Scatter(df, kdims=['x'],vdims=['y', 'category']).opts(marker = "dot", size = 4, width=800, height=800, data_aspect=1, color='category', cmap='kr').redim(x=hv.Dimension('x', range=(-4,4)),y=hv.Dimension('y', range=(-4, 4)))

pn.panel(roots).servable(title='The ({},{})-Riley slice'.format(p,q))
