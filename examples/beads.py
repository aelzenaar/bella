""" Example: plotting bead groups.

    Bead groups are defined in Section VIII.F of Maskit, they are very old examples of Kleinian groups (e.g, there is a famous picture of a bead group
    due to Fricke and Klein (fig.65 of [KAG65])) They are generated by the reflections in a string of tangent circles (`beads').

    We give an implementation which allows the input of a arbitrary polygonal path and then fits beads onto the vertices and possibly fills the gaps
    if necessary.

    [KAG86] S.L. Krushkalʹ, B.N. Apanasov, and N.A. Gusevskiĭ, "Kleinian groups in examples
            and problems". American Mathematical Society, 1986.
"""

from bella import cayley
import holoviews as hv
hv.extension('bokeh')
from mpmath import mp
from functools import reduce

class BeadGroup(cayley.GroupCache):
    def __init__(self, path):
        """ Bead group on a polygonal path.


            Represents the orientation preserving half of the group
            generated by circle inversions around the list of circles
            produced in the following way:

            For each point p_i in path = (p_0,...,p_n), let r_i be the lesser
            of the two distances between p_i-1 and p_i, and p_i and p_i+1.
            Add the circle C_i centred at p_i of radius r_i to the list of circles.
            Now,  for each i consider the circles C_i and C_{i+1}. By construction,
            these circles do not intersect, except possibly at a point of tangency.
            Let x and y be the points of the segment [p_i, p_{i+1}] which are respectively
            the intersection points of C_i and C_{i+1} with that segment. Append to the list
            of circles the circle centred at (x+y)/2 with radius |x-y|/2.
        """

        path_with_ends = [path[-1]] + path + [path[0]] # p_n, p_0, ..., p_n, p_0 (so we can take +-1 in subscripts)
        circles_at_vertices = [] # This is the list of C_i
        for i in range(1, len(path_with_ends)-1):
            r_i = min( mp.fabs(path_with_ends[i-1] - path_with_ends[i]), mp.fabs(path_with_ends[i] - path_with_ends[i+1]) )/2
            circles_at_vertices.append( (path_with_ends[i], r_i) )

        filling_circles = []
        for i in range(0, len(path_with_ends)-1):
            radii = [circles_at_vertices[-1][1]] + [ c[1] for c in circles_at_vertices ] + [circles_at_vertices[0][1]]
            x = path_with_ends[i] + radii[i]*(path_with_ends[i+1]-path_with_ends[i])/mp.fabs(path_with_ends[i+1]-path_with_ends[i])
            y = path_with_ends[i+1] + radii[i+1]*(path_with_ends[i]-path_with_ends[i+1])/mp.fabs(path_with_ends[i]-path_with_ends[i+1])
            if not mp.almosteq(x,y):
                filling_circles.append( ((x+y)/2, mp.fabs(x-y)/2) )

        self.circles = circles_at_vertices + filling_circles

        super().__init__(cayley.generators_from_circle_inversions(self.circles, []))

num_points = 10**6

def write_limit_set(G,filename):
    # We put fixed points and beads onto the picture, here is the calculation.
    beads = [hv.Ellipse(float(centre.real), float(centre.imag), float(radius)*2).opts(color='red') for (centre, radius) in G.circles]
    seed = G.fixed_points((0,1))[0]
    fixed_points = [hv.Points([ [float(p.real), float(p.imag)] for p in G.fixed_points((n,))]).opts(marker = "dot", size = 20) for n in range(0,len(G))]

    # compute the limit set
    df = G.coloured_limit_set_fast(num_points, seed=seed)
    scatter = hv.Scatter(df, kdims = ['x'], vdims = ['y','colour'])\
                .opts(marker = "dot", size = 0.1,  color = 'colour', frame_width=1600, frame_height=1600, data_aspect=1, cmap='Set1')


    #isometric circles of generators
    isocircles = [G.isometric_circle(w) for w in G.free_cayley_graph_bfs(1)]
    ellipses = [hv.Ellipse(float(centre.real), float(centre.imag), float(radius)*2).opts(color='gray') for (centre, radius) in isocircles] #<-the final parameter of hv.Ellipse is diameter, not radius

    scatter = reduce(lambda a,b: a*b, ellipses+beads+fixed_points, scatter)
    hv.save(scatter, filename)

# Beads at the roots of unity
root = 8
G = BeadGroup([mp.exp(n*2j*mp.pi/root) for n in range(root)])
write_limit_set(G, 'beads_rootsofunity.png')
print("  beads.py: finished 1/4")

# Beads in a rectangle
G = BeadGroup([0, 1, 1+1j, 1+2j, 2j, 1j])
write_limit_set(G, 'beads_rectangle.png')
print("  beads.py: finished 2/4")

# Beads randomly placed in some curve
G = BeadGroup([0, 1, 2, 1.5+3j, 4j, 5j, 6j - 1, 4j - 3, 2j-2])
write_limit_set(G, 'beads_wonky.png')
print("  beads.py: finished 3/4")

# "Twisted Fuchsian group": Maskit, sec. VIII.F.5
G = BeadGroup([0, 1+1j, 1+mp.sqrt(2) + 1j, 2+mp.sqrt(2), 1 + mp.sqrt(2) - 1j, 1-1j, 0, -1+1j, -1-mp.sqrt(2) + 1j, -2-mp.sqrt(2), -1 - mp.sqrt(2) - 1j, -1-1j ])
write_limit_set(G, 'beads_fig8.png')
print("  beads.py: finished 4/4")
