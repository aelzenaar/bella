# This is a very naive sage script to generate points in the exterior of the Dunfield-Tiozzo slice
# (see dunfield_tiozzo.py).
#
# Setting depth high will seriously tax your computer since we do very minimal caching. To improve things
# we can use the recursive product formula from our Farey polynomial paper but it seems like a lot of work
# to implement for a 1-off thing.

import itertools
import csv

depth = 15

t = var('t')

def farey_word(r,s):
    """ Compute the Farey word of slope r/s using the cutting sequence definition.

        The Farey word is W^{-1} Y W X where W is the Riley word; it is the relator in the presentation < X, Y : W_r/s = 1>
        of the r/s two-bridge knot.

        Arguments:
        r, s -- coprime integers such that r/s is the slope of the desired Farey word

        Returns:
        A tuple consisting of single-character strings representing generators of the group and their inverses.
    """

    if gcd(r,s) != 1:
        raise ValueError("Arguments to farey_word should be coprime integers.")

    lookup_table=[['a','A'],['B','b']]
    length = 2*s
    def height(i):
        h = i*r/s
        h = h+1/2 if ceil(h)==h else h
        return ceil(h)
    return tuple( lookup_table[i%2][height(i)%2]  for i in range(1,length+1) )


def walk_tree_bfs(end = None):
    """ Yield every fraction with denominator < `end` in a breadth first way.

        If `end` == None then keep going forever.
    """

    for s in itertools.count(1):
        if s == end:
            return None
        for r in range(0,s+1):
            if gcd(r,s) == 1:
                yield (r,s)

A = Matrix([[-t,1],[0,1]])
B = Matrix([[1,0],[t,-t]])
A = A/det(A)
B = B/det(B)
a = A.inverse()
b = B.inverse()

all_roots = []

cache = dict()

fracs = list(walk_tree_bfs(depth))
n=0
for r,s in fracs:
    n+=1
    print(f' * {int(n)}/{len(fracs)}\t{(int(100)*int(n)/len(fracs)):.3f}%')
    word = '*'.join(farey_word(r,s))
    if word[:-1] in cache:
      evaled = cache[word[:-1]] * eval(word[-1])
    else:
      evaled = eval(word)

    cache[word] = evaled
    trace = evaled.trace()

    try:
      roots = solve(trace == -2, t, to_poly_solve=true)
      all_roots += [root.rhs() for root in roots]
      roots = solve(trace == 2, t, to_poly_solve=true)
      all_roots += [root.rhs() for root in roots]
    except:
      # print(trace)
      pass

C = []
for r in all_roots:
  try:
    n = N(r)
    C.append([str(real(n)), str(imag(n))])
  except:
    pass

with open('dunfield_tiozzo.csv', 'w') as f:
    c = csv.writer(f)
    c.writerows(C)
