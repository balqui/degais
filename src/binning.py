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

# binary binning labels for a thresholded Gaifman graph and effect on Titanic:
# ~ def t(x):
    # ~ if x < 23: return 0 # just forgets about the 6 children in 1st class
    # ~ return 1
# ~ def t(x):
    # ~ if x < 212: return 0 # there is a bend there hitting some exp-like
    # ~ return 1
    # marks that few children overall, and that few people in 1st and 2nd class
# ~ def t(x):
    # ~ if x < 1000: return 0 # displays the Birkenhead Drill
    # ~ return 1
# ~ def t(x):
    # ~ if x < 200: return 0 # exploring cmc, 10% is 147
    # ~ return 1
