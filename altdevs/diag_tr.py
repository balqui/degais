fnm = "diagnostic_100"
# ~ fnm = "diagnostic_80"
with open(fnm + ".txt") as f:
    _ = f.readline() # discard headers
    with open(fnm + ".td", "w") as g:
        for line in f:
            linlist = [ d for d in line.strip().split(',') if d ]
            # ~ if len(linlist) > 1:
            if True:
                print(' '.join(linlist), file = g)
