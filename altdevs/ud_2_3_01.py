'''
Explore discretization in 2 or 3 bins again.
This time, cutpoints are at +/- eps of data
points, except first -eps and last +eps which
are always fixed.
'''

from itertools import chain, pairwise
from functools import cache
from collections import Counter
from math import comb, log
from random import gauss

DEFAULTSIZE = 50
VLOW = float('-inf')

def initreg(n):
    "fails for n = 1030 at i = 500, int too large to become float"
    reg = [0, 1]
    reg.append( sum( comb(n, i) * (i/n)**i * ((n-i)/n)**(n-i) for i in range(n+1) ) )
    for k3 in range(5):
        "complete up to 7 values, k3 is k-3 actually"
        reg.append(reg[-1] + (n/(k3+1)*reg[-2]))
    return reg

@cache
def intsum(md, b, e):
    return sum(md[b:e])

def ev_int(candcuts, md, beg, end, lim):
    '''
    VLOW value for empty intervals, now possible
    start adding up at (beg+1)//2 incl
    stop  adding up at (end+1)//2 excl
    '''
    int_total = intsum(md, (beg+1)//2, (end+1)//2)
    if int_total == 0:
        return VLOW
    total = intsum(md, 0, lim) # JUST STARTING TO HAVE SERIOUS DOUBTS ABOUT THIS VALUE
    int_len = candcuts[end] - candcuts[beg]
    # ~ return int_total * log( int_total/(total*int_len) )
    return int_total * log( eps*int_total/(total*int_len) )

def ev_cut(candcuts, md, lim, cut):
    "VLOW absorbs addition with finite values or with VLOW"
    return ev_int(candcuts, md, 0, cut, lim) + \
           ev_int(candcuts, md, cut, lim, lim)

def ocut(candcuts, md, lim):
    '''
    best cost for a cut into md[0:cut] and md[cut:lim]
    cut in range(1, lim-1), 3 <= lim < len(candcuts)
    '''
    # ~ oc = 1
    # ~ print("cut", oc, candcuts[oc])
    # ~ mx = ev_cut(candcuts, md, lim, oc)
    mx = VLOW
    for cut in range(1, lim):
        # ~ print("cut", cut, candcuts[cut], "->", end = ' ')
        m = ev_cut(candcuts, md, lim, cut)
        # ~ print(m)
        if m > mx:
            # ~ print("new best", cut, m)
            mx = m
            oc = cut
    return mx, oc

# ~ nn = input("n? ")
# ~ try:
    # ~ n = int(nn)
    # ~ if n == 0:
        # ~ raise ValueError
    # ~ print("n =", n)
# ~ except ValueError:
    # ~ "coming from either a zero or a non-int string"
    # ~ print(f"n = {DEFAULTSIZE}")
    # ~ n = DEFAULTSIZE

# ~ d = list()
# ~ for _ in range(n):
    # ~ d.append(gauss(0, 1))
# ~ for _ in range(n//2):
    # ~ d.append(gauss(0, 1))
# ~ for _ in range(n - n//2):
    # ~ d.append(gauss(4, 1))

# ~ if n < 25:
    # ~ print("raw:", ' '.join(f"{dt:6.4f}" for dt in d))

# ~ print("logreg:",  ' '.join(f"{log(r):6.2f}" for r in reg[1:]))

# ~ d = sorted(d)

# Titanic edge multiplicities:
# ~ d = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 23, 24, 45, 52, 57, 64, 79, 106, 118, 122, 126, 145, 167, 178, 179, 180, 196, 203, 212, 261, 319, 344, 367, 425, 510, 528, 627, 654, 673, 862, 885, 1364, 1438, 1667]
# Titanic edge multiplicities w/o zeros:
d = [6, 23, 24, 45, 52, 57, 64, 79, 106, 118, 122, 126, 145, 167, 178, 179, 180, 196, 203, 212, 261, 319, 344, 367, 425, 510, 528, 627, 654, 673, 862, 885, 1364, 1438, 1667]

# to compute eps and candcuts we must collapse duplicates in d first
dd = Counter(d)
ud = sorted(dd) # data without duplicates
md = tuple( dd[a] for a in ud ) # data multiplicities in same order as ud
                                # immutable so that ev_int can be cached

# ~ print("Multiplicities", list(zip(ud, md)))

# minimum difference of consecutive, different values
mindiff = min(b - a for a, b in pairwise(ud))

# 0.1 fraction of minimum empirical separation
eps = mindiff/10 

# candcuts[0] and candcuts[-1] always belong to the cut sequence
candcuts = tuple(chain.from_iterable([a - eps, a + eps] for a in ud))

# a = ud[i] iff candcuts[2*i] = a - eps and candcuts[2*i+1] = a + eps
# hence md[i] data points between candcuts[2*i] and candcuts[2*i+1]
# ~ for i, a in enumerate(d):
    # ~ print(a - eps, candcuts[2*i])
    # ~ print(a + eps, candcuts[2*i+1])

# ~ if n < 25:
    # ~ print("data:", ' '.join(f"{dt:6.2f}" for dt in d))
    # ~ print("diff:", ' '.join(f"{d[i+1]-d[i]:6.2f}" for i in range(len(d)-1)))

reg = initreg(len(ud))

spl2loglik = list()
spl2optcut = list()

# ~ print("candcuts", candcuts)
print("len candcuts", len(candcuts), "at 39:", candcuts[39], '\n    ',
      "log comb 1", log(1/(len(candcuts)-2)),  '\n    ',
      "log comb 2", log(1/comb(len(candcuts)-2, 2)))

# 2 intervals below 3 forces empty intervals
for lim in range(3, len(candcuts)):
    "best cost for a cut below and up to lim-1"
    # ~ print("2 intervals up to", lim)
    ll, oc = ocut(candcuts, md, lim)
    # ~ print("best", oc, ll)
    spl2loglik.append(ll)
    spl2optcut.append(oc)

print( "Cut into 2 at", oc, "loglik", ll, "total", ll - log(reg[2]), "with log", ll - log(reg[2]) - log(len(candcuts)-2))

# ~ spl2loglik[0]: val of best cut up to lim 3
# ~ for ggg in enumerate(spl2loglik): print(ggg)

mx = VLOW

# 3 intervals below 4 implies empty intervals
for c in range(4, len(candcuts)):
    "best cost for a cut into opt cut in 2 of d[0:cut] and d[cut:lim]"
    # ~ print("2 intervals up to", c, "plus 3rd one, val:", end = '')
    m = spl2loglik[c-3] + ev_int(candcuts, md, c, len(candcuts) - 1, len(candcuts))
    # ~ print(m)
    if m > mx:
        # ~ print("new best", c, m)
        mx, o1c, o2c = m, spl2optcut[c-3], c

print( "Cut into 3 at", o1c, o2c, "loglik", mx, "total", mx - log(reg[3]), "with log", mx - log(reg[3]) - log(comb(len(candcuts)-2, 2)))

