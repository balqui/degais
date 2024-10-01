'''
DeGaiS: Decomposing Gaifman Structures

Current version: Vendemiaire 2024

Author: Jose Luis Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Umpteenth attempt at having a working platform on which view
2-structure decompositions of generalized Gaifman graphs.

Idea started several decades ago and went through several
different manifestations from 2017 onwards. The present 
incarnation had its first few correct and complete runs
by early Vendemiaire 2024.

PUSH THIS WITH SIMPLIFIED CASES, THEN MOVE ON TO DELETING
DEAD CODE AND CALL IT GAMMA, THEN SEE WHAT ELSE IS 
NEEDED BEFORE SETTING UP AN APP AND GENERATING IT.
MAYBE OPTIONAL OUTPUT MESSAGE AND CALL CLI COMMAND
TO SHOW THE PNG. ALSO, TRY EVERYTHING ON VENV AT THE
OFFICE MACHINE TO CHECK THE DEPENDENCIES. ALSO IT MAY
BE THAT conda HAS EVERYTHING SET UP ALSO ON WINDOWS.
'''

from ezGraph import EZGraph
from clans import Clan
from dectree import DecTree
# from td2dot import read_graph_in
from collections import defaultdict as ddict
from itertools import combinations

VERSION = "0.1 beta"

def run():
    '''
    Stand-alone CLI command to be handled as entry point
    (https://packaging.python.org/en/latest/specifications/entry-points)
    '''
    from argparse import ArgumentParser
    argp = ArgumentParser(
        description = "Construct a dot-coded Gaifman structure " + 
                      "decomposition for a transactional dataset"
        )

    argp.add_argument('-V', '--version', action = 'version', 
                                         version = "degais " + VERSION,
                                         help = "print version and exit")

    argp.add_argument('dataset', nargs = '?', default = None, 
                      help = "name of optional dataset file (default: none, ask user)")

    args = argp.parse_args()

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

    # Construct labeled graph: labels are multiplicities
    g = EZGraph(fullfilename)
    # print(g)
    items = g.items # maybe we want to use a different list of items
    # print(items)

    # Initialize the decomposition tree
    assert len(items) > 0
    dt = DecTree(g)
    root = dt.sgton(items[0])
    # print("root:", root)
    
    # Add each item in turn to the decomposition tree
    for it in items[1:]:
        # print(" ... adding", it, "to", root.name)
        item_cl = dt.sgton(it)
        root = root.add(item_cl, dt)
        # print(" ... added", it, "and the current root of color", root.color, "is:")
        # for e in root:
        #     print('    ', e)

    # ~ print(root)
    # ~ print(g)
    # ~ print(dt.visib)
    # ~ for name in dt:
        # ~ print(name, dt[name])
    # ~ g.to_dot("tt")

    # Convert the decomposition tree into a GV graph for drawing
    dt.draw(root, filename)
    print("Wrote", filename + ".gv")

if __name__ == "__main__":
    run()

