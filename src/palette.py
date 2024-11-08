'''
Author: Jose Luis Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Palette of colors for Gaifman structures under various binning schemes.

Binning functions to reduce the quantity of labels in a 
Gaifman structure as labeling with frequencies may be
too rigid.

Plan is to:
- create it taking into account the CLI parameters, including the
  newly planned one of making transparent correspond only to zero
  multiplicities with an on/off switch
- offer from here a coloring method to color the EZGraph
- this coloring is to be in the range of the number of available colors
- that method must also register which values are actually employed
- so as to offer also the drawing of the color legend only with actually
  employed colors and corresponding values or intervals
- compute a default cut if coloring is thresh and no param is
  specified, by applying Kontkanen-Myllymaeki before or after taking
  the zeros out as required
'''


from math import floor, ceil, log

# ident: keeps multiplicities as labels
# binary: labels 0/1 give, essentially, a standard Gaifman graph
# thresh: thresholded Gaifman graph, threshold given as param
# linwidth: linear Gaifman graph, interval width given as param,
#   default value provided by lguess
# expwidth: exponential Gaifman graph, base given as param,
#   default value provided by eguess

ident = lambda _, x: x

# binary binning labels 0/1 give, essentially, a standard Gaifman graph
binary = lambda _, x: int(x > 0)

# binary binning labels for thresholded Gaifman graph
thresh = lambda thr, x: int(x >= thr)

# binning with linear intervals
linwidth = lambda w, x: x // int(w) # w width of regular intervals
# int needed because -p value in command line is now a float
# task of ensuring denominator is not null falls upon the caller

# binning with exponentially growing intervals
expwidth = lambda b, x: 0 if x < b else floor(log(x, b))
# zero (and potential negatives) flattened up to const 0

# JLB guess of default width for linwidth coloring
lguess = lambda mx, mn: ceil( (mx - mn)/4 )

# JLB guess of default base for expwidth coloring
eguess = lambda mx, mn: ceil( (mx/max(1,mn)) ** (1/3) )
