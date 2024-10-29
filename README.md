# degais
Decomposing Gaifman Structures (again)

Current version: early Brumaire 2024

Author: Jose Luis Balcazar, ORCID 0000-0003-4248-4528,
relying in large parts on the functionality of code by 
Marie Ely Piceno (https://github.com/balqui/labgaif),
fully rewritten.

Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Umpteenth attempt at having a working platform on which 
we can view 2-structure decompositions of generalized 
Gaifman graphs.

## Usage

Data expected as a transactional dataset: a sequence of
transactions, one per line, each consisting of a set of items:
(almost) arbitrary strings separated by spaces. Characters ':' 
and '-' should not appear in items.

CLI: call the main program with the options `-h` or `--help`
to see them. Option `-f N` / `--freq_thr N` discards all 
items appearing less than `N`times. The `-c` / `--coloring` 
and `-p` / `--param` options are as follows:

-c / --coloring

`binary`: `--param` ignored, constructs standard Gaifman graph where
two items are connected exactly if they appear jointly in some
transaction;

`thresh`: `--param T` is interpreted as a threshold, graph has an edge
between two items if they appear together in at least `T` many 
transactions, a default corresponding to one plus the minimum frequency 
of a pair is set if `--param` is omitted;

`linwidth`: edge colors correspond to frequencies of cooccurrence 
falling in intervals of width `L`, if `--param L` is specified, 
otherwise an empirically determined default for `L` is set;

`expwidth`: edge colors correspond to frequencies of cooccurrence 
falling in intervals of exponentially growing width with base `B`, 
if `--param B` is specified, otherwise an empirically determined 
default for `B` is set.
 
### Hints

Large primitive clans do not provide any intuition about the dataset;
the more potential "colors" are allowed, the larger the primitive
clans show up, hence it is recommended that only up to 4 or 5 color
values are employed. Default values of the parameter for each option 
may fail spectacularly: check out all the information provided to 
provide explicit alternative values to explore.

### Example

File `zoo.td` contains a transactional version of the famous Zoo
dataset of UCI; there, for simplicity, only `True` values of the 
Boolean attributes are reflected as items. We suggest next some 
runs that illustrate the workings of `degais`. Pay attention to
the information the program provides: besides the given input and
parameters, we see the quantity of items that will be drawn and 
the highest and lowest number of joint occurrences of pairs of items.

1. Limiting initially the view to a dozen items is advised: use `-f 28`
or `--freq_thr 28` to keep the 12 items appearing at least 28 times. 
All are connected in the standard Gaifman graph (`lowest` reports 
this), so a single complete clan appears.

2. Add `-c thresh` or `--coloring thresh` to change the graph;
the default value will be at 2 and it will disconnect the clan 
`mammal -- milk` from the item `eggs`.

3. Set a higher threshold to `-c thresh`: add `-p 9` or `--param 9`
in order to be more strict for the creation of an edge, and see
more structure appearing. Don't forget to explore intemediate and/or
larger values.

4. Change the coloring scheme to linear width with `-c linwidth` 
or `--coloring linwidth`. A default parameter of 19 will be guessed
but it still leaves a large primitive clan. Smaller values lead to
more colors so more distinguishable items and larger clans.

5. Try `-c expwidth` instead. A base of 5 will be guessed that still
leaves a large clan with three small ones. Try instead `-p 4` for a
more interesting diagram.

## Previous developments:

The idea started several decades ago and went through several
different manifestations from 2017 onwards. The present 
incarnation had its first few correct and complete runs
by early Vendemiaire 2024.

Repository `labgaif` and several other repos contain earlier 
developments towards the same functionality. Here, we gave up 
the insistence of subclassing `pygraphviz`'s `AGraph` classes 
to work our way on `td2dot`-style graphs. Tried `python3-gv`
which works like a charm... but only on Linux, it seems! 
Then moved on to `https://github.com/xflr6/graphviz` which
we found much less comfortable to work with, but is supposed 
to fly on all systems.
