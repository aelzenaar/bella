""" Example: plotting the figure eight knot limit set along with the traces of elements in the group.
"""

from bella import farey, riley,cayley
from mpmath import mp
import holoviews as hv
hv.extension('bokeh')

# Just compute the parabolic slice and save it to an image file.
ω = mp.exp(2*mp.pi*1j/3)
G = riley.ClassicalRileyGroup(mp.inf, mp.inf, -ω)

traces = []
for word in G.free_cayley_graph_dfs(6):
  trace = cayley.simple_tr(G[word])
  traces.append(trace)
  # print(trace)
# for r,s in farey.walk_tree_bfs(10):
#   traces.append(G.farey_polynomial(r,s)(-ω))
print(len(traces))

logpoints = 7
seed = G.fixed_points((0,1))[0]
df = G.coloured_limit_set_fast(10**logpoints, seed=seed)
scatter = hv.Scatter(df, kdims = ['x'], vdims = ['y','colour'])\
            .opts(marker = "dot", size = 0.1,  color = 'colour', frame_width=1000, frame_height=1000, data_aspect=1, cmap='Set1')\
              .redim(x=hv.Dimension('x', range=(-4,4)),y=hv.Dimension('y', range=(-4, 4)))

scatter *= hv.Points([(float(z.real), float(z.imag)) for z in traces]).opts(color='black', size=5)

hv.save(scatter, 'fig8lattice.png', fmt='png')
