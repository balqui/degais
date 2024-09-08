#! /usr/bin/env python3

'''
Author: Jose Luis Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Construct labeled Gaifman graph of a transactional dataset.

Produce either DOT output on stdout for the Gaifman graph
or an AGraph from pygraphviz with separate singletons and 
representing points.

Pending: smarter iterator on .td file to handle comments and such

Graph is read as adjacency lists, then transformed into DOT code
or into an AGraph. Specifically, graph g is a dict of counters, 
maps node u to g[u] which is a Counter of edges: g[u][v] gives 
how many occurrences we find of the pair (u, v) in a transaction.

Invariant: undirected graph, hence g[u][v] = g[v][u], careful 
with the redundancy at output time.

Alpha chars in filename used as dot graph name.

'''

from collections import Counter, defaultdict
from itertools import combinations
from sgton import Sgton
from auxfun import delbl, q

VERSION = "0.2 alpha"

def read_graph_in(filename):
    '''
    filename must be a .td file containing only transactions:
    comments and other variations not supported yet;
    returns Gaifman graph and sorted list of items
    '''
    gr = defaultdict(Counter)
    items = set()
    with open(filename) as f:
        for line in f:
            transaction = set(line.split())
            if transaction:
                items.update(transaction)
                for (u,v) in combinations(transaction, 2):
                    gr[u][v] += 1
                    gr[v][u] += 1
    return gr, sorted(items)

def dump_graph(gr):
    for u in gr:
        for v in gr[u]:
            if u <= v:
                print(u, v, gr[u][v], gr[v][u])

def dot_output(gr, name):
    print("graph " + name + " {")
    for u in gr:
        for v in gr[u]:
            if gr[u][v] != gr[v][u]:
                print("Wrong count for items", u, "and", v)
                exit(-1)
            if u <= v:
                print(q(u), " -- ", q(v), "[ label = ", gr[u][v], "]")
    print("}")

def dot_output_file(gr, name, fnm):
	with open(fnm, 'w') as f:
	    print("graph " + name + " {", file = f)
	    for u in gr:
	        for v in gr[u]:
	            if gr[u][v] != gr[v][u]:
	                print("Wrong count for items", u, "and", v)
	                exit(-1)
	            if u <= v:
	                print(q(u), " -- ", q(v), "[ label = ", gr[u][v], "]", file = f)
	    print("}", file = f)

def make_agraph(gr, items, outgr):
	'''outgr expected to be a pygraphviz's AGraph;
	adds to it the pairs for the singletons and
	returns the internal names for the representing points
	'''
	name = dict()
	for n in items:
		s = Sgton(n)
		name[n] = s.nmr
		s.add_sgton(outgr)
	for u in gr:
		for v in gr[u]:
			if u <= v:
				outgr.add_edge(name[u], name[v], label = gr[u][v])
	return sorted(name.values())

def make_agraph_edge_sorted(gr, items, outgr):
	'''outgr expected to be a pygraphviz's AGraph;
	adds to it the pairs for the singletons and
	returns the internal names for the representing points
	'''
	name = dict()
	weight = defaultdict(int)
	for n in items:
		s = Sgton(n)
		name[n] = s.nmr, s.lbl 
		s.add_sgton(outgr)
	for u in gr:
		for v in gr[u]:
			if u <= v:
				outgr.add_edge(name[u][0], name[v][0], label = gr[u][v])
				weight[name[u][1]] = max(weight[name[u][1]], gr[u][v])
				weight[name[v][1]] = max(weight[name[v][1]], gr[u][v])
	# ~ print(weight)
	return sorted(name.values(), key = lambda x: weight[x], reverse = True)



if __name__ == "__main__":
    
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
    



