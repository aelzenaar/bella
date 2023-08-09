""" Example: animate primitive slices.

    Animate the primitive Riley slices for θ = 0 and η running from 0 to 2pi.
    Observe that the 1/2 cusp always looks like 2j, despite (as animate_limits_as_slices_vary.py will show you)
    some of the 2j groups for the same values of θ, η are non-discrete!
"""
from bella import slices
import mpmath as mp
import holoviews as hv
import pandas as pd
hv.extension('bokeh')
import os
import multiprocessing

θ = 0
depth = 35

first = -200
last = 200
scale = 100

# Output one frame of the animation. See below for explanation of the parameters.
def one_frame(kk,θ,depth,first,scale):
    print("Computing frame "+ str(kk))
    η = (kk/scale) * mp.pi
    df = slices.primitive_exterior(θ,η,1,1,depth)
    scatter = hv.Scatter(df, 'x','y')\
                .opts(marker = "dot", size = 5, width=1000, height=500, data_aspect=1, color='black') * hv.Text(0,3,"β = exp(πi ({}/{}))".format(kk,scale))\
                .redim(x=hv.Dimension('x', range=(-5,5)),y=hv.Dimension('y', range=(-2.5, 2.5)))
    hv.save(scatter, 'animate_slices/frame{:05}.png'.format(-first+kk), fmt='png')
    print("Done frame " + str(kk))

# We use this __main__ pattern since we use multiprocessing, see
# the documentation: https://docs.python.org/dev/library/multiprocessing.html#multiprocessing-programming
if __name__=='__main__':
    # θ is fixed. Depth is passed directly into slice..
    θ = 0
    depth = 30

    # We will compute η as (kk/scale)*π, where kk runs from first to last. Hence to adjust the number of frames
    # adjust scale and modify last so that last/scale is the endpoint value of the anumation that you want.
    first = 0
    last = 400
    scale = 200

    # Make the output directory if necessary.
    try:
        os.mkdir('animate_slices')
    except FileExistsError:
        pass

    # Unlike in animate_limits_as_slices_vary.py, using multiprocessing is unnecessary for memory usage,
    # it's just for speed.
    multiprocessing.set_start_method('spawn') # Actually in python 3.14 this will be the default anyway
    with multiprocessing.Pool(8, maxtasksperchild=1) as pool:
        pool.starmap(one_frame, [ (kk,θ,depth,first,scale) for kk in range(first, last) ], chunksize=1)
