'''
Author: Jose Luis Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Assorted, auxiliary little functions needed by several modules.
'''

def delbl(lbl):
    '''
    reduce lbl to only alnum chars or dot, capitalized initial 
    if alpha, to be used as internal clan name
    '''
    return ''.join( c for c in lbl if c.isalnum() or c == '.' ).capitalize()

def q(s):
    'quote string s'
    return '"' + s + '"'
