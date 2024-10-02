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
from binning import ident

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

    def __init__(self, filename = None, coloring = ident, frq_thr = 0):
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
                # ~ if u.startswith('*'):
                    # ~ "caveat: did we remove this constraint definitely?" 
                    # ~ print('Initial asterisk not valid in item', u)
                    # ~ exit()
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
        # print(sorted(self[u][v] for u in self for v in self[u])) 
        return r

    # ~ def has(self, item):
        # ~ '''
        # ~ Search among dict keys unreliable due to edges only from min to max.
        # ~ Bisect for binary search on items.
        # ~ '''
        # ~ pos = bisect(self.items, item)
        # ~ return pos > 0 and self.items[pos - 1] == item

    # ~ def new_node(self, u):
        # ~ '''
        # ~ Might be already there; if not, connect with -2 to 
        # ~ existing nodes; only applies to additional clan nodes.
        # ~ '''
        # ~ print(' ... ... new node call:', u, end = ' ')
        # ~ if not self.has(u):
            # ~ '''
            # ~ Slightly inefficient, repeats the log search just made,
            # ~ but linear shift time dominates.
            # ~ '''
            # ~ insort(self.items, u)
            # ~ q = u
            # ~ print("connecting -2", end = ' ')
            # ~ for v in self.items:
                # ~ print(v, end = ' ')
                # ~ if v < u:
                    # ~ self[v][u] = -2
                # ~ if v > u:
                    # ~ self[u][v] = -2
        # ~ print("|")

    # ~ def new_edge(self, u, v, label, src = ''):
        # ~ '''
        # ~ Employed only on visibility graphs; u is a clan name 
        # ~ and v an item, hence u < v due to asterisk.
        # ~ No need to cater for adding isolated vertices.
        # ~ SUPERSEDED, NEED TO BE ABLE TO ADD EDGES BETWEEN CLANS
        # ~ if v < u:
            # ~ u, v = v, u
        # ~ '''
        # ~ print(' ... ... ... new edge', u, v, label, src)
        # ~ if u not in self.items:
            # ~ insort(self.items, u)
        # ~ if v not in self.items:
            # ~ insort(self.items, v)
        # ~ self[u][v] = label

    # ~ def edge_label(self, u, v):
        # ~ '''
        # ~ '''
        # ~ p, q = min(u, v), max(u, v)
        # ~ return self[p][q]

    def new_edge(self, u, v, label, src = ''):
        '''
        Items in self.items might be data items or clan names.
        '''
        # print(' ... ... ... new edge:', u, v, label, src)
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



# Replaced by to_dot:
# ~ def dot_output_file(gr, name, fnm):
    # ~ with open(fnm, 'w') as f:
        # ~ print("graph " + name + " {", file = f)
        # ~ for u in gr:
            # ~ for v in gr[u]:
                # ~ if gr[u][v] != gr[v][u]:
                    # ~ print("Wrong count for items", u, "and", v)
                    # ~ exit(-1)
                # ~ if u <= v:
                    # ~ print(q(u), " -- ", q(v), "[ label = ", gr[u][v], "]", file = f)
        # ~ print("}", file = f)

# Replaced by the init dunder:
# ~ def read_graph_in(filename, coloring = binary):
    # ~ gr = defaultdict(Counter)
    # ~ items = set()
    # ~ with open(filename) as f:
        # ~ for line in f:
            # ~ transaction = set(line.split())
            # ~ if transaction:
                # ~ items.update(transaction)
                # ~ for (u,v) in combinations(transaction, 2):
                    # ~ gr[u][v] += 1
                    # ~ gr[v][u] += 1
    # ~ for u in gr:
        # ~ for v in gr:
            # ~ gr[u][v] = coloring(gr[u][v])
    # ~ return gr, sorted(items)

# Replaced by the str dunder:
# ~ def dump_graph(gr):
    # ~ for u in gr:
        # ~ for v in gr[u]:
            # ~ if u <= v:
                # ~ print(u, v, gr[u][v], gr[v][u])

