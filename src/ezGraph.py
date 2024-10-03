'''
Author: Jose Luis Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Easy, homemade graph class for supporting the construction of 
labeled Gaifman graph of a transactional dataset. Quite a few
earlier attempts of employing ready-made graph classes got into
far more complications than preparing it from scratch.

Pending: smarter iterator on .td file to handle comments and such.

As of recently, items must not contain SEP which defaults to '-',
see https://github.com/balqui/degais/issues/3 about that. 
Earlier constraint that items must not start with an asterisk not
enforced anymore.
'''

# ~ from sys import exit
from collections import Counter, defaultdict as ddict
from itertools import combinations
from auxfun import delbl, q
from bisect import bisect, insort

# default coloring, keeps multiplicities as labels
# ~ from binning import ident

SEP = '-' # constant to make up clan names, forbidden in items

# ~ DIGITS = frozenset('0123456789') # to remove items with digits in cmc dataset

class EZGraph(ddict):
    '''
    Nodes are strings. A graph is a dict of counters: maps node u 
    to g[u] which is a Counter of edges: in the case of the Gaifman
    structure on the input dataset, g[u][v] tells how many transactions
    include some occurrence of the pair (u, v) or, alternatively, the 
    outcome of an optional binning strategy (called coloring and for 
    now imported from a binning package) on that quantity. The values 
    g[u][v] are then called colors or labels. Another instance stores 
    the visibility graph of the decomposition tree: how each clan sees 
    each other as we have found up to that point.

    As undirected graphs without self-loops, g[u][v] only kept for u<v.

    Contains as well the sorted list of items (strings in the nodes).

    Alpha chars in filename used as graph name for exporting 
    later into DOT format.
    '''

    def __init__(self, filename = None, coloring = lambda x: x, frq_thr = 0):
        '''
        The filename must be a .td file containing only transactions,
        but see https://github.com/balqui/degais/issues/12 about it;
        initializes colored Gaifman graph and adds to it the sorted 
        list of items. The coloring function is usually taken from 
        the package binning.py and the frequency threshold allows us
        to discard infrequent items if this is convenient.
        '''
        super().__init__(Counter)
        if filename is None:
            self.items = list()
            self.name = '' # empty name e. g. for clan visibility graph
        else:
            self.name = delbl(filename.split('.')[0])
            items = Counter()
            with open(filename) as f:
                for line in f:
                    transaction = set(line.split())
                    if transaction:
                        items.update(Counter(transaction))
                        # ~ items.update( it for it in transaction 
                          # ~ if not DIGITS.intersection(it) ) # for cmc
                        for (u,v) in combinations(transaction, 2):
                            self[min(u, v)][max(u, v)] += 1
            self.items = sorted(it for it in items if items[it] > frq_thr)
            for u in self.items:
                if SEP in u:
                    print(q(SEP), 'not valid in item', u, 
                          '(please change separator SEP in source code).')
                    exit()
                for v in self.items:
                    if u < v:
                        self[u][v] = coloring(self[u][v])

    def __str__(self):
        "Tuned for 1-digit colors, short names and few nodes; caveat: improve some day"
        mxlen = 0
        for u in self.items:
            mxlen = max(mxlen, len(u))
        r = self.name + '\n'
        r += ' ' * (mxlen + 1) + ' '.join(f'{u:<{mxlen}}' for u in self.items) + '\n'
        for u in self.items:
            r += f'{u:<{mxlen}}' + ' '
            for v in self.items:
                if u < v:
                    r += f'{self[u][v]:<{mxlen + 1}}'
                else: 
                    r += ' ' * (mxlen + 1)
            r += '\n'
        return r

    def new_edge(self, u, v, label, src = ''):
        '''
        Items in self.items might be data items or clan names.
        '''
        if u not in self.items:
            insort(self.items, u)
        if v not in self.items:
            insort(self.items, v)
        self[u][v] = label

    def to_dot(self, filename = None):
        "Edges with label zero are omitted"
        if filename is None:
            filename = self.name
        if not filename.endswith(".dot"):
            filename += ".dot"
        with open(filename, 'w') as f:
            print("graph " + self.name + " {", file = f)
            for u in self:
                for v in self[u]:
                    if u < v and self[u][v] > 0:
                        print(q(u), " -- ", q(v), "[ label = ", q(str(self[u][v])), "]", file = f)
            print("}", file = f)

if __name__ == "__main__":
    gr1 = EZGraph("ex_dec_0.td")
    print(gr1)
    gr1.to_dot()
