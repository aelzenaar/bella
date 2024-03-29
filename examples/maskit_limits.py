""" Example: plotting coloured limit sets of Maskit groups [MSW02, chap. 9] in a dynamic way.
"""
from bella import cayley, slices
from mpmath import mp
import holoviews as hv
import pandas as pd
hv.extension('bokeh')
import panel as pn
from bella.hvhelp import makeCircles,pairsToCircles

class MaskitGroup(cayley.GroupCache):
    def __init__(self, μ):
        self.μ = μ

        X = mp.matrix([[-1j*μ, -1j],[-1j, 0]])
        Y = mp.matrix([[1,2], [0,1]])

        super().__init__([X,Y])

# This subroutine takes a particular MaskitGroup(μ) and
# returns an overlay of:
#   (a) an hv.Scatter plot where x and y values are points in the limit set, and the colour comes from the
#       `colour` attribute returned from GroupCache.coloured_limit_set,
#       i.e. it refers to the first letter in the word indexing that limit point); and
#   (b) three points, which give the fixed points of the generators X and Y (the fourth fixed point is at infinity).
def limit_set_points(x=1,y=0, logpoints=3):
    G = MaskitGroup(x+1j*y)
    fixed_points_X = [ [float(p.real), float(p.imag)] for p in G.fixed_points((0,))]
    fixed_points_Y = [ [float(p.real), float(p.imag)] for p in G.fixed_points((1,))]
    seed = G.fixed_points((0,1))[0]
    df = G.coloured_limit_set_fast(10**logpoints, seed=seed)
    circles = G.coloured_isometric_circles_bfs(1)
    scatter = hv.Scatter(df, kdims = ['x'], vdims = ['y','colour'])\
                .opts(marker = "dot", size = 0.1,  color = 'colour', width=800, height=800, data_aspect=1, cmap='Category10')\
                  .redim(x=hv.Dimension('x', range=(-4,4)),y=hv.Dimension('y', range=(-4, 4)))
    return scatter * hv.Points(fixed_points_X).opts(marker = "dot", size = 20,  color = 'red', width=800, height=800, data_aspect=1)\
      * hv.Points(fixed_points_Y).opts(marker = "dot", size = 20,  color = 'green', width=800, height=800, data_aspect=1)\
      * makeCircles(circles, kdims = ['x'], vdims = ['y','colour','radius']).opts(radius='radius', color = 'colour', data_aspect=1, cmap='Category10', alpha=0.5)

# Paint the slice with given parameters
def slice_points(depth):
    print("Recomputing slice")
    df = slices.maskit_slice_exterior(depth, extraprec=1500)

    return hv.Scatter(df, kdims=['x'],vdims=['y'])\
             .opts(marker = "dot", size = 4, width=800, height=800, data_aspect=1, color='black', cmap='kr')\
             .redim(x=hv.Dimension('x', range=(-4,4)),y=hv.Dimension('y', range=(-4, 4)))

# Plot which displays a single dot at x_dot, y_dot
def clickable_panel(x_dot, y_dot):
    return hv.Points([[x_dot, y_dot]])\
             .opts(marker = "dot", size = 20,  color = 'black', width=800, height=800, data_aspect=1, cmap='Category10')\
         * hv.Text(x_dot,y_dot+.1, f"{x_dot:.2f} + {y_dot:.2f}i")

# Sliders and displays
depth_slider = pn.widgets.IntSlider(name='depth to compute slice', value=15, start=10, end=50)
points_slider = pn.widgets.IntSlider(name='log10(number of points)', value=4, start=2, end=8)
order_sliders = pn.Column(depth_slider, points_slider)

# Overlay the plots
slice_plot_blank = hv.Points([])
stream = hv.streams.Tap(source=slice_plot_blank, x=0, y=2)
slice_plot = slice_plot_blank *\
             hv.DynamicMap(pn.bind(slice_points, depth=depth_slider)) *\
             hv.DynamicMap(pn.bind(clickable_panel, x_dot = stream.param.x, y_dot = stream.param.y))
limitset_plot = pn.bind(limit_set_points, x = stream.param.x, y = stream.param.y, logpoints = points_slider)

app = pn.Row(slice_plot, order_sliders, limitset_plot)

app.servable(title="Maskit slice")
