""" Example: plotting an Accola atom group.

    We approximate the Accola atom group (Maskit, VIII.F.7). In the lomit (as n->\infty),
    the quotient Ω(G)/G has four components. Two of these components are discs: they are the projections of the discs 0<|z|<1
    and 2<|z| in Ω(G) which both have trivial stabiliser in G, and which are called atoms.
"""

from bella import cayley
import holoviews as hv
hv.extension('bokeh')
from mpmath import mp
from functools import reduce

class AtomGroup(cayley.GroupCache):
    def __init__(self, n, M, speedfactor = 0.3):
        """ Approximations of Accola's atom group.

            We will generate n circles on the two spirals, smaller circles for bigger M.
            The speed of spiraling is controlled by speedfactor.
        """

        spiral1 = lambda θ: 1 + 1/(1+mp.exp(-speedfactor*θ))
        spiral2 = lambda θ: spiral1(θ+mp.pi)

        def walk_a_spiral(this_r, other_r, direction):
            circles = []
            θ = 0
            for i in range(0,n):
                radius = min( mp.fabs(other_r(θ-2*mp.pi) - this_r(θ)), mp.fabs(other_r(θ+2*mp.pi) - this_r(θ)), mp.fabs(other_r(θ) - this_r(θ)) )/(2*M)
                Δθ = direction*mp.atan(radius/this_r(θ))
                centre = mp.exp(1j*(θ + Δθ))*mp.sqrt( this_r(θ)**2 + radius**2 )
                circles.append((centre,radius))
                θ = θ + 2*Δθ
            return circles

        self.circles1 = walk_a_spiral(spiral1,spiral2,+1)+walk_a_spiral(spiral1,spiral2,-1)
        self.circles2 = walk_a_spiral(spiral2,spiral1,+1)+walk_a_spiral(spiral2,spiral1,-1)

        super().__init__(cayley.generators_from_circle_inversions(self.circles1+self.circles2, []))

depth = 50
logpoints = 4
generators = 10000
add_bead_annotations = False #Adding these annotations significantly increases compute time. (on the order of 10 seconds vs 30 minutes)
G = AtomGroup(generators, 1.2)
seed = G.fixed_points((0,1))[0]
df = G.coloured_limit_set_mc(depth,10**logpoints, seed=seed)
scatter = hv.Scatter(df, kdims = ['x'], vdims = ['y','colour'])\
            .opts(marker = "dot", size = .1,  color = 'black', width=10000, height=10000, data_aspect=1)

if add_bead_annotations:
    # circles which we are inverting across
    beads = [hv.Ellipse(float(centre.real), float(centre.imag), float(radius)*2).opts(color='red') for (centre, radius) in G.circles1]
    beads += [hv.Ellipse(float(centre.real), float(centre.imag), float(radius)*2).opts(color='blue') for (centre, radius) in G.circles2]

    # isometric circles of generators
    isocircles = [G.isometric_circle(w) for w in G.free_cayley_graph_bfs(1)]
    ellipses = [hv.Ellipse(float(centre.real), float(centre.imag), float(radius)*2).opts(color='gray') for (centre, radius) in isocircles] #<-the final parameter of hv.Ellipse is diameter, not radius
    scatter = reduce(lambda a,b: a*b, ellipses+beads, scatter)
    hv.save(scatter, "atom.png")
else:
    hv.save(scatter, "atom_no_beads.png")
