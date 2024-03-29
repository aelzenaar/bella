""" Example: plotting coloured limit sets of elliptic Riley groups in a dynamic way.
"""
from bella import riley, slices
from mpmath import mp
import holoviews as hv
import pandas as pd
hv.extension('bokeh')
import panel as pn
from bella.hvhelp import makeCircles,pairsToCircles

# This subroutine takes a particular ClassicalRileyGroup(p,q,μ) and
# returns an overlay of:
#   (a) an hv.Scatter plot where x and y values are points in the limit set, and the colour comes from the
#       `colour` attribute returned from GroupCache.coloured_limit_set,
#       i.e. it refers to the first letter in the word indexing that limit point); and
#   (b) three points, which give the fixed points of the generators X and Y (the fourth fixed point is at infinity).
def limit_set_points(x, y, p, q, p_inf, q_inf, logpoints):
    print("Recomputing limit set")
    p = mp.inf if p_inf == True else p
    q = mp.inf if q_inf == True else q
    μ =  x + 1j * y
    G = riley.ClassicalRileyGroup(p, q, μ)
    α = complex(G.α)
    β = complex(G.β)

    limit_points = G.coloured_limit_set_fast(10**logpoints)
    circles = G.coloured_isometric_circles_bfs(1)

    scatter = hv.Scatter(limit_points, kdims = ['x'], vdims = ['y','colour']).opts(marker = "dot", size = 0.1,  color = 'colour', width=800, height=800, data_aspect=1, cmap='Category10')\
                .redim(x=hv.Dimension('x', range=(-2,2)),y=hv.Dimension('y', range=(-2, 2)))\
            * makeCircles(circles, kdims = ['x'], vdims = ['y','colour','radius']).opts(radius='radius', color = 'colour', width=800, height=800, data_aspect=1, cmap='Category10', alpha=0.5)\

    # If X is elliptic it has a fixed point away from infinity.
    if not p_inf:
        scatter *= hv.Points([[(-α/(α**2-1)).real, (-α/(α**2-1)).imag]])\
                     .opts(marker = "dot", size = 20,  color = 'red', width=800, height=800, data_aspect=1, cmap='Category10')

    if q_inf:
        y_fixed_points = [[0,0]]
    else:
        y_fixed_points = [[0,0], [((β - β**-1)/μ).real, ((β - β**-1)/μ).imag]]

    return scatter * hv.Points(y_fixed_points)\
                       .opts(marker = "dot", size = 20,  color = 'green', width=800, height=800, data_aspect=1, cmap='Category10')

# Paint the slice with given parameters
def slice_points(p, q, p_inf, q_inf, depth):
    print("Recomputing slice")
    p = mp.inf if p_inf else p
    q = mp.inf if q_inf else q
    df = slices.elliptic_exterior(p, q, depth, extraprec=1500)

    α = mp.exp(mp.pi*1j/p) if not p_inf else 1
    β = mp.exp(mp.pi*1j/q) if not q_inf else 1
    centres  = [-α*(β - mp.conj(β)), -mp.conj(α)*(mp.conj(β) - β), -α*β - mp.conj(α)*mp.conj(β), mp.conj(α)*β + α*mp.conj(β)]
    radius = 2

    return hv.Scatter(df, kdims=['x'],vdims=['y'])\
             .opts(marker = "dot", size = 4, width=800, height=800, data_aspect=1, color='black', cmap='kr')\
             .redim(x=hv.Dimension('x', range=(-4,4)),y=hv.Dimension('y', range=(-4, 4)))\
         * pairsToCircles([(z, radius) for z in centres])

# Plot which displays a single dot at x_dot, y_dot
def clickable_panel(x_dot, y_dot):
    return hv.Points([[x_dot, y_dot]])\
             .opts(marker = "dot", size = 20,  color = 'black', width=800, height=800, data_aspect=1, cmap='Category10')\
         * hv.Text(x_dot,y_dot+.1, f"{x_dot:.2f} + {y_dot:.2f}i")

# Sliders and displays
p_slider = pn.widgets.IntSlider(name='order of X', value=3, start=2, end=20)
p_inf_check = pn.widgets.Checkbox(name='X parabolic (overrides order)')
q_slider = pn.widgets.IntSlider(name='order of Y', value=4, start=2, end=20)
q_inf_check = pn.widgets.Checkbox(name='Y parabolic (overrides order)')
depth_slider = pn.widgets.IntSlider(name='depth to compute slice', value=15, start=10, end=50)
points_slider = pn.widgets.IntSlider(name='log10(number of points)', value=4, start=2, end=8)
order_sliders = pn.Column(p_slider, p_inf_check, q_slider, q_inf_check, depth_slider, points_slider)

# Overlay the plots
slice_plot_blank = hv.Points([])
stream = hv.streams.Tap(source=slice_plot_blank, x=0, y=2)
slice_plot = slice_plot_blank *\
             hv.DynamicMap(pn.bind(slice_points, p=p_slider, q=q_slider, p_inf = p_inf_check, q_inf = q_inf_check, depth=depth_slider)) *\
             hv.DynamicMap(pn.bind(clickable_panel, x_dot = stream.param.x, y_dot = stream.param.y))
limitset_plot = pn.bind(limit_set_points, x = stream.param.x, y = stream.param.y, p = p_slider, q = q_slider, p_inf = p_inf_check, q_inf = q_inf_check, logpoints = points_slider)

app = pn.Row(slice_plot, order_sliders, limitset_plot)

app.servable("Riley slices")
