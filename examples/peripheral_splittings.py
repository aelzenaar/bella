""" Produce an interesting file to send to Jeroen
"""
from bella import farey
import pandas as pd

def generator(max_denom = 300):
    last_denom = 0
    for r,s in farey.walk_tree_bfs(max_denom):
        if s > last_denom:
            print(f"{s}/{max_denom}")
            last_denom+=1
        splittings = farey.peripheral_splittings(farey.farey_word(r,s))
        yield (r, s, ''.join(splittings[0][0]),''.join(splittings[0][1]),''.join(splittings[1][0]),''.join(splittings[1][1]))


df = pd.DataFrame.from_records(generator(), columns=['r','s','u1','v1','u2','v2'])
df.to_csv('peripheral_splittings.csv')
