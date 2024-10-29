from auxfun import comb

def path(cl, dt):
    seencol = 0
    lodeg = ddict(int)
    for cl_a, cl_b in comb(cl, 2):
        col = dt.how_seen(cl_a, cl_b)
        if col > 0:
            if seencol == 0:
                seencol = col
            elif col != seencol:
                return False
            lodeg[cl_a] += 1
            lodeg[cl_b] += 1
    dg1 = list( cl for cl in lodeg if lodeg[cl] == 2 )

