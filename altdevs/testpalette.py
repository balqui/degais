'''
Author: Jose Luis Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Original programming of the the various binning schemes used
earlier, before storing explicitly the cuts.
'''


from math import floor, ceil, log
from bisect import bisect_left as bs # specific variant of binary search

# ident: keeps multiplicities as labels
# binary: labels 0/1 give, essentially, a standard Gaifman graph
# thresh: thresholded Gaifman graph, threshold given as param
# linwidth: linear Gaifman graph, interval width given as param,
#   default value provided by lguess
# expwidth: exponential Gaifman graph, base given as param,
#   default value provided by eguess

# ALL THESE FUNCTIONS TO BE REMOVED WHEN TESTING IS SUFFICIENT
ident = lambda _, x: x

# binary binning labels 0/1 give, essentially, a standard Gaifman graph
binary = lambda _, x: int(x > 0)

# binary binning labels for thresholded Gaifman graph
thresh = lambda thr, x: int(x > thr)

# binning with linear intervals
# ~ linwidth = lambda w, x: x // int(w) # w width of regular intervals
linwidth = lambda w, x: ceil(x / int(w)) # w width of regular intervals
# int needed because -p value in command line is now a float
# task of ensuring denominator is not null falls upon the caller

# binning with exponentially growing intervals
expwidth = lambda b, x: 0 if x <= b else floor(log(x, b))
# zero (and potential negatives) flattened up to const 0

# ~ def test(label, index, palette):
	# ~ "Redundant test of the colors, are they are off by 1? depends on -k?"
	# ~ print(" *** Test; -k:", palette.complete)
	# ~ print(" *** Index for label " + str(label) 
		  # ~ + " in " + palette.coloring + " with " + str(palette.param) 
		  # ~ + ': ' + str(index) + ' ' + str(eval(palette.coloring)(palette.param, label))
		  # ~ + '; check: ' + str(index == eval(palette.coloring)(palette.param, label)) + '.' )            

def test(value, palette):
	"Redundant test of the colors, obsolete"
	print(" *** Test " + str(value) + ' ' 
	      + str(eval(palette.coloring)(palette.param, value)) + ' ' 
	      + str(bs(palette.cuts, value)) )
