""" Example: plotting coloured limit sets of Dunfield-Tiozzo groups [DT] in a dynamic way.

    [DT] Nathan M. Dunfield and Giulio Tiozzo, "Roots of Alexander polynomials of random positive 3-braids" (2024). https://arxiv.org/abs/2402.06771
"""
from bella import cayley, slices
from mpmath import mp
import holoviews as hv
from holoviews import opts
import pandas as pd
hv.extension('bokeh')
import panel as pn
from bella.hvhelp import makeCircles,pairsToCircles
from holoviews.operation.datashader import datashade, rasterize, shade, dynspread, spread
import datashader as ds

class DunfieldTiozzoGroup(cayley.GroupCache):
    def __init__(self, t):
        self.t = t
        u = mp.sqrt(-t)

        # X = (1/u)*mp.matrix([[-t,1],[0,1]])
        # Y = (1/u)*mp.matrix([[1,0],[t,-t]])
        X = (1/u)*mp.matrix([[1-t, -1],[-t, 0]])
        Y = (1/u)*mp.matrix([[1,0], [1,-t]])
        R = X*Y*X
        S = X*Y

        super().__init__([R,S])


# This subroutine takes a particular DunfieldTiozzoGroup(μ) and returns an overlay of:
#   (a) an hv.Scatter plot where x and y values are points in the limit set, and the colour comes from the
#       `colour` attribute returned from GroupCache.coloured_limit_set,
#       i.e. it refers to the first letter in the word indexing that limit point); and
#   (b) three points, which give the fixed points of the generators X and Y (the fourth fixed point is at infinity).
def limit_set_points(x=1,y=0, logpoints=3):
    t = x+1j*y
    G = DunfieldTiozzoGroup(t)
    fixed_points_X = [ [float(p.real), float(p.imag)] for p in G.fixed_points((0,))]
    fixed_points_Y = [ [float(p.real), float(p.imag)] for p in G.fixed_points((1,))]
    fixed_points_XYX = [ [float(p.real), float(p.imag)] for p in G.fixed_points((0,1,0))]
    seed = G.fixed_points((0,1))[0]
    df = G.coloured_limit_set_fast(10**logpoints, seed=seed)

    circles_1 = [G.isometric_circle((0,)), G.isometric_circle((2,))]
    circles_2 = [G.isometric_circle((1,)), G.isometric_circle((3,))]
    circles_3 = [G.isometric_circle((0,1,)), G.isometric_circle((3,2,))]

    scatter = hv.Scatter(df, kdims = ['x'], vdims = ['y','colour'])\
                .opts(marker = "dot", size = 0.1,  color = 'colour', width=800, height=800, data_aspect=1, cmap='Category10', shared_axes=False)\
                  .redim(x=hv.Dimension('x', range=(-4,4)),y=hv.Dimension('y', range=(-4, 4)))

    return (scatter * hv.Points(fixed_points_X).opts(marker = "dot", size = 20,  color = 'red', width=800, height=800, data_aspect=1, shared_axes=False)\
      * hv.Points(fixed_points_Y).opts(marker = "dot", size = 20,  color = 'green', width=800, height=800, data_aspect=1, shared_axes=False)\
      * pairsToCircles(circles_2).opts(color='green')\
      * pairsToCircles(circles_1).opts(color='red')
      * pairsToCircles(circles_3).opts(color='blue')\
          ).opts(opts.Overlay(shared_axes=False))

# Plot which displays a single dot at x_dot, y_dot
def clickable_panel(x_dot, y_dot):
    return (hv.Points([[x_dot, y_dot]])\
             .opts(marker = "dot", size = 20,  color = 'black', width=800, height=800, data_aspect=1, cmap='Category10', shared_axes=False)\
         * hv.Text(x_dot,y_dot+.1, f"{x_dot:.2f} + {y_dot:.2f}i")).opts(opts.Overlay(shared_axes=False))

def slice_panel():
    pts = pd.read_csv('dunfield_tiozzo.csv', names=['x','y','colour'])
    # return hv.Scatter(pts[pts['colour']=='Positive'], kdims=['x'],vdims=['y','colour'])\
    return datashade(hv.Scatter(pts, kdims=['x'],vdims=['y','colour']), aggregator=ds.by('colour', ds.count()))\
             .opts(width=800, height=800, shared_axes=False)\
             .redim(x=hv.Dimension('x', range=(-4,4)),y=hv.Dimension('y', range=(-4, 4)))

# Sliders and displays
points_slider = pn.widgets.IntSlider(name='log10(number of points)', value=4, start=2, end=8)
order_sliders = pn.Column(points_slider)

# Overlay the plots
slice_plot_blank = hv.Points([])
stream = hv.streams.Tap(source=slice_plot_blank, x=1.37, y=1.52)
slice_plot = slice_plot_blank *\
             slice_panel() *\
             hv.DynamicMap(pn.bind(clickable_panel, x_dot = stream.param.x, y_dot = stream.param.y))
limitset_plot = pn.bind(limit_set_points, x = stream.param.x, y = stream.param.y, logpoints = points_slider)

app = pn.Row(slice_plot, order_sliders, limitset_plot)

app.servable(title="Dunfield Tiozzo groups")
