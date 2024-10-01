from ezGraph import EZGraph
from clans import Clan
from dectree import DecTree
from td2dot import read_graph_in
from collections import defaultdict as ddict
from itertools import combinations

# Handle the input
# ~ filename = "e4a" # binary: ok, ident: ok
# ~ filename = "e4b" # binary = ident: ok
# ~ filename = "e6" # binary: ok, ident: ok
# ~ filename = "e6a" # binary: ok, ident: ok
# ~ filename = "e7" # binary: ok, ident: ok
# ~ filename = "e7r" # binary: ok, ident: ok
# ~ filename = "e7alt" # binary: ok, ident: ok
# ~ filename = "e8a" # binary: ok, ident: ok
# ~ filename = "ex_dec_0" # ident: ok, binary: redecomp incomplete, unavailable
# ~ filename = "titanic_" # 
filename = "lenses" # 


def run(filename):
    fullfilename = filename + ".td"
    g = EZGraph(fullfilename)
    items = g.items
    dt = DecTree(g)
    root = dt.sgton(items[0])
    for it in items[1:]:
        item_cl = dt.sgton(it)
        root = root.add(item_cl, dt)
    return root, dt

import cProfile
cProfile.run('run(filename)')
# ~ dt.draw(root, filename)
