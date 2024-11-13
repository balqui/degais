'''
Author: Jose Luis Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Assorted, auxiliary little functions needed by several modules.
'''

from itertools import combinations as comb

# JLB guess of default width for linwidth coloring
lguess = lambda mx, mn: ceil( (mx - mn)/4 )

# JLB guess of default base for expwidth coloring
eguess = lambda mx, mn: ceil( (mx/max(1,mn)) ** (1/3) )

def delbl(lbl):
    '''
    reduce lbl to only alnum chars or dot, capitalized initial 
    if alpha, to be used as internal clan name
    '''
    return ''.join( c for c in lbl if c.isalnum() or c == '.' ).capitalize()

'quote string s'
q = lambda s: '"' + s + '"'

