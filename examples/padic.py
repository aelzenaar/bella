""" Example: p-adic limit sets
"""

from bella import cayley, chistyakov
import numpy as np
import holoviews as hv
import pandas as pd
hv.extension('bokeh')

from pyadic import PAdic
from pyadic.padic import padic_sqrt
from fractions import Fraction as Q


def padic_limit_set(G, filename, prime, depth = 15, logwords=4):
    df = G.coloured_limit_set_mc(depth, 10**logwords, 0, lambda z: chistyakov.Υ(0, 0.5*chistyakov.s0(prime), z, 100))
    scatter = hv.Scatter(df, kdims = ['x'], vdims = ['y','colour']).opts(marker = "dot", size = .1, width=1000, height=1000, data_aspect=1, color='colour', cmap='Set1')\
        .redim(x=hv.Dimension('x', range=(-2,2)),y=hv.Dimension('y', range=(-2, 2)))
    hv.save(scatter, filename)

# This is Example 6.1 of arXiv:2110.10904
one_fifth = PAdic(Q(1,5), 5, 100)
g1 = np.array([[one_fifth, -one_fifth],[-one_fifth,26*one_fifth]])
g2 = np.array([[-1,1],[-one_fifth,-4*one_fifth]])
g3 = np.array([[one_fifth,0],[0,-one_fifth]])
G = cayley.GroupCache([g1,g2,g3], disable_det_warning=True)
padic_limit_set(G,'padic1.png', 5)
print("  padic.py: finished 1/2")

# This is the example of case (g) with G_0 = A_5 in arXiv:2208.12404.
# It is a discrete group which is an HNN-extension of A_5.
q = 11
accuracy = 100 # this is very slow, I guess it is because pyadic is not very efficient internally...
assert q%10==1

t = (1 + padic_sqrt(PAdic( 5, q, accuracy )))/2
uniformiser = PAdic(q,q,accuracy)
quadroot = lambda a,b,c: (-b + padic_sqrt(b**2 - 4*a*c))/(2*a)
a_from_s = lambda s: quadroot(1, -t, 1 - (s-t**2+ 2)/(2- uniformiser**2 - uniformiser**-2))
a = a_from_s(1)

A = np.array([[a, 1],[a*(t-a)-1, t-a]])
B = np.array([[uniformiser,0],[0,uniformiser**-1]])
G = cayley.GroupCache([A,B], disable_det_warning=True)
padic_limit_set(G,'padic2.png', q)
print("  padic.py: finished 2/2.")
