from clans import Clan
from td2dot import read_graph_in
from collections import defaultdict as ddict
from itertools import combinations

VERSION = "0.0 alpha"


if __name__ == "__main__":
    '''
    Taken from laibgaf/redecomp.py, initially verbatim, to be finished
    '''
    
    # ~ color = binary # Standard graph-theoretic module decomposition

    # Handle the input
    # ~ filename = "e7"
    filename = "titanic_" # TO BE REPLACED BY ARGUMENT PARSING AS FOLLOWS

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
    g, items = read_graph_in(fullfilename)
    # ~ print(items)

# Titanic nodes in order of edge weight, computed separately, 
# cases 1a and 1b until Age_Child 1d:
    # ~ ittit = ['Age_Adult', 'Sex_Male', 'Survived_No', 'Class_Crew', 
    # ~ 'SurvivedYes', 'Class_3rd', 'Sex_Female', 'Class_1st', 
    # ~ 'Class_2nd', 'Age_Child']
    items = ['Class_1st', 'Class_Crew', 'Class_3rd', 'Class_2nd',
    'Age_Adult', 'Sex_Male', 'Survived_No'] 
    # 'SurvivedYes', 'Sex_Female',  
    # , 'Age_Child']


    # Initialize the decomposition tree
    assert len(items) > 1 # need at least two items
    first = Clan()
    first.sgton(items[0])
    second = Clan()
    second.sgton(items[1])

    root = Clan()
    root.init(first, second, g[first.prototype][second.prototype])
    print(root)

    # Add all items to the decomposition tree
    for it in items[2:]:
        root = root.add(it, g)
        print(root)

    # Convert the decomposition tree into a GV graph for drawing


