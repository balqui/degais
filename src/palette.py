'''

El desajuste está viniendo de que intento que los cortes marquen
diferencia entre x < cut y cut <= x pero, sin embargo, en el caso
default sin -a quiero que el índice 0 sea para x == 0. Y lo estoy
intentando hacer con un cut en 0 pero, claro, ahora nada funciona.


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
# ~ from bisect import bisect_left # DOUBLE-CHECK THAT I WANT THIS EXACTLY
# ~ from bisect import bisect_left as bisect # DOUBLE-CHECK THAT I WANT THIS EXACTLY
from bisect import bisect # DOUBLE-CHECK THAT I WANT THIS EXACTLY
import graphviz as gvz # NOT the official bindings!

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
    NB: the cut sequence does NOT include the extreme points.
    '''

    def __init__(self, labels, coloring, param, alledges):
        '''
        we need the frequency labels of all edges
        caveat: make double sure all defaults are positive
        '''

        print(" *** Labels:", labels)

        default = { 'thresh': labels[0] + 1,                # PENDING
                    'expwidth': eguess(labels[-1], labels[0]), 
                    'linwidth': lguess(labels[-1], labels[0]), 
                    'binary': 1, 'ident': 1 } # last two irrelevant
        try:
            "tried to detect wrong colorings below but too late, they raise KeyError here"
            param = default[coloring] if param is None else float(param) 
            if coloring.endswith('width') and param <= 0:
                raise ValueError
            if coloring != 'expwidth':
                param = int(param)
        except ValueError:
            "comes from either float(param) or a nonpositive value"
            print(" * Disallowed value " + param + " for " + coloring + '.')
            exit()

        self.coloring = coloring
        self.param = param
        self.alledges = alledges

        self.usedcolorindices = set()

        self.the_colors = ( # original color sequence by Ely Piceno,
                            # except transparent instead of white
                        'transparent', 'black', 'blue', 'blueviolet',
                        'brown', 'burlywood', 'cadetblue', 
                        'chartreuse', 'coral', 'crimson', 'cyan',
                        'darkorange', 'deeppink', 'deepskyblue', 
                        'forestgreen', 'gold', 'greenyellow',
                        'hotpink', 'orangered', 'pink', 'red',
                        'seagreen', 'yellow') 


# TEMPORARY SOLUTION WITH CUTPOINTS AT .5 
# WHICH WILL NOT WORK WELL FOR THE LEGEND 
# BUT AT LEAST MAKE SURE THINGS START WORKING.
# AS OF TODAY, INCLUDES ARTIFICIAL EXTREMES.

        self.cuts = [ -0.5 ]

        if coloring == 'ident':
            "color: bisect - int(not alledges)"
            if len(labels) > len(self.the_colors) - int(self.alledges):
                print(" * Sorry. Too many classes", 
                      "not enough colors.")
                exit()
            self.cuts.extend(x + 0.5 for x in labels)
            self.ident = True
        elif coloring == 'thresh':
            "NOT COMPLETE YET"
            self.cuts.append(param)
        elif coloring == 'linwidth':
            c = param if self.alledges else 0.5
            while c <= labels[-1]:
                self.cuts.append(c)
                c += param
            self.cuts.append(c)
        elif coloring == 'expwidth':
            if not self.alledges:
                "first interval contains just zero and will be transparent"
                self.cuts.append(0.5)
            c = param
            while c <= labels[-1]:
                self.cuts.append(c)
                c *= param
        elif coloring == 'binary':
            self.cuts = [1]
            self.alledges = False # override --alledges if it was present
        else:
            print(" * Color scheme", coloring, "unknown.")
            exit() 



# EARLIER SOLUTION TO FISH BACK IN SOME PARTS:

        # ~ if not self.alledges:
            # ~ "first interval contains just zero, 0:1, and will be transparent"
            # ~ self.cuts = [0]
        # ~ else:
            # ~ "init cutpoints, don't handle zero separately"
            # ~ self.cuts = list()

        # ~ if coloring == 'ident':
            # ~ if len(labels) > len(self.the_colors) - int(self.alledges):
                # ~ print(" * Sorry. Too many class numbers", 
                      # ~ "not enough colors.")
                # ~ exit()
            # ~ self.cuts += labels
            # ~ self.ident = True
        # ~ elif coloring == 'thresh':
            # ~ self.cuts.append(param)
        # ~ elif coloring == 'linwidth':
            # ~ c = param
            # ~ while c <= labels[-1]:
                # ~ self.cuts.append(c)
                # ~ c += param
        # ~ elif coloring == 'expwidth':
            # ~ c = param
            # ~ while c <= labels[-1]:
                # ~ self.cuts.append(c)
                # ~ c *= param
        # ~ elif coloring == 'binary':
            # ~ self.cuts = [1]
            # ~ self.alledges = False # override --alledges if it was present
        # ~ else:
            # ~ print(" * Color scheme", coloring, "unknown.")
            # ~ exit() 

    def test(self, label, index):
        "Redundancy test before removing the functions"
        if not self.alledges:
            "o/w they are off by 1, I believe now"
            print(" * Index for label " + str(label) 
                  + " in " + self.coloring + " with " + str(self.param) 
                  + ': ' + str(index) 
                  + '; check: ' + str(index == eval(self.coloring)(self.param, label)) + '.' )            

    def color(self, label):
        "if alledges, need to avoid index 0 so as to avoid flattening"
        index = bisect(self.cuts, label) - 1 + int(self.alledges)
        print(" *** Cuts:", self.cuts)
        print(" *** (", self.coloring, self.param, ")", label, index)
        self.test(label, index)
        self.usedcolorindices.add(index)
        return index

# add make_legend which takes the color from self.the_colors
# and the intervals from consecutive pairs in self.cuts

    def _legend_item(self, legend_line, color_index):
        if self.coloring == 'ident':
            "caveat: single-value label to be extended to some other cases"
            print(" ***** Coloring ident in _legend_item",
                "color_index", color_index, "for", self.cuts)
            label = str(self.cuts[color_index])
        else:
            print(" ***** Coloring in _legend_item:", self.coloring, 
                "color_index", color_index, "for", self.cuts)
            label = str(self.cuts[color_index]) + ' - '
            if color_index < len(self.cuts) - 1:
                label += str(self.cuts[color_index + 1] - 1)
        color = self.the_colors[color_index + int(self.alledges)]
        legend_line.node("sgL" + str(color), shape = "none", label = '')
        legend_line.node("sgR" + str(color), shape = "none", label = label)
        legend_line.edge("sgL" + str(color), "sgR" + str(color), 
            color = color, arrowhead = "none", penwidth = "2.5" )
        return "sgL" + str(color)

    def make_legend(self):
        if self.coloring == 'binary':
            "no legend necessary"
            return
        leg_gr = gvz.Digraph(graph_attr = { "compound": "true", 
            "newrank": "true", "ranksep" : "0.1", "labeljust" : "l",
            "fontname" : "Courier New" })
        prev = None
        for color_index in sorted(self.usedcolorindices):
            with leg_gr.subgraph(graph_attr = { "rank" : "same" }) as sg:
                sg_n = self._legend_item(sg, color_index)
            if prev is not None:
                leg_gr.edge(prev, sg_n, color = 'transparent')
            prev = sg_n
        leg_gr.render(view = True)
