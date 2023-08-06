from bella import cayley, riley
import mpmath as mp
import holoviews as hv
import pandas as pd
hv.extension('bokeh')
from mpmath.libmp.libhyper import NoConvergence as BadThing
import multiprocessing

def one_frame(kk,θ,depth,logpoints,first,scale):
    print(f"#{kk}")
    η = (kk/scale) * mp.pi
    G = riley.RileyGroup(θ,η,4j)
    df = G.coloured_limit_set_mc(depth,10**logpoints)
    scatter = hv.rasterize(hv.Scatter(df, kdims = ['x'], vdims = ['y','colour']).opts(marker = "dot", size = 1,  color = 'colour', width=800, height=800, data_aspect=1, cmap='Category10'))
    hv.save(scatter.redim(x=hv.Dimension('x', range=(-2,2)),y=hv.Dimension('y', range=(-2, 2))), f'animation/frame{-first+kk:05}.png', fmt='png')
    print(f"Done {kk}")

if __name__=='__main__':
    θ = 0
    depth = 10
    logpoints = 4

    first = 0
    last = 200
    scale = 100
    
    with multiprocessing.Pool(4, maxtasksperchild=1) as pool:
        pool.starmap(one_frame, [ (kk,θ,depth,logpoints,first,scale) for kk in range(first, last) ], chunksize=1)

