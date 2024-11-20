'''
Author: Jose Luis Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Assorted, auxiliary functions.
'''

from itertools import chain, pairwise
from itertools import combinations as comb
from math import floor, ceil, log
from functools import cache
from collections import Counter

VLOW = float('-inf')

# JLB guess of default width for linwidth coloring - OLD FORMAT
# lguess = lambda mx, mn: ceil( (mx - mn)/4 )
lguess = lambda labels: ceil( (labels[-1] - labels[0])/4 )

# JLB guess of default base for expwidth coloring - OLD FORMAT
# eguess = lambda mx, mn: ceil( (mx/max(1,mn)) ** (1/3) )
# ~ eguess = lambda labels: ceil( (labels[-1]/max(1,labels[0])) ** (1/3) )
eguess = lambda labels: round( (labels[-1]/max(0.9,labels[0])) ** (1/3), 4)

def delbl(lbl):
    '''
    reduce lbl to only alnum chars or dot, capitalized initial 
    if alpha, to be used as internal clan name
    '''
    return ''.join( c for c in lbl if c.isalnum() or c == '.' ).capitalize()

'quote string s'
q = lambda s: '"' + s + '"'

# ==== Ancillary functions for the 2-split for thr_1, default in thresh

@cache
def _intsum(md, b, e):
    return sum(md[b:e])

def _ev_int(candcuts, md, beg, end, lim, eps): 
    '''
    VLOW value for empty intervals, now possible
    start adding up at (beg+1)//2 incl
    stop  adding up at (end+1)//2 excl
    '''
    int_total = _intsum(md, (beg+1)//2, (end+1)//2)
    if int_total == 0:
        return VLOW
    total = _intsum(md, 0, lim)
    int_len = candcuts[end] - candcuts[beg]
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
        m = _ev_cut(candcuts, md, lim, cut, eps)
        if m > mx:
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
    candcuts = tuple(chain.from_iterable([a - eps, a + eps] for a in ud))
    ll, oc = _ocut(candcuts, md, len(candcuts) - 1, eps)
    return floor(candcuts[oc])
