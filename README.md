# degaist
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

An example here.

## Previous developments:

Idea started several decades ago and went through several
different manifestations from 2017 onwards. The present 
incarnation had its first few correct and complete runs
by early Vendemiaire 2024.

Repository `labgaif` and several other repos contain earlier 
developments towards the same functionality. Here, we gave up 
the insistence of subclassing `pygraphviz`'s `AGraph` classes 
to work our way on `td2dot`-style graphs. Tried `python3-gv`
which works like a charm but only on Linux, then moved on to 
`https://github.com/xflr6/graphviz` much less comfortable to work
with but supposed to fly on all systems.
