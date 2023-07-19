""" Example: profile GroupCache.free_cayley_graph_mc() vs GroupCache.cayley_graph_mc()
"""

from bella import cayley
import mpmath as mp
import timeit
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
  if free:
      return list(G.free_cayley_graph_mc(15,10**3))
  else:
      return list(G.cayley_graph_mc(15,10**3))

cProfile.run('testfn(True)')
cProfile.run('testfn(False)')
