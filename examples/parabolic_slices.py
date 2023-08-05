""" Example: plotting parabolic Riley slices

    We will produce a panel application which showcases different level sets of the Farey
    polynomials, as well as the Riley polynomials.
"""

from bella import slices
import pandas as pd
import holoviews as hv
hv.extension('bokeh')
import panel as pn

# Compute a whole bunch of level sets, and stick them into one pandas dataframe
depth = 20
farey_levels = range(-2,3)
riley_slices = [ slices.parabolic_exterior_from_farey(depth, level_set = level) for level in farey_levels ]
riley_slices.append(slices.parabolic_exterior_from_riley(depth))
df = pd.concat(riley_slices)

# We need to make a new category column in the dataframe for the holoview.
df['category'] = df.method + " = " + df.level_set.astype(str)

# Now plot it in a scatter plot with Holoviews, using the new category column as the colour dimension.
roots = hv.Scatter(df, kdims=['x'],vdims=['y', 'category']).opts(marker = "dot", size = 4, width=800, height=800, data_aspect=1, color='category', cmap='kr').redim(x=hv.Dimension('x', range=(-4,4)),y=hv.Dimension('y', range=(-4, 4)))

pn.panel(roots).servable(title='The Riley slice, approximated with different polynomials')
