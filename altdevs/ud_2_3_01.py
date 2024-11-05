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
    CAVEAT: still to figure out a value for empty intervals, 
            (now possible) and see whether that is what happens now
    beg even: start adding up at beg//2 o/w at (beg+1)//2 incl
    end even: stop  adding up at end//2 o/w at (end+1)//2 excl
    start adding up at (beg+1)//2 incl
    stop  adding up at (end+1)//2 excl
    '''
    print("Evaluate", beg, end, lim, candcuts[beg], candcuts[end])
    total = intsum(md, 0, lim)
    int_total = intsum(md, (beg+1)//2, (end+1)//2)
    print("   int_total:", int_total)
    int_len = candcuts[end] - candcuts[beg]
    return int_total * log( int_total/(total*int_len) )

def ev_cut(candcuts, md, lim, cut):
    return ev_int(candcuts, md, 0, cut, lim) + \
           ev_int(candcuts, md, cut, lim, lim)

def ocut(candcuts, md, lim):
    '''
    best cost for a cut into md[0:cut] and md[cut:lim]
    cut in range(1, lim-1), 3 <= lim < len(candcuts)
    '''
    print("cuts up to", lim)
    oc = 1
    print("cut", oc, candcuts[oc])
    mx = ev_cut(candcuts, md, lim, oc)
    for cut in range(2, lim):
        print("cut", cut, candcuts[cut])
        m = ev_cut(candcuts, md, lim, cut)
        print(m)
        if m > mx:
            print("new best", cut, m)
            mx = m
            oc = cut
    return mx, oc

nn = input("n? ")
try:
    n = int(nn)
    if n == 0:
        raise ValueError
    print("n =", n)
except ValueError:
    "coming from either a zero or a non-int string"
    print(f"n = {DEFAULTSIZE}")
    n = DEFAULTSIZE

d = list()
for _ in range(n):
    d.append(gauss(0, 1))
# ~ for _ in range(n//2):
    # ~ d.append(gauss(0, 1))
# ~ for _ in range(n - n//2):
    # ~ d.append(gauss(4, 1))

if n < 25:
    print("raw:", ' '.join(f"{dt:6.2f}" for dt in d))

# ~ print("logreg:",  ' '.join(f"{log(r):6.2f}" for r in reg[1:]))

# to test candcuts
# ~ d = list(range(4))
# ~ d.extend(range(3))

# ~ d = sorted(d)

# to compute eps and candcuts we must collapse duplicates in d first
dd = Counter(d)
ud = sorted(dd) # data without duplicates
md = tuple( dd[a] for a in ud ) # data multiplicities in same order as ud
                                # immutable so that ev_int can be cached

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

reg = initreg(n)

spl2loglik = list()
spl2optcut = list()

print("candcuts", candcuts)

# lim below 3 forces empty intervals
for lim in range(3, len(candcuts)):
    "best cost for a cut below and up to lim-1"
    ll, oc = ocut(candcuts, md, lim)
    spl2loglik.append(ll)
    spl2optcut.append(oc)

print( "Cut into 2 at", oc, "loglik", ll, "total", ll - log(reg[2]) )

exit()

mx = spl2loglik[0] + ev_int(candcuts, md, 3, n, n)
o1c = 1
o2c = 2
for c in range(3, n-1):
    "best cost for a cut into opt cut in 2 of d[0:cut] and d[cut:lim]"
    m = spl2loglik[c-2] + evhalf(d, c+1, n)
    if m > mx:
        mx, o1c, o2c = m, spl2optcut[c-2], c

print( "Cut into 3 at", o1c, "and", o2c, "loglik", mx, "total", mx - log(reg[3]) )

