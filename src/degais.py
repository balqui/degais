'''
DeGaiS: Decomposing Gaifman Structures

Current version: early Frimaire 2024

Author: Jose Luis Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Umpteenth attempt at having a working platform on which view
2-structure decompositions of generalized Gaifman graphs.

Idea started several decades ago and went through several
different manifestations from 2017 onwards. The present 
incarnation had its first few correct and complete runs
by early Vendemiaire 2024.
'''

from collections import defaultdict as ddict
from functools import partial

from ezGraph import EZGraph
from clans import Clan
from dectree import DecTree # based on SB's graphviz for Python
                            # see deadends/dectree_linux.py for 
                            # a Linux-only variant based on the
                            # official Graphviz bindings python3-gv

from palette import Palette

# REFACTORED INTO Palette CLASS

# ~ from binning import \
    # ~ ident, binary, thresh, linwidth, expwidth, lguess, eguess

# ident: keeps multiplicities as labels
# binary: labels 0/1 give, essentially, a standard Gaifman graph
# thresh: thresholded Gaifman graph, threshold given as param
# linwidth: linear Gaifman graph, interval width given as param,
#   default value provided by lguess
# expwidth: exponential Gaifman graph, base given as param,
#   default value provided by eguess

VERSION = "1.4"


def run():
    '''
    Stand-alone CLI command to be handled as entry point
    (https://packaging.python.org/en/latest/specifications/entry-points)
    '''
    from argparse import ArgumentParser
    argp = ArgumentParser(
        description = "Construct a dot-coded Gaifman structure " + 
                      "decomposition for a transactional dataset."
        )

    argp.add_argument('-V', '--version', action = 'version', 
       version = "degais " + VERSION,
       help = "print version and exit")

    argp.add_argument('dataset', nargs = '?', default = None, 
       help = "name of optional dataset file (default: none, ask user)")

    argp.add_argument('-f', '--freq_thr', nargs = '?', default = '1', 
       help = "discard items with frequency below it (default: 1)")

    argp.add_argument('-c', '--coloring', nargs = '?', default = 'binary', 
       help = ("label/color scheme on multiplicities" +
           " (default: binary for std Gaifman graphs)") +
           "; see README at GitHub for options and param")

    argp.add_argument('-p', '--param', nargs = '?', default = None, 
       help = "additional parameter for coloring")

    argp.add_argument('-k', '--complete', action = 'store_true', 
       help = "draw a complete graph instead of disconnecting " + \
              "items that never co-occur (default: disconnect " + \
              "them); ignored if coloring is binary.")

    args = argp.parse_args()

    # handle the dataset file
    if args.dataset:
        filename = args.dataset
    else:
        print("No dataset file specified.")
        filename = input("Dataset File Name? ")

    if '.' in filename:
        fullfilename = filename
        filename, ext = filename.split('.', maxsplit = 1)
        if ext != "td":
            print(" * Found extension", ext, "instead of td for file", filename)
    else:
        fullfilename = filename + ".td"

    g = EZGraph(fullfilename, int(args.freq_thr) )
    items = g.items # maybe we want to use a different list of items
    
    if len(g.labels) == 0:
        print(" * Sorry. No edges available.", 
              len(g.items), "item(s) at that frequency threshold.",
              "Exiting.")
        exit()
    
    palette = Palette(g.labels, args.coloring, args.param, args.complete)

    g.recolor(palette.color)

    print(" * Loaded " + fullfilename + "; coloring: " + palette.coloring
          + "; param: " + str(palette.param) 
          + "; freq_thr: " + args.freq_thr 
          + ";\n   items at threshold: " +  str(len(items)) 
          + "; pair frequencies, "
          + "highest: " + str(g.labels[-1]) 
          + ", lowest: " + str(g.labels[0]) + "."
          )

    filename += '_' + args.freq_thr # for output

    ans = input(" * Continue? ")
    if ans in ['n', 'N', 'no', 'No', 'NO' ]: exit()

    palette.make_legend(filename)

    # ~ exit()

    # Initialize the decomposition tree
    dt = DecTree(g)
    root = dt.sgton(items[0])
    
    # Add each item in turn to the decomposition tree
    for it in items[1:]:
        item_cl = dt.sgton(it)
        root = root.add(item_cl, dt)

    # Convert the decomposition tree into a GV graph for drawing
    outfile = dt.draw(root, filename, palette.the_colors)
    print(" * Wrote files with prefix", filename + ".")

if __name__ == "__main__":
    run()

