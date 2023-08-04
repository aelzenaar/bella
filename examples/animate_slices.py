from bella import cayley,riley
import mpmath as mp
import holoviews as hv
import pandas as pd
hv.extension('bokeh')
from bokeh.plotting import show
from mpmath.libmp.libhyper import NoConvergence as BadThing

θ = 0
depth = 35

first = -200
last = 200
scale = 100

def one_frame(kk):
    print(f"#{kk}")
    η = (kk/scale) * mp.pi
    L = list(riley.riley_slice_exterior(θ,η, depth=depth))
    df = pd.DataFrame(data=[(float(point.real), float(point.imag)) for point in L], columns=['x','y'], copy=False)
    scatter = hv.Scatter(df, 'x','y').opts(marker = "dot", size = 5, width=800, height=800, data_aspect=1, color='black') * hv.Text(0,3,f"β = exp(πi ({kk}/{scale}))")
    hv.save(scatter.redim(x=hv.Dimension('x', range=(-4.5,4.5)),y=hv.Dimension('y', range=(-4.5, 4.5))), f'animation/frame{-first+kk:05}.png', fmt='png')
    print(f"Done {kk}")

for kk in range(first, last):
    try:
        one_frame(kk)
    except BadThing:
        print(f"**BAD {kk}")
