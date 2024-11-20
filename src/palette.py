'''
Author: Jose Luis Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Palette of colors for Gaifman structures under various binning schemes.

Cuts in list mark a different color between x <= cut and cut < x
(doing it the other way raises incompatibilities with zero
and the -k option; a temporary solution with cuts at .5 and
exploring different binary search schemes did not provide the 
desired behavior).

Offers a coloring method to color the EZGraph while registering 
which colors are actually employed, and a method for drawing a 
legend only with actually employed colors with their corresponding 
values or intervals.

Available colorings:
 ident: keeps multiplicities as labels
 binary: labels 0/1 which give, essentially, a standard Gaifman graph
 thresh: thresholded Gaifman graph, threshold given as param
 linwidth: linear Gaifman graph, interval width given as param,
   default value provided by lguess
 expwidth: exponential Gaifman graph, base given as param,
   default value provided by eguess
'''

import graphviz as gvz               # NOT the official bindings!

from math import floor
from bisect import bisect_left as bs # specific variant of binary search
from auxfun import lguess, eguess, thr_1    # compute heuristic defaults


class Palette:
    '''
    Handles the colors both in the graph (as an index) and
    at drawing time; provides as well the legend; it needs
    the explicit cuts for this.
    NB: sequence self.cuts does NOT include the extreme points.
    Sequence self.ecuts does. Maybe one can do with only one of them.
    '''

    def __init__(self, labels, coloring, param, complete):
        '''
        We need the frequency labels of all edges now.
        '''
        if len(labels) == 1:
            print(" * Only one label. Binary coloring scheme enforced.")
            self.coloring = 'binary'
            self.param = 1
            self.complete = False # will be complete anyhow, on itself
        else:
            default = {   'thresh': thr_1, 
                        'expwidth': eguess, 
                        'linwidth': lguess, 
                          'binary': lambda x: 1, 
                           'ident': lambda x: 1 } # last two irrelevant
            if coloring not in default:
                print(" * Sorry. Unknown coloring scheme " + coloring + '. Exiting.')
                exit()
            try:
                param = default[coloring](labels) if param is None else float(param) 
                if coloring.endswith('width') and param <= 0:
                    raise ValueError
                if coloring != 'expwidth':
                    param = int(param)
                elif param <= 1:
                    raise ValueError
            except ValueError:
                "may come from either float(param) or a nonpositive value"
                print(" * Sorry. Disallowed value " + str(param) + " for " + coloring + '. Exiting.')
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

        if self.coloring == 'ident':
            "color: bisect - int(not complete)"
            if len(labels) > len(self.the_colors) - int(self.complete):
                print(" * Sorry. Too many classes, not enough colors. Exiting.")
                exit()
            self.cuts = labels
            self.complete = True # override --complete if it was absent
        elif self.coloring == 'thresh':
            self.cuts.append(param)
        elif self.coloring == 'linwidth':
            c = param
            while c <= labels[-1]:
                self.cuts.append(c)
                c += param
        elif self.coloring == 'expwidth':
            c = param
            while c <= labels[-1]:
                self.cuts.append(c)
                c *= param
        else:
            "coloring is 'binary'"
            self.cuts = [0]
            self.complete = False # override --complete if it was present
        self.ecuts = ([-1] if self.complete else list()) + self.cuts + [labels[-1]]


    def color(self, label):
        "if complete, need to avoid index 0 so as to avoid flattening"
        index = bs(self.cuts, label) + int(self.complete)
        self.usedcolorindices.add(index)
        return index


    def _legend_item(self, legend_line, color_index):
        '''
        takes the color from self.the_colors and the value or 
        interval from consecutive pairs in self.ecuts; 
        '''
        if self.coloring == 'ident':
            label = str(self.cuts[color_index - int(self.complete)])
        else:
            "some coloring schemes work with a float as param"
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
        leg_gr.render(format = "png", view = True) # may produce some Linux error
        # ~ leg_gr.render(view = True)
