'''
Author: Jose Luis Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Assorted, auxiliary little functions.

Note found in earlier versions:
  In delbl we should keep alphabetic versions of digits.
(I don't understand it anymore.)
'''

def delbl(lbl):
	'''reduce lbl to only alnum chars, capitalized initial if alpha'''
	return ''.join( c for c in lbl if c.isalnum() ).capitalize()

def q(s):
    'quote string s'
    return '"' + s + '"'

