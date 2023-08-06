""" Example: profile GroupCache.free_cayley_graph_mc() vs GroupCache.cayley_graph_mc()

    The output should show that the free_* version is much faster than the non-free_* version.
"""

from bella import cayley
import mpmath as mp
import cProfile

def testfn(free):
  mu = 2 + 2j
  p = 2
  q = 3
  alpha = mp.exp(1j*mp.pi/p)
  beta = mp.exp(1j*mp.pi/q)
  X = mp.matrix([[alpha,1],[0,mp.conj(alpha)]])
  Y = mp.matrix([[beta,0],[mu,mp.conj(beta)]])
  G = cayley.GroupCache([X,Y], [(0,)*p,(1,)*q])
  # We cast to a list to force the generator returned to actually be computed.
  if free:
      return list(G.free_cayley_graph_mc(15,10**4))
  else:
      return list(G.cayley_graph_mc(15,10**4))

cProfile.run('testfn(True)')
cProfile.run('testfn(False)')
