'''
Explore discretization in 2 or 3 bins.
'''

from math import comb, log
from random import gauss

eps = 0.1

def initreg(n):
    reg = [0, 1]
    reg.append( sum( comb(n, i) * (i/n)**i * ((n-i)/n)**(n-i) for i in range(n+1) ) )
    for k3 in range(5):
        "complete up to 7 values, k3 is k-3 actually"
        reg.append(reg[-1] + (n/(k3+1)*reg[-2]))
    return reg

def intlen(d, beg, end):
    "length of left interval up to cut"
    return d[end-1] - d[beg] + 2*eps

def evhalf(d, beg, end):
    return (end-beg)*log((end-beg)/(lim*intlen(d, beg, end)))

def ev(d, lim, cut):
    return evhalf(d, 0, cut) + evhalf(d, cut, lim)

def ocut(d, lim):
    oc = 1
    mx = ev(d, lim, oc)
    for cut in range(2, lim):
        m = ev(d, lim, cut)
        if m > mx:
            mx = m
            oc = cut
    return mx, oc

nn = input("n? ")
try:
    n = int(nn)
    print("n =", n)
except ValueError:
    print("n = 50")
    n = 50

reg = initreg(n)

d = list()
for _ in range(n):
    d.append(gauss(0, 1))
d = sorted(d)

print("logreg:",  ' '.join(f"{log(r):6.2f}" for r in reg[1:]))
if n < 25:
    print("data:", ' '.join(f"{dt:6.2f}" for dt in d))

spl2loglik = list()
spl2optcut = list()

for lim in range(2, n):
    "best cost for a cut into d[0:cut] and d[cut:lim], cut in range(1, lim-1)"
    ll, oc = ocut(d, lim)
    spl2loglik.append(ll) # pos lim-2
    spl2optcut.append(oc)

print( "Cut into 2 at", oc, "loglik", ll, "total", ll - log(reg[2]) )

mx = spl2loglik[0] + evhalf(d, 3, n)
o1c = 1
o2c = 2
for c in range(3, n-1):
    "best cost for a cut into opt cut in 2 of d[0:cut] and d[cut:lim]"
    m = spl2loglik[c-2] + evhalf(d, c+1, n)
    if m > mx:
        mx, o1c, o2c = m, spl2optcut[c-2], c

print( "Cut into 3 at", o1c, "and", o2c, "loglik", mx, "total", mx - log(reg[3]) )

