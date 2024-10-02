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

from collections import defaultdict as ddict
from itertools import combinations
from functools import partial

from ezGraph import EZGraph
from clans import Clan
from dectree import DecTree

from binning import ident, binary, binlog, thresh

# ident: keeps multiplicities as labels
# binary: labels 0/1 give, essentially, a standard Gaifman graph
# binlog: base-2 exponential Gaifman graph
# partial(thresh, thr): value < thr as an int 
# Caveat: STRANGE BEHAVIOR HAPPENED WITH BINNING CONST ZERO

# from td2dot import read_graph_in

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

    argp.add_argument('-f', '--freq_thr', nargs = '?', default = '1', 
       help = "discard items with frequency below it (default: 1)")

    argp.add_argument('-c', '--coloring', nargs = '?', default = 'ident', 
       help = "label/color scheme on multiplicities (default: ident)")

# there should be a list but not hardcoded, taken from some dict or...

    argp.add_argument('-l', '--label_thr', nargs = '?', default = '1', 
       help = "set binary labels according to whether >= / < the " +
              "label threshold (only for -c thresh, default 1)")

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

    # ~ print(" ... types:", type(fullfilename), type(args.coloring),
          # ~ type(args.label_thr), type(args.freq_thr + ")") )

    # Construct labeled graph: labels are multiplicities by default but
    # we can request a thresholded graph, discarding items below also
    if (thr := int(args.label_thr)) > 1 and args.coloring == 'thresh':
        g = EZGraph(fullfilename, partial(thresh, int(args.label_thr)), 
                    int(args.freq_thr) )
    else:
        # ~ g = EZGraph(fullfilename)
        g = EZGraph(fullfilename, eval(args.coloring), 
                    int(args.freq_thr)) # eval gets function from name
        # ~ g = EZGraph(fullfilename, binlog)
    # print(g)
    items = g.items # maybe we want to use a different list of items
    # print(items)
    print(" ... loaded " + fullfilename + " (coloring " + args.coloring
          + "; freq_thr " + args.freq_thr + ")")
    if args.coloring == thresh:
          print(" ... ... label_thr " + args.label_thr)

    filename += '_' + args.freq_thr # for output


    # Initialize the decomposition tree
    assert len(items) > 0
    dt = DecTree(g)
    root = dt.sgton(items[0])
    # print("root:", root)
    
    # Add each item in turn to the decomposition tree
    for it in items[1:]:
        # print(" ... adding", it, "to", root.name) # , "root size", len(root))
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

