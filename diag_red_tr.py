def filt(item, addinf = False, cond = False, proc = False):
    if not item: return item
    if item == '1': return 'M' if addinf else ''
    if item == '2': return 'F' if addinf else ''    
    if item.startswith('V'): return item if cond else ''
    if item[0].isalpha(): return item if addinf else ''
    if len(item.split('.')[0]) < 3: return item if proc else ''
    return item

def nosp(s):
    return '_'.join(s.split())

# ~ fnm = "diagnostic_80.txt"
fnm = "Hosp_red"
with open(fnm + ".csv") as f:
    f.readline() # skip headers
    with open(fnm + ".td", "w") as g:
        for line in f:
            linlist = list()
            for d in line.strip().split(','):
                dd = filt(d)
                if dd:
                    linlist.append(nosp(dd))
            print(' '.join(linlist), file = g)

            # ~ if len(linlist) > 1:
