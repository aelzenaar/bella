""" Example: a B-group with an accidental parabolic, obtained from the modular group using Exercise
    IX.I.4 of [M87].

    [M87] Bernard Maskit. Kleinian groups. Grundlehren der mathematischen Wissenshaften 287. Springer-Verlag, 1987.
"""

from bella import cayley
import holoviews as hv
hv.extension('bokeh')
from mpmath import mp

class AccidentalParabolicGroup(cayley.GroupCache):
    def __init__(self):
        X = mp.matrix([[0,-1],[1,0]])
        Y = mp.matrix([[1,1],[0,1]])
        h = mp.matrix([[1,4j],[0,1]])
        super().__init__([X,Y, h@X@h**-1, h@Y@h**-1])

num_points = 10**7
G = AccidentalParabolicGroup()
seed = G.fixed_points((0,1))[0]
df = G.coloured_limit_set_fast(num_points, seed=seed)
scatter = hv.Scatter(df, kdims = ['x'], vdims = ['y','colour'])\
            .opts(marker = "dot", size = 0.1,  color = 'colour', frame_width=2000, frame_height=2000, data_aspect=1, cmap='Set1')\
              .redim(x=hv.Dimension('x', range=(-2.5,2.5)),y=hv.Dimension('y', range=(-0.5, 4.5)))

hv.save(scatter, f"accidental_parabolic.png")
