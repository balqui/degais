'''
Binning functions to reduce the quantity of labels in a 
Gaifman structure as labeling with frequencies may be
too rigid.
'''
from math import floor, log

ident = lambda _, x: x

# binary binning labels 0/1 give, essentially, a standard Gaifman graph
binary = lambda _, x: int(x > 0)

# binning with linear intervals
linwidth = lambda w, x: x // w # w width of regular intervals

# binning with exponentially growing intervals
expwidth = lambda b, x: floor(log(x + 1, b)) # +1 to handle zero

# binary binning labels for thresholded Gaifman graph:
thresh = lambda thr, x: int(x >= thr)

