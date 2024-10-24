with open("diagnostic_80.txt") as f:
    with open("diagnostic_80.td", "w") as g:
        for line in f:
            linlist = [ d for d in line.strip().split(',') if d ]
            if len(linlist) > 1:
                print(' '.join(linlist), file = g)

