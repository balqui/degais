'''



Author: Jose Luis Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Palette of colors for Gaifman structures under various binning schemes.

Cuts in list mark difference between x <= cut and cut < x
(doing it the other way raises incompatibilities with zero
and the -k option). A temporary solution with cuts at .5 and
exploring different binary search schemes did not provide the 
desired behavior.

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
from bisect import bisect_left as bs # specific variant of binary search
import graphviz as gvz               # NOT the official bindings!

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

    def __init__(self, labels, coloring, param, complete):
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
            if coloring not in default:
                print(" * Sorry. Unknown coloring scheme " + coloring + '. Exiting.')
                exit()
            param = default[coloring] if param is None else float(param) 
            if coloring.endswith('width') and param <= 0:
                raise ValueError
            if coloring != 'expwidth':
                param = int(param)
        except ValueError:
            "comes from either float(param) or a nonpositive value"
            print(" * Sorry. Disallowed value " + param + " for " + coloring + '. Exiting.')
            exit()

        self.coloring = coloring
        self.param = param
        self.complete = complete

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

        if not self.complete:
            "first interval contains just zero and will be transparent"
            self.cuts = [0]
        else:
            "init cutpoints, don't handle zero separately"
            self.cuts = list()

        if coloring == 'ident':
            "color: bisect - int(not complete)"
            if len(labels) > len(self.the_colors) - int(self.complete):
                print(" * Sorry. Too many classes, not enough colors. Exiting.")
                exit()
            self.cuts = labels # take out the zero as well
        elif coloring == 'thresh':
            self.cuts.append(param)
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
        else:
            "coloring == 'binary'"
            self.cuts = [1]
            self.complete = False # override --complete if it was present

        self.ecuts = ([-1] if self.complete else list()) + self.cuts + [labels[-1]]
        print(self.cuts)
        print(self.ecuts, '\n\n\n\n')
        # ~ exit()

    def test(self, label, index):
        "Redundancy test TO REVIEW AND ENSURE WHAT HAPPENS"
        pass
        # ~ if not self.complete:
            # ~ "o/w they are off by 1, I believe now"
            # ~ print(" * Index for label " + str(label) 
                  # ~ + " in " + self.coloring + " with " + str(self.param) 
                  # ~ + ': ' + str(index) 
                  # ~ + '; check: ' + str(index == eval(self.coloring)(self.param, label)) + '.' )            

    def color(self, label):
        "if complete, need to avoid index 0 so as to avoid flattening"
        index = bs(self.cuts, label) + int(self.complete)
        # ~ print(" *** Cuts:", self.cuts)
        # ~ print(" *** (", self.coloring, self.param, ")", label, index)
        self.test(label, index)
        self.usedcolorindices.add(index)
        return index

# add make_legend which takes the color from self.the_colors
# and the intervals from consecutive pairs in self.cuts

    def _legend_item(self, legend_line, color_index):
        if self.coloring == 'ident':
            print(" ***** Coloring ident in _legend_item",
                "color_index", color_index, "for", self.cuts)
            label = str(self.cuts[color_index - int(self.complete)])
        else:
            print(" ***** Coloring in _legend_item:", self.coloring, 
                "color_index", color_index, "for", self.ecuts)
            label = str(floor(self.ecuts[color_index - 1]) + 1) + ' - ' \
                  + str(floor(self.ecuts[color_index]))
        color = self.the_colors[color_index]
        legend_line.node("sgL" + str(color), shape = "none", label = '')
        legend_line.node("sgR" + str(color), shape = "none", label = label)
        legend_line.edge("sgL" + str(color), "sgR" + str(color), 
            color = color, arrowhead = "none", penwidth = "2.5" )
        return "sgL" + str(color)

    def make_legend(self, name):
        if self.coloring == 'binary':
            "no legend necessary"
            return
        leg_gr = gvz.Digraph(name + '_legend', 
            graph_attr = { "compound": "true", "newrank": "true", 
                "ranksep" : "0.1", # "labeljust" : "l",
                "fontname" : "Courier New" })
        prev = None
        if not self.complete:
            self.usedcolorindices.discard(0)
        for color_index in sorted(self.usedcolorindices):
            with leg_gr.subgraph(graph_attr = { "rank" : "same" }) as sg:
                sg_n = self._legend_item(sg, color_index)
            if prev is not None:
                leg_gr.edge(prev, sg_n, color = 'transparent')
            prev = sg_n
        leg_gr.render(view = True)
