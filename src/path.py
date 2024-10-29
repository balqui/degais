from collections import defaultdict as ddict
from auxfun import comb
from ezGraph import EZGraph
from clans import Clan

def path(cl, dt):
    print(" ... ", cl, len(cl))
    count = 0
    seencol = 0
    neigh = ddict(list)
    for cl_a, cl_b in comb(cl, 2):
        col = dt.how_seen(cl_a, cl_b)
        if col > 0:
            count += 1
            if seencol == 0:
                seencol = col
            elif col != seencol:
                "not a single-color path if path at all"
                return False
            neigh[cl_a.name].append(cl_b.name)
            neigh[cl_b.name].append(cl_a.name)
    if count != len(cl) - 1:
        "not a path, wrong number of edges"
        return False
    for scl in neigh:
        if len(neigh[scl]) > 2:
            "not a path, vertex of degree higher than 2"
            return False
    # attempt at constructing path
    curr = None
    for scl in neigh:
        "start with some vertex of deg 1"
        if len(neigh[scl]) == 1:
            curr = scl
            break
    if curr is None:
        "not a path, no vertex of degree 1"
        return False
    attempting = True
    attempt = list()
    attempt.append(dt[curr])
    nxt = neigh[curr][0] # uniquely defined here
    while len(neigh[nxt]) == 2:
        "keep constructing path"
        for scl in neigh[nxt]:
            if scl != curr:
                curr = nxt
                attempt.append(dt[curr])
                nxt = scl
                break
    attempt.append(dt[nxt])
    if len(attempt) < len(cl):
        "path too short"
        return False
    else:
        "path found"
        return Clan(cl.name, attempt, cl.color) # color marks primitive

if __name__ == "__main__":
    from dectree_path import DecTree
    sbin = lambda x: int(x > 0)
    g = EZGraph("e4ccc.td")
    g.recolor(sbin)
    dt = DecTree(g)
    root = dt.sgton(g.items[0])
    for it in g.items[1:]:
        item_cl = dt.sgton(it)
        root = root.add(item_cl, dt)
    for cl_nm in dt:
        pth = path(dt[cl_nm], dt)
        if pth:
            "replace it"
            dt[cl_nm] = pth
            print(" ... replaced", pth)
    dt.draw(root, "e4ccc_path")
    
