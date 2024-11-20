# degais

### Decomposing Gaifman Structures (again)

<br>
<br>

![Zoo dataset, freq thr 28, exp 4](zoo_28_exp_3_9.png)

<!--- 
Check out this one day.
--->

<br>
<br>

(Image: screen capture of the outcome of 
`degais zoo --coloring expwidth --param 3.9`.)

<br>
<br>

Current version: early Frimaire 2024, 
planned to be made publicly available.

Author: Jose Luis Balcazar, ORCID 0000-0003-4248-4528,
relying in large parts on the functionality of 
[code by Marie Ely Piceno](https://github.com/balqui/labgaif),
although fully rewritten.

Copyleft: [MIT License](https://en.wikipedia.org/wiki/MIT_License).

Usage: [Documentation](https://github.com/balqui/degais/blob/main/docs/doc.md)
is rather minimal as of today but covers the basics. 

Umpteenth attempt at having a working platform on which 
we can view 2-structure decompositions of generalized 
Gaifman graphs.

The idea started several decades ago and went through several
different manifestations from 2017 onwards. The present 
incarnation had its first few correct and complete runs
by early Vendemiaire 2024.

Repository `labgaif` and several other repos contain earlier 
developments towards the same functionality. Here, we gave up 
the insistence of subclassing `pygraphviz`'s `AGraph` classes 
to work our way on `td2dot`-style graphs. Tried 
[python3-gv](https://graphviz.org/pdf/gv.3python.pdf)
which works like a charm... but only on Linux, it seems! 
Then moved on to 
[Sebastian Bank's `graphviz`](https://graphviz.readthedocs.io):
then we no longer can access the internals of `Graphviz` 
(the original C++ tool) but gain portability as it is 
supposed to fly on all systems.
