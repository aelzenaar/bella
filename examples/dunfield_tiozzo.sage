# This is a very naive sage script to generate points in the exterior of the Dunfield-Tiozzo slice
# (see dunfield_tiozzo.py).
#
# Setting depth high will seriously tax your computer since we do very minimal caching. To improve things
# we can use the recursive product formula from our Farey polynomial paper but it seems like a lot of work
# to implement for a 1-off thing.

import random
import itertools
import csv
from sage.libs.mpmath.utils import mpmath_to_sage, sage_to_mpmath
import mpmath

depth = 50
max_number=200000
prec=200

K.<t> = FunctionField(QQ)

def random_word(max_length=depth):
    word = []
    if random.choice(['pos','all']) == 'pos':
        letters = ['A','B', 'end']
    else:
        letters = ['a','b','A','B', 'end']
    while len(word) < max_length:
        next_letter = random.choice(letters)
        if next_letter == 'end':
            if len(word) > 0:
              break
            else:
              continue

        if len(word) == 0 or next_letter != word[-1].swapcase():
            word.append(next_letter)
        else:
            continue
    return tuple(word)


A = Matrix([[-t,1],[0,1]])
B = Matrix([[1,0],[t,-t]])
A = A/det(A)
B = B/det(B)
a = A.inverse()
b = B.inverse()

all_roots = []
colours = []

done = set()

n=0
while n < max_number:
    word = '*'.join(random_word())
    if word in done:
        print(f' * * retrying')
        continue
    else:
        done.add(word)
        print(f' * {int(n+1)}/{int(max_number)}\t{(int(100)*int(n+1)/int(max_number)):.3f}%')
        n += 1
    evaled = eval(word)
    trace = ((evaled.trace())**2 - 4).numerator()

    if(word.isupper()):
      colour = 'Positive'
    else:
      colour = 'Non-positive'

    if trace != 0:
      roots = [mpmath_to_sage(z,prec) for z in mpmath.polyroots([ sage_to_mpmath(x,prec) for x in list(reversed(trace.list()))], maxsteps=500,extraprec=1000)]
      # roots = [r for r,_ in trace.roots(CC)]
      all_roots += [r for r in roots]
      colours += [colour]*len(roots)

C = []
for r, colour in zip(all_roots, colours):
  n = N(r)
  C.append([str(real(n)), str(imag(n)), colour])

with open('dunfield_tiozzo.csv', 'w') as f:
    c = csv.writer(f)
    c.writerows(C)
