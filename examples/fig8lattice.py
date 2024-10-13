""" Example: plotting the figure eight knot limit set along with
    the traces of elements in the group and the limit set of a
    Seifert surface subgroup.
"""

from bella import riley,cayley
from mpmath import mp
import holoviews as hv
hv.extension('matplotlib')

omega = mp.exp(2*mp.pi*1j/3)
G = riley.ClassicalRileyGroup(mp.inf, mp.inf, -omega)

traces = []
for word in G.free_cayley_graph_dfs(6):
  trace = cayley.simple_tr(G[word])
  traces.append(trace)
print(len(traces))

numpoints = 4*10**7
seed = G.fixed_points((0,1))[0]
limset = G.coloured_limit_set_fast(numpoints, seed=seed)
scatter = hv.Scatter(limset, kdims = ['x'], vdims = ['y','colour'])\
            .opts(marker = "d", s = .2,\
                  aspect=1, fig_size=1000,\
                  color = 'colour', cmap="glasbey_cool")\
              .redim(x=hv.Dimension('x', range=(-2, 2)),\
                     y=hv.Dimension('y', range=(-2, 2)))

P = G.subgroup([ G.string_to_word("YxYXyxYx"), G.string_to_word("xYXy") ])
limsetP = P.coloured_limit_set_fast(numpoints, (P.fixed_points((1,1)))[0])
scatterP = hv.Scatter(limsetP, kdims = ['x'], vdims = ['y','colour'])\
             .opts(marker = "d", s=.2, aspect=1, \
                   color = "colour", cmap="glasbey_warm")


scatter *= hv.Points([(float(z.real), float(z.imag)) for z in traces])\
             .opts(color='black', s=5) * scatterP

hv.save(scatter, 'fig8lattice_mpl2.png', fmt='png')
