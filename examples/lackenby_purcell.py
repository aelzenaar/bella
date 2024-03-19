""" Example: plotting coloured limit sets of groups uniformising (1;2)-compression bodies.

    Let G be a group generated by two parabolics sharing a common fixed point and an independent loxodromic. Such a group
    generally uniformises a 3-manifold with one genus 2 boundary component and one genus 1 boundary component (a rank 2 cusp).

    See [LP], though we use different generators.

    [LP] M. Lackenby and J. Purcell, "Geodesics and compression bodies" (2014). https://arxiv.org/abs/1302.3652
"""
from bella import cayley
from mpmath import mp
import holoviews as hv
from holoviews import opts
import pandas as pd
hv.extension('bokeh')
import panel as pn
from bella.hvhelp import makeCircles,pairsToCircles

class LackenbyPurcellGroup(cayley.GroupCache):
    def __init__(self, α, β, λ):
        self.α = α
        self.β = β
        self.λ = λ

        X = mp.matrix([[1, α], [0, 1]])
        Y = mp.matrix([[1, β], [0, 1]])
        M = mp.matrix([[λ, λ**2 - 1], [1, λ]])

        super().__init__([X, Y, M])

def limit_set_points(α_x, α_y, β_x, β_y, λ_x, λ_y, logpoints):
    λ = λ_x + λ_y*1j
    α = α_x + α_y*1j
    β = β_x + β_y*1j
    G = LackenbyPurcellGroup(α, β, λ)

    limit_points = G.coloured_limit_set_fast(10**logpoints)
    circles = G.coloured_isometric_circles_bfs(1)

    scatter = hv.Scatter(limit_points, kdims = ['x'], vdims = ['y','colour']).opts(marker = "dot", size = 0.1,  color = 'colour', cmap='Category10', shared_axes=False)\
                .redim(x=hv.Dimension('x', range=(-3,3)),y=hv.Dimension('y', range=(-3, 3)))\
            * makeCircles(circles, kdims = ['x'], vdims = ['y','radius']).opts(radius='radius', color = 'gray', alpha=0.5)\

    square = [(float(z.real), float(z.imag)) for z in [(α + β)/2, (α - β)/2, (-α - β)/2, (-α + β)/2, (α + β)/2]]

    fp = complex(mp.sqrt(λ**2 - 1))
    return (scatter * hv.Points([[fp.real, fp.imag], [-fp.real, -fp.imag]])\
                       .opts(marker = "dot", size = 20,  color = 'red', cmap='Category10')\
                   * hv.Path(square).opts(color = "gray", alpha=0.5)).opts(shared_axes=False,  width=1000, height=1000, data_aspect=1)


# Plot which displays a single dot at x_dot, y_dot
def clickable_panel(x_dot, y_dot):
    return (hv.Points([[x_dot, y_dot]])\
             .opts(marker = "dot", size = 20,  color = 'black', width=250, height=250, data_aspect=1, cmap='Category10')\
         * hv.Text(x_dot,y_dot+.1, f"{x_dot:.2f} + {y_dot:.2f}i")).opts(shared_axes=False)

# Sliders and displays
points_slider = pn.widgets.IntSlider(name='log10(mumber of points)', value=8, start=2, end=8)
order_sliders = pn.Column(points_slider)

# Overlay the plots
lambda_plot_blank = hv.Points([]).opts(shared_axes=False)
lambda_stream = hv.streams.Tap(source=lambda_plot_blank, x=1, y=0)
lambda_plot = lambda_plot_blank * hv.DynamicMap(pn.bind(clickable_panel, x_dot = lambda_stream.param.x, y_dot = lambda_stream.param.y))
lambda_plot.opts(opts.Overlay(title='λ', shared_axes=False))

alpha_plot_blank = hv.Points([]).opts(shared_axes=False)
alpha_stream = hv.streams.Tap(source=alpha_plot_blank, x=0, y=2)
alpha_plot = alpha_plot_blank * hv.DynamicMap(pn.bind(clickable_panel, x_dot = alpha_stream.param.x, y_dot = alpha_stream.param.y))
alpha_plot.opts(opts.Overlay(title='α', shared_axes=False))

beta_plot_blank = hv.Points([]).opts(shared_axes=False)
beta_stream = hv.streams.Tap(source=beta_plot_blank, x=-4, y=0)
beta_plot = beta_plot_blank * hv.DynamicMap(pn.bind(clickable_panel, x_dot = beta_stream.param.x, y_dot = beta_stream.param.y))
beta_plot.opts(opts.Overlay(title='β', shared_axes=False))

limitset_plot = pn.bind(limit_set_points,
                        λ_x = lambda_stream.param.x, λ_y = lambda_stream.param.y,
                        α_x = alpha_stream.param.x, α_y = alpha_stream.param.y,
                        β_x = beta_stream.param.x, β_y = beta_stream.param.y,
                        logpoints = points_slider)

app = pn.Row(pn.Column(lambda_plot, alpha_plot, beta_plot),
             pn.Column(order_sliders, limitset_plot))

app.servable()
