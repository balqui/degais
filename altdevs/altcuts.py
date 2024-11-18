'''
Author: Jose Luis Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Ancillary functions for the 2-split for thr_1, default in thresh,
alternative formulation attempt.

UNABLE TO UNDERSTAND WHY IT WORKS THE WAY IT WORKS.
'''

from itertools import pairwise # chain, 
# ~ from itertools import combinations as comb
from math import floor, log #  ceil,
from functools import cache
from collections import Counter

VLOW = float('-inf')

@cache
def _intsum(md, b, e):
    return sum(md[b:e])

def _ev_int(candcuts, md, beg, end, lim): 
    int_total = _intsum(md, beg, end)
    if int_total == 0:
        "this should not happen anymore"
        print(" *** Empty interval evaluated", md, beg, end)
        return VLOW
    total = _intsum(md, 0, lim) # cached, not recomputed / is it lim+1?
    int_len = candcuts[end] - candcuts[beg]
    lik = (int_total/(total*int_len))**int_total
    print(" ***** Eval int", beg, end, lim, 
          "in_bin:", int_total, "bin_len:", int_len, "total", total,
          "raw_lik", lik)
    return lik
    # ~ return int_total * log( int_total/(total*int_len) )

def _ev_cut(candcuts, md, lim, cut):
    "VLOW absorbs addition with finite values or with VLOW"
    lft_lik = _ev_int(candcuts, md, 0, cut, lim)
    rgh_lik = _ev_int(candcuts, md, cut, lim, lim)
    loglik = log(lft_lik) + log(rgh_lik)
    print(" ***** Eval cut", cut, "to lim", lim, "lik", lft_lik*rgh_lik,
          "loglik", loglik)
    return loglik
    # ~ return _ev_int(candcuts, md, 0, cut, lim) + \
           # ~ _ev_int(candcuts, md, cut, lim, lim)

def _ocut(candcuts, md, lim):
    '''
    best cost for a cut into md[0:cut] and md[cut:lim] but note that
    candcuts[0] and candcuts[-1] are not really candidate cuts; 
    cut in range(1, lim-1), 2 <= lim < len(candcuts)
    '''
    mx = VLOW
    for cut in range(1, lim):
        m = _ev_cut(candcuts, md, lim, cut)
        print("cut", cut, candcuts[cut], "->", end = ' ')
        print(m)
        if m > mx:
            print("new best", cut, m)
            mx = m
            oc = cut
    return mx, oc

def thr_1_alt(labels):
    print("thr_1_alt", len(labels))
    assert len(labels) > 1, "No cut possible with less than 2 labels"
    dd = Counter(labels)
    ud = sorted(dd) # data without duplicates
    md = tuple( dd[a] for a in ud ) # data multiplicities in same order as ud
                                    # immutable so that ev_int can be cached
    # cutpoints are midpoints of consecutive, different values,
    # plus the first and last point, 
    # not real candidate cuts but handy for the evaluation
    candcuts = tuple( [ud[0]] + list((a+b)/2 for a, b in pairwise(ud)) + [ud[-1]] )
    ll, oc = _ocut(candcuts, md, len(candcuts) - 1)
    print(" *** ALT Threshold loglik, cut, label", ll, oc, candcuts[oc], floor(candcuts[oc]))
    return floor(candcuts[oc])

# BELIEVE IT OR NOT, ALL THESE CASES GET CUT AT 1.5 
d = [1, 2, 5, 6]
print(d, thr_1_alt(d))
d = [1, 2, 5, 7]
print(d, thr_1_alt(d))
d = [1, 2, 5, 8]
print(d, thr_1_alt(d))
d = [1, 2, 6, 8]
print(d, thr_1_alt(d))
d = [1, 2, 6, 9]
print(d, thr_1_alt(d))
d = [1, 2, 4, 8]
print(d, thr_1_alt(d))
