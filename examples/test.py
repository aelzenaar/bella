from bella import cayley
import numpy as np
import timeit
import cProfile

def testfn(free):
  mu = 2 + 2j
  p = 2
  q = 3
  alpha = np.exp(1j*np.pi/p)
  beta = np.exp(1j*np.pi/q)
  X = np.array([[alpha,1],[0,np.conj(alpha)]])
  Y = np.array([[beta,0],[mu,np.conj(beta)]])
  G = cayley.GroupCache([X,Y], [(0,)*p,(1,)*q])
  if free:
      return list(G.free_cayley_graph_mc(15,10**3))
  else:
      return list(G.cayley_graph_mc(15,10**3))

cProfile.run('testfn(True)')
cProfile.run('testfn(False)')
