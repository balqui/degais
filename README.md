# degais
Decomposing Gaifman Structures (again)

<br>
<br>

![Zoo dataset, freq thr 28, exp 4](zoo_28_exp_3_9.png)

<!--- 
Comments here.
--->

<br>
<br>
<br>

Current version: early Frimaire 2024, planned to be installable.

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
(almost) arbitrary strings separated by spaces; however, 
characters ':' and '-' should not appear in items.

CLI: call the main program with the options `-h` or `--help`
to see how to employ it. Option `-f N` / `--freq_thr N` discards all 
items appearing less than `N` times. The `-c` / `--coloring` 
and `-p` / `--param` options are as follows:

`-c` / `--coloring`

`binary`: `--param` ignored, constructs standard Gaifman graph where
two items are connected exactly if they appear jointly in some
transaction;

`thresh`: `--param T` is interpreted as a threshold, graph has an edge
between two items if they appear together in at least `T` many 
transactions; if `--param` is omitted, a default is set, found by
application of (simple cases of) density-estimation-based 
unsupervised discretization;

`linwidth`: edge colors correspond to frequencies of co-occurrence 
falling in intervals of width `L`, if `--param L` is specified, 
otherwise a heuristically determined default for `L` is set;

`expwidth`: edge colors correspond to frequencies of co-occurrence 
falling in intervals of exponentially growing width with base `B`, 
if `--param B` is specified, otherwise a heuristically determined 
default for `B` is set;

`ident`: each co-occurrence frequency gets its own color (but might
exhaust the available colors); most often, this scheme leads to a 
trivial decomposition with a single, very large, spaghetti-shaped 
clan that no one understands.

Additionally, the `-k` / `--complete` option makes sure that all the
edges are visibly drawn, forming thus a 2-structure; the default
is to draw it as a graph, with missing edges for zero co-occurrences.

Two images are drawn: one with the decomposition and a second one 
(whose window may be hidden behind the decomposition) with a legend 
specifying the co-occurrence intervals corresponding to each color. 
The legend is omitted for the binary coloring scheme.


### Hints

Large primitive clans do not provide any intuition about the dataset;
the more potential "colors" are allowed, the larger primitive
clans show up, hence it is recommended that only up to 4 or 5 color
values are employed. Default values of the parameter for each option 
may fail spectacularly: check out all the information provided in order
to identify explicit alternative values to explore.


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

2. Add `-c thresh` or `--coloring thresh` while specifying `-p 2` or
`--param 2`: it will disconnect the clan `mammal -- milk` from the 
item `eggs`. The reason one needs value 2 for that effect goes by
the name "platypus".

3. Add `-c thresh` or `--coloring thresh` but leaving the actual
threshold value unspecified (no `-p` / `--param`); the default 
value will be at 43 and will disconnect from the larger clan 
a 5-element 2-structure, decomposed in turn.

4. Set other thresholds to `-c thresh`: e. g., try `-p 9` or 
`--param 9` in order to be more strict for the creation of an edge, 
and see more structure appearing. Don't forget to explore intemediate 
and/or larger values.

5. Change the coloring scheme to linear width with `-c linwidth` 
or `--coloring linwidth`. A default parameter of 19 will be guessed
but it still leaves a large primitive clan. Smaller values lead to
more colors so more distinguishable items and larger clans: it is
better to explore larger values, but even then the outcomes are not
spectacular.

6. Try `-c expwidth` instead. A fractional base of 4.1983 will 
be guessed that still leaves a large clan with four smallish ones. 
Try instead `-p 3.9` for a more interesting diagram (image above)
or, even, try `-p 3.99`.


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
