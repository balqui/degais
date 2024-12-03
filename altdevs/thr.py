'''
Author: Jose Luis Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Assorted, auxiliary functions.
'''

from itertools import chain, pairwise
# ~ from itertools import combinations as comb
from math import log, floor # , ceil, log
from functools import cache
from collections import Counter

VLOW = float('-inf')

# ==== Experimentation for the 2-split default in thresh

@cache
def _intsum(md, b, e):
    return sum(md[b:e])

def _ev_int(candcuts, md, beg, end, lim, eps): 
    '''
    VLOW value for empty intervals, now possible
    For candcuts at +/- eps:
	    start adding up at (beg+1)//2 incl
	    stop  adding up at (end+1)//2 excl
    '''
    # ~ good for candcuts at +/- eps
    # ~ int_total = _intsum(md, (beg+1)//2, (end+1)//2)
    # ~ good for candcuts at midpoints
    int_total = _intsum(md, beg, end)
    if int_total == 0:
        return VLOW
    total = _intsum(md, 0, lim)
    int_len = candcuts[end] - candcuts[beg]
    print(" *** ev int_", beg, end, "int_total:", int_total, 
          "total:", total, "int_len:", int_len, "quotient:",
          int_total/(total*int_len))
    return int_total * log( eps*int_total/(total*int_len) )

def _ev_cut(candcuts, md, lim, cut, eps):
    "VLOW absorbs addition with finite values or with VLOW"
    return _ev_int(candcuts, md, 0, cut, lim, eps) + \
           _ev_int(candcuts, md, cut, lim, lim, eps)

def _ocut(candcuts, md, lim, eps):
    '''
    best cost for a cut into md[0:cut] and md[cut:lim]
    cut in range(1, lim-1), 3 <= lim < len(candcuts)
    '''
    mx = VLOW
    for cut in range(1, lim):
        print("cut", cut, candcuts[cut]) # , "->", end = ' ')
        m = _ev_cut(candcuts, md, lim, cut, eps)
        print(m)
        if m > mx:
            print("new best", cut, m)
            mx = m
            oc = cut
    return mx, oc

def thr_1(labels):
    assert len(labels) > 1, "Threshold with only one label should not happen."
    dd = Counter(labels)
    ud = sorted(dd) # data without duplicates
    md = tuple( dd[a] for a in ud ) # data multiplicities in same order as ud
                                    # immutable so that ev_int can be cached
    # minimum difference of consecutive, different values
    mindiff = min(b - a for a, b in pairwise(ud))
    # 0.1 fraction of minimum empirical separation
    eps = mindiff/10 
    # candcuts[0] and candcuts[-1] always belong to the cut sequence
    # case of just points +/- eps
    # ~ candcuts = tuple(chain.from_iterable([a - eps, a + eps] for a in ud))
    # case of midpoints
    candcuts = tuple( (a+b)/2 for a, b in pairwise([ud[0] - 1] + ud + [ud[-1] + 1]))
    print(" ******* ", candcuts)
    ll, oc = _ocut(candcuts, md, len(candcuts) - 1, eps)
    print(" *** Threshold loglik, cut, label", ll, oc, candcuts[oc], floor(candcuts[oc]))
    return floor(candcuts[oc])

if __name__ == "__main__":
    sfdata = [ 1, 2, 4, 5.5, 8, 10 ]
    print(thr_1(sfdata))
