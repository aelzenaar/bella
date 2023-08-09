""" Example: produce a list of parabolic Farey and Riley polynomials
"""

from bella import farey,riley
from mpmath import mp
import numpy as np
np.set_printoptions(precision=4) # This does not seem to work despite https://github.com/numpy/numpy/pull/21654
np.polynomial.set_default_printstyle('ascii')
P = np.polynomial.Polynomial

max_denom = 13

def build_tex_table(caption, function):
    print("""\
\\begin{table}
  \\begin{tabular}{cc}""")
    for r,s in farey.walk_tree_bfs(max_denom):
        if r % 2 == 0:
            continue
        print("    ${}/{}$ & $ {} $\\\\".format(r,s,function(r,s)))
    print("""\
  \\end{{tabular}}
  \\caption{{{}}}
\\end{{table}}
""".format(caption))


build_tex_table("The Riley words", lambda r,s: ''.join(farey.riley_word(r,s)))
build_tex_table("The Farey words", lambda r,s: ''.join(farey.farey_word(r,s)))
build_tex_table("The Riley polynomials", lambda r,s: str(farey.riley_polynomial(r,s)).replace("**","^") )
parabolic_traces = riley.traces_from_holonomies(0,0)
build_tex_table("The Farey polynomials (parabolic)", lambda r,s: str(farey.farey_polynomial(r,s,*parabolic_traces)).replace("**","^") )

elliptic_traces = riley.traces_from_holonomies(mp.pi/7,mp.pi/2)
build_tex_table("The Farey polynomials (p = 7, q = 2)", lambda r,s: str(farey.farey_polynomial(r,s,*elliptic_traces)).replace("**","^") )
