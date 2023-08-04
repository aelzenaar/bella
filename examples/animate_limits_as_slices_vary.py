from bella import cayley, riley
import mpmath as mp
import holoviews as hv
import pandas as pd
hv.extension('bokeh')
from bokeh.plotting import show
from mpmath.libmp.libhyper import NoConvergence as BadThing

θ = 0
depth = 20
logpoints = 4

first = 0
last = 200
scale = 100

def one_frame(kk):
    print(f"#{kk}")
    η = (kk/scale) * mp.pi
    G = riley.RileyGroup(θ,η,4j)
    df = G.coloured_limit_set_mc(depth,10**logpoints)
    scatter = hv.Scatter(df, kdims = ['x'], vdims = ['y','colour']).opts(marker = "dot", size = 1,  color = 'colour', width=800, height=800, data_aspect=1, cmap='Category10')
    hv.save(scatter.redim(x=hv.Dimension('x', range=(-2,2)),y=hv.Dimension('y', range=(-2, 2))), f'animation/frame{-first+kk:05}.png', fmt='png')
    print(f"Done {kk}")

for kk in range(first, last):
    try:
        one_frame(kk)
    except BadThing:
        print(f"**BAD {kk}")
