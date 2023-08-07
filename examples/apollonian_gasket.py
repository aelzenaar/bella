""" Example: plotting the Apollonian Gasket at high definition.
"""

from bella import riley
import holoviews as hv
hv.extension('bokeh')

# Just compute the gasket as the limit set of the μ=2i parabolic Riley group, and save it to an image file.
depth = 50
logpoints = 4
G = riley.RileyGroup(0, 0, 2j)
seed = G.fixed_points((0,1))[0]
df = G.coloured_limit_set_mc(depth,10**logpoints, seed=seed)
scatter = hv.Scatter(df, kdims = ['x'], vdims = ['y','colour'])\
            .opts(marker = "dot", size = 0.1,  color = 'colour', width=1600, height=1600, data_aspect=1, cmap='Set1')\
              .redim(x=hv.Dimension('x', range=(-4,4)),y=hv.Dimension('y', range=(-4, 4)))
hv.save(scatter, 'apollonian_gasket.png', fmt='png')
