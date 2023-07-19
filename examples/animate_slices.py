from bella import cayley, moduli
import mpmath as mp
import holoviews as hv
import pandas as pd
hv.extension('bokeh')
from bokeh.plotting import show
from mpmath.libmp.libhyper import NoConvergence as BadThing

θ = 0
depth = 30

first = -2000
last = 2000
scale = 1000

def one_frame(kk):
    print(f"#{kk}")
    η = mp.exp(kk/scale)
    L = list(moduli.approximate_riley_slice(θ,η, depth))
    df = pd.DataFrame(data=[(float(point.real), float(point.imag)) for point in L], columns=['x','y'], copy=False)
    scatter = hv.Scatter(df, 'x','y').opts(marker = "dot", size = 5, width=800, height=800, data_aspect=1, color='black') * hv.Text(0,3,f"η = exp({kk}/{scale}) = {complex(η):.2f}")
    hv.save(scatter.redim(x=hv.Dimension('x', range=(-4.5,4.5)),y=hv.Dimension('y', range=(-4.5, 4.5))), f'animation/frame{-first+kk:05}.png', fmt='png')
    print(f"Done {kk}")

for kk in range(first, last):
    try:
        one_frame(kk)
    except BadThing:
        print(f"**BAD {kk}")
