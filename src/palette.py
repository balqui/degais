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
from bisect import bisect_left # DOUBLE-CHECK THAT I WANT THIS EXACTLY

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



class Palette:
    '''
    Handles the colors both in the graph (as an index) and
    at drawing time; provides as well the legend, it needs
    the explicit cuts for this so that actually the functions
    above seem right now redundant as one can search fast 
    in the cut sequence.
    '''

    def __init__(self, labels, coloring, param, alledges):
        '''
        mn, mx from graph are smallest and largest 
        frequency labels of all edges
        '''

        default = { 'thresh': labels[0] + 1,                # PENDING
                    'expwidth': eguess(labels[-1], labels[0]), 
                    'linwidth': lguess(labels[-1], labels[0]), 
                    'binary': 1, 'ident': 1 } # last two irrelevant
        try:
            param = default[coloring] if param is None else float(param)
            if coloring.endswith('width') and param <= 0:
                raise ValueError
        except ValueError:
            "comes from either float(param) or a nonpositive value"
            print(" * Disallowed value " + param + " for " + coloring + '.')
            exit()

        self.zero = not alledges

        self.usedcolorindices = set()

        self.the_colors = ( # original color sequence by Ely,
                            # except transparent instead of white
                        'transparent', 'black', 'blue', 'blueviolet',
                        'brown', 'burlywood', 'cadetblue', 
                        'chartreuse', 'coral', 'crimson', 'cyan',
                        'darkorange', 'deeppink', 'deepskyblue', 
                        'forestgreen', 'gold', 'greenyellow',
                        'hotpink', 'orangered', 'pink', 'red',
                        'seagreen', 'yellow') 

        if self.zero:
            "first interval contains just zero, 0:1"
            self.cuts = [1]
        else:
            "init cutpoints, don't handle zero separately"
            self.cuts = list()
        if coloring == 'binary':
            self.cuts = [1, labels[-1]]
        elif coloring == 'ident':
            if len(labels) > len(self.the_colors):
                print(" * Sorry. Too many class numbers", 
                      "not enough colors.")
                exit()
            self.cuts = labels
        elif coloring == 'thresh':
            self.cuts.extend([param, labels[-1]])
        elif coloring == 'linwidth':
            c = param
            while c <= labels[-1]:
                self.cuts.append(c)
                c += param
        elif coloring == 'expwidth':
            c = param
            while c <= labels[-1]:
                self.cuts.append(c)
                c *= param

    def color(self, label):
        index = eval(coloring)(param, label)
        if index != bisect_left(self.cuts, label):
            print(" * Bad index for label " + str(label) + 
                  " in " + coloring + " with " + param + ': ' +
                  str(index) + ' ' + str(bisect_left(self.cuts, label)) + '.' )            
        self.usedcolorindices.add(index)
        return index

# add make_legend which takes the color from self.the_colors
# and the intervals from consecutive pairs in self.cuts


