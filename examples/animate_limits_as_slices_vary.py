""" Example: compute the limit sets of a Riley group with fixed μ and varying θ, η.
"""
from bella import cayley, riley
import mpmath as mp
import holoviews as hv
import pandas as pd
hv.extension('bokeh')
import multiprocessing
import os

# Output one frame of the animation. See below for explanation of the parameters.
def one_frame(kk,θ,depth,logpoints,first,scale):
    print("Computing frame "+ str(kk))
    η = (kk/scale) * mp.pi
    G = riley.RileyGroup(θ,η,2j) # <- we fix the value of μ.
    df = G.coloured_limit_set_mc(depth,10**logpoints)
    scatter = hv.Scatter(df, kdims = ['x'], vdims = ['y','colour'])\
                .opts(marker = "dot", size = 1,  color = 'colour', width=1000, height=1000, data_aspect=1, cmap='Category10')\
                .redim(x=hv.Dimension('x', range=(-1,1)),y=hv.Dimension('y', range=(-1, 1)))
    hv.save(scatter, 'animate_limits_as_slices_vary/frame{:05}.png'.format(-first+kk), fmt='png')
    print("Done frame " + str(kk))

# We use this __main__ pattern since we have to use multiprocessing, see
# the documentation: https://docs.python.org/dev/library/multiprocessing.html#multiprocessing-programming
if __name__=='__main__':
    # θ is fixed. Depth and logpoints are passed directly into GroupCache.coloured_limit_set_mc().
    θ = 0
    depth = 20
    logpoints = 4

    # We will compute η as (kk/scale)*π, where kk runs from first to last. Hence to adjust the number of frames
    # adjust scale and modify last so that last/scale is the endpoint value of the anumation that you want.
    first = 0
    last = 400
    scale = 200

    # Make the output directory if necessary.
    try:
        os.mkdir('animate_limits_as_slices_vary')
    except FileExistsError:
        pass

    # If we don't run all of the one_frame() calls in different processes, then we leak memory in holoviews. (The bokeh renderer keeps a copy of every dataframe
    # passed in, so the garbage collector doesn't throw them away even when the one_frame() function ends; since this is global in the holoviews
    # module, the only way we get out of running out of memory is to start a new process each time.) As a nice side-effect, it's fast.
    multiprocessing.set_start_method('spawn') # Using "fork" also leaks memory.
    with multiprocessing.Pool(4, maxtasksperchild=1) as pool:
        pool.starmap(one_frame, [ (kk,θ,depth,logpoints,first,scale) for kk in range(first, last) ], chunksize=1)
