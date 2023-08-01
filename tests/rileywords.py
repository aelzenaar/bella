from bella import farey

def test(r,s):
    rw = farey.riley_word(r,s)
    fw1 = ''.join(farey.farey_word(r,s))
    fw2 = ''.join([c.swapcase() for c in reversed(rw)] + ['Y'] + rw + ['X'])
    if fw1 != fw2:
      print(f'{r}/{s}\t',fw1==fw2, '\t', fw1[s-1], fw1, '\t', ''.join([c.swapcase() for c in reversed(rw)] + [' Y '] + rw + [' X']))

for r,s in farey.walk_tree_bfs(10):
    test(r,s)
