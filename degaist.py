from ezGraph import EZGraph
from clans import Clan
from dectree import DecTree
from td2dot import read_graph_in
from collections import defaultdict as ddict
from itertools import combinations

VERSION = "0.0 alpha"


if __name__ == "__main__":
    '''
    Taken from laibgaf/redecomp.py, initially verbatim, to be finished
    '''
    
    # ~ color = binary # Standard graph-theoretic module decomposition
                       # This issue moved to EZGraph import as coloring

    # Handle the input
    # ~ filename = "e7"
    filename = "e4a"
    # ~ filename = "e4b"
    # ~ filename = "e6a"
    # ~ filename = "e6"
    # ~ filename = "e8a"
    # ~ filename = "e7r"
    # ~ filename = "e7alt"
    # ~ filename = "ex_dec_0.td"
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
    root = Clan()
    root.sgton(items[0])
    print("root:", root)
    
    dt = DecTree(g)
    rootname = dt.store_clan(root)

    # Add each item in turn to the decomposition tree
    for it in items[1:]:
        print(" ... adding", it, "to", rootname)
        item_cl = Clan()
        item_cl.sgton(it)
        item_cl_name = dt.store_clan(item_cl)
        root = root.add(item_cl, dt)
        print(" ... added", it, "and the current root of color", root.color, "is:")
        for e in root:
            print('    ', e)

    print(root)
    print(g)
    print(dt.visib)
    for name in dt:
        print(name, dt[name])
    # ~ g.to_dot("tt")
    dt.draw(root, filename)

    # Convert the decomposition tree into a GV graph for drawing
