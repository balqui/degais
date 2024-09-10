'''
Author: Jose Luis Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Easy, homemade graph class for supporting the construction of 
labeled Gaifman graph of a transactional dataset. Quite a few
earlier attempts of employing ready-made graph classes got into
far more complications than preparing it from scratch.

Pending: smarter iterator on .td file to handle comments and such.
'''

VERSION = "0.0 alpha"

from collections import Counter, defaultdict as ddict
from itertools import combinations
from auxfun import delbl, q

# keeps multiplicities as labels
from binning import ident as coloring 

# labels 0/1 give, essentially, a standard Gaifman graph
# ~ from binning import binary as coloring 

class EZGraph(ddict):
    '''
    Nodes are strings. A graph is a dict of counters: maps node u 
    to g[u] which is a Counter of edges: g[u][v] gives how many 
    occurrences we find of the pair (u, v) in a transaction or, 
    alternatively, the outcome of an optional binning strategy 
    (called coloring and probably imported from a binning package)
    on that quantity. The values g[u][v] are called colors or labels. 
    
    As undirected graphs without self-loops, g[u][v] only exists if u < v.

    Contains as well the sorted list of items (strings in the nodes).

    Alpha chars in filename used as graph name for exporting 
    into DOT format.
    '''

    def __init__(self, filename = None):
        '''
        The filename must be a .td file containing only transactions:
        comments and other variations not supported yet;
        initializes colored Gaifman graph and adds to it sorted list of items.
        '''
        super().__init__(Counter)
        if filename is None:
            self.items = list()
            self.name = None
        else:
            self.name = delbl(filename.split('.')[0])
            items = set()
            with open(filename) as f:
                for line in f:
                    transaction = set(line.split())
                    if transaction:
                        items.update(transaction)
                        for (u,v) in combinations(transaction, 2):
                            self[min(u, v)][max(u, v)] += 1
                print()
            self.items = sorted(items)
            for u in self.items:
                for v in self.items:
                    if u < v:
                        self[u][v] = coloring(self[u][v])

    def __str__(self):
        "Tuned for 1-digit colors, improve some day"
        r = self.name + '\n' + '  ' + ' '.join(self.items) + '\n'
        for u in self.items:
            r += u + ' '
            for v in self.items:
                if u < v:
                    r += str(self[u][v]) + ' '
                else: 
                    r += '  '
            r += '\n'
        return r

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
                    if u < v and self[u][v]:
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
    # ~ gr0 = EZGraph()
    # ~ print(gr0)
    # ~ gr1 = EZGraph("e7.td")
    gr1 = EZGraph("ex_dec_0.td")
    print(gr1)
    gr1.to_dot("ex_dec_0")


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
    



