""" Example: plotting limit sets of Bianchi groups.

    [MR] Colin Maclachlan and Alan W. Reid, "The arithmetic of hyperbolic 3-manifolds". Springer, 2003.
    [S] Richard G. Swan, "Generators and relations for certain special linear groups". In: Advances in Mathematics 6(1), 1971, pp.1-77.
"""

from bella import cayley
import holoviews as hv
hv.extension('bokeh')
from mpmath import mp

num_points = 2*10**7

B1 = cayley.GroupCache([mp.matrix([[0,-1],[1,0]]), mp.matrix([[1j,0],[0,-1j]]), mp.matrix([[1,1],[0,1]]), mp.matrix([[1j,-1],[0, -1j]])])
ω = (-1+1j*mp.sqrt(3))/2
B3 = cayley.GroupCache([mp.matrix([[1,1],[0,1]]), mp.matrix([[1,ω],[0,1]]), mp.matrix([[ω**2,0],[0,ω]]), mp.matrix([[0,-1],[1, 0]])])
σ = 1j*mp.sqrt(2)
B2 = cayley.GroupCache([mp.matrix([[1,1],[0,1]]), mp.matrix([[1,σ],[0,1]]), mp.matrix([[0,-1],[1, 0]])])
φ = 1j*mp.sqrt(5)
B5 = cayley.GroupCache([mp.matrix([[1,1],[0,1]]), mp.matrix([[1,φ],[0,1]]), mp.matrix([[-φ,2],[2,φ]]), mp.matrix([[-φ-4,-2*φ],[2*φ,φ-4]]), mp.matrix([[0,-1],[1, 0]])])


print("O_1")
df = B1.coloured_limit_set_fast(num_points)
scatter = hv.Scatter(df, kdims = ['x'], vdims = ['y','colour'])\
            .opts(marker = "dot", size = 0.1,  color = 'colour', frame_width=2000, frame_height=2000, data_aspect=1, cmap='Set1')\
              .redim(x=hv.Dimension('x', range=(-2,2)),y=hv.Dimension('y', range=(-2, 2)))
hv.save(scatter, f"bianchi_O1.png")

del df
del scatter
del B1

print("O_3")
df = B3.coloured_limit_set_fast(num_points)
scatter = hv.Scatter(df, kdims = ['x'], vdims = ['y','colour'])\
            .opts(marker = "dot", size = 0.1,  color = 'colour', frame_width=2000, frame_height=2000, data_aspect=1, cmap='Set1')\
              .redim(x=hv.Dimension('x', range=(-2,2)),y=hv.Dimension('y', range=(-2, 2)))
hv.save(scatter, f"bianchi_O3.png")

del df
del scatter
del B3

print("O_2")
df = B2.coloured_limit_set_fast(num_points)
scatter = hv.Scatter(df, kdims = ['x'], vdims = ['y','colour'])\
            .opts(marker = "dot", size = 0.1,  color = 'colour', frame_width=2000, frame_height=2000, data_aspect=1, cmap='Set1')\
              .redim(x=hv.Dimension('x', range=(-2,2)),y=hv.Dimension('y', range=(-2, 2)))
hv.save(scatter, f"bianchi_O2.png")

del df
del scatter
del B2

print("O_5")
df = B5.coloured_limit_set_fast(num_points)
scatter = hv.Scatter(df, kdims = ['x'], vdims = ['y','colour'])\
            .opts(marker = "dot", size = 0.1,  color = 'colour', frame_width=2000, frame_height=2000, data_aspect=1, cmap='Set1')\
              .redim(x=hv.Dimension('x', range=(-2,2)),y=hv.Dimension('y', range=(-2, 2)))
hv.save(scatter, f"bianchi_O5.png")
