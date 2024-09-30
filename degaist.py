from ezGraph import EZGraph
from clans import Clan
from dectree import DecTree
from td2dot import read_graph_in
from collections import defaultdict as ddict
from itertools import combinations

VERSION = "0.1 alpha"

# Pending: remove dead code, follow up caveats, try to unify more cases,
# improve __str__ of EZGraph, run with profiler, 
# improve the docstrings, reconsider palette, set up as an application.
# Profiler to assess relevance of quadratic cost in sibling among
# the general exploration.
# Later: 
#   - Hide large primitive clans, abstract some sets of items into "others".
#   - The Nejada task (maybe somebody has written a gateway from 
#     graphviz to pygame?)
#   - Flattening issues: is palette[0] not drawn, affects flattening
#     of complete clans of color 0, paths could be flattened too.

if __name__ == "__main__":
    '''
    Taken from laibgaf/redecomp.py, initially verbatim, to be finished
    '''
    
    # ~ color = binary # Standard graph-theoretic module decomposition
                       # This issue moved to EZGraph import as coloring
                       # Caveat: STRANGE BEHAVIOR HAPPENED WITH BINNING CONST ZERO

    # Handle the input
    # ~ filename = "e4a" # binary: ok, ident: ok
    # ~ filename = "e4b" # binary = ident: ok
    # ~ filename = "e6" # binary: ok, ident: ok
    # ~ filename = "e6a" # binary: ok, ident: ok
    filename = "e7" # binary: ok, ident: ok
    # ~ filename = "e7r" # binary: ok, ident: ok
    # ~ filename = "e7alt" # binary: ok, ident: ok
    # ~ filename = "e8a" # binary: ok, ident: ok
    # ~ filename = "ex_dec_0" # ident: ok, binary: redecomp incomplete, unavailable
    # ~ filename = "titanic_" # TO BE REPLACED BY ARGUMENT PARSING AS FOLLOWS

    # ~ from argparse import ArgumentParser
    # ~ argp = ArgumentParser(
        # ~ description = ("Construct dot-coded decomposition of a graph or 2-structure"),
        # ~ prog = "python[3] redecomp.py or just ./redecomp"
        # ~ )

    # ~ argp.add_argument('-V', '--version', action = 'version', 
                                         # ~ version = "redecomp " + VERSION,
                                         # ~ help = "print version and exit")

    # ~ argp.add_argument('dataset', nargs = '?', default = None, 
                      # ~ help = "name of optional dataset file (default: none, ask user)")

    # ~ args = argp.parse_args()

    # ~ if args.dataset:
        # ~ filename = args.dataset
    # ~ else:
        # ~ print("No dataset file specified.")
        # ~ filename = input("Dataset File Name? ")

    if '.' in filename:
        fullfilename = filename
        filename, ext = filename.split('.', maxsplit = 1)
        if ext != "td":
            print("Found extension", ext, "instead of td for file", filename)
    else:
        fullfilename = filename + ".td"

    # Construct labeled graph: labels are multiplicities
    # ~ g, items = read_graph_in(fullfilename)
    g = EZGraph(fullfilename)
    print(g)
    items = g.items
    # ~ items = list(reversed(g.items))
    # ~ items = list('abcde') # 'abcdef'

# Titanic nodes in order of edge weight, computed separately, 
# cases 1a and 1b until Age_Child 1d:
    # ~ ittit = ['Age_Adult', 'Sex_Male', 'Survived_No', 'Class_Crew', 
    # ~ 'SurvivedYes', 'Class_3rd', 'Sex_Female', 'Class_1st', 
    # ~ 'Class_2nd', 'Age_Child']
    # ~ items = ['Class_1st', 'Class_Crew', 'Class_3rd', 'Class_2nd',
    # ~ 'Age_Adult', 'Sex_Male', 'Survived_No',
    # ~ 'Survived_Yes', 'Sex_Female', 'Age_Child'] # 4Classes and Adult good for t coloring

    print(items)

    # Initialize the decomposition tree
    assert len(items) > 0
    dt = DecTree(g)
    root = dt.sgton(items[0])
    print("root:", root)
    
    # ~ rootname = dt.store_clan(root)

    # Add each item in turn to the decomposition tree
    for it in items[1:]:
        print(" ... adding", it, "to", root.name)
        item_cl = dt.sgton(it)
        # ~ item_cl_name = dt.store_clan(item_cl)
        root = root.add(item_cl, dt)
        print(" ... added", it, "and the current root of color", root.color, "is:")
        for e in root:
            print('    ', e)

    # ~ print(root)
    # ~ print(g)
    print(dt.visib)
    # ~ for name in dt:
        # ~ print(name, dt[name])
    # ~ g.to_dot("tt")

    # Convert the decomposition tree into a GV graph for drawing
    dt.draw(root, filename)