# ~ def dot_output(gr, name):
    # ~ print("graph " + name + " {")
    # ~ for u in gr:
        # ~ for v in gr[u]:
            # ~ if gr[u][v] != gr[v][u]:
                # ~ print("Wrong count for items", u, "and", v)
                # ~ exit(-1)
            # ~ if u <= v:
                # ~ print(q(u), " -- ", q(v), "[ label = ", gr[u][v], "]")
    # ~ print("}")

# rest of file inherited from earlier files, to be adjusted or deleted

# ~ def make_agraph(gr, items, outgr):
    # ~ '''outgr expected to be a pygraphviz's AGraph;
    # ~ adds to it the pairs for the singletons and
    # ~ returns the internal names for the representing points
    # ~ '''
    # ~ name = dict()
    # ~ for n in items:
        # ~ s = Sgton(n)
        # ~ name[n] = s.nmr
        # ~ s.add_sgton(outgr)
    # ~ for u in gr:
        # ~ for v in gr[u]:
            # ~ if u <= v:
                # ~ outgr.add_edge(name[u], name[v], label = gr[u][v])
    # ~ return sorted(name.values())

# ~ def make_agraph_edge_sorted(gr, items, outgr):
    # ~ '''outgr expected to be a pygraphviz's AGraph;
    # ~ adds to it the pairs for the singletons and
    # ~ returns the internal names for the representing points
    # ~ '''
    # ~ name = dict()
    # ~ weight = defaultdict(int)
    # ~ for n in items:
        # ~ s = Sgton(n)
        # ~ name[n] = s.nmr, s.lbl 
        # ~ s.add_sgton(outgr)
    # ~ for u in gr:
        # ~ for v in gr[u]:
            # ~ if u <= v:
                # ~ outgr.add_edge(name[u][0], name[v][0], label = gr[u][v])
                # ~ weight[name[u][1]] = max(weight[name[u][1]], gr[u][v])
                # ~ weight[name[v][1]] = max(weight[name[v][1]], gr[u][v])
    # ~ return sorted(name.values(), key = lambda x: weight[x], reverse = True)

if __name__ == "__main__":
    # ~ gr1 = EZGraph("e7.td")
    gr1 = EZGraph("ex_dec_0.td")
    # ~ gr1 = EZGraph("lenses.td") # requires a different SEP
    print(gr1)
    # ~ gr1.to_dot("ex_dec_0")


if __name__ == "__MAIN__":
    "This never runs, inherited from earlier files and to be adjusted or deleted"
    
    from argparse import ArgumentParser
    argp = ArgumentParser(
        description = ("Construct dot-coded labeled Gaifman graph" +
                       " from transactional dataset"),
        prog = "python[3] td2dot.py or just ./td2dot"
        )

    # ~ argp.add_argument('-v', '--verbose', action = 'store_true', 
                      # ~ help = "verbose report of current support at every closure")

    argp.add_argument('-V', '--version', action = 'version', 
                                         version = "td2dot " + VERSION,
                                         help = "print version and exit")

    argp.add_argument('dataset', nargs = '?', default = None, 
                      help = "name of optional dataset file (default: none, ask user)")
    
    args = argp.parse_args()

    # ~ if args.verbose:
        # ~ statics.verbose = True

    if args.dataset:
        filename = args.dataset
    else:
        print("No dataset file specified.")
        filename = input("Dataset File Name? ")
    
    if '.' in filename:
        fullfilename = filename
        filename, ext = filename.split('.', maxsplit = 1)
        if ext != "td":
            print("Found extension", ext, "instead of td for file", filename)
    else:
        fullfilename = filename + ".td"
    
    gr, items = read_graph_in(fullfilename)
    # ~ print(items)
    # ~ dump_graph(gr)
    # ~ dot_output(gr, delbl(filename))
    
    from pygraphviz import AGraph
    g = AGraph(name = delbl(filename))
    # ~ nm = make_agraph(gr, items, g)
    nm = make_agraph_edge_sorted(gr, items, g)
    # ~ print("Internal AGraph names:", nm)
    g.layout("dot")
    g.draw(filename + "_sgtons.png")
    # ~ g.write(filename + "_sgtons.dot")
    



