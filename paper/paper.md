---
title: 'Decomposing Gaifman Structures'
tags:
  - Python
  - visual data analysis
  - 2-structures
  - Gaifman graphs
  - transactional datasets
authors:
  - name: JLB
    orcid: 0000-0000-0000-0000
    equal-contrib: true
    affiliation: "1, 2" # (Multiple affiliations must be quoted)
    corresponding: true # (This is how to denote the corresponding author)
  - name: Author Without ORCID
    equal-contrib: true # (This is how you can denote equal contributions between multiple authors)
    affiliation: 2
  - name: Author with no affiliation
    affiliation: 3
  - given-names: Ludwig
    dropping-particle: van
    surname: Beethoven
    affiliation: 3
affiliations:
 - name: Lyman Spitzer, Jr. Fellow, Princeton University, United States
   index: 1
   ror: 00hx57361
 - name: Institution Name, Country
   index: 2
 - name: Independent Researcher, Country
   index: 3
date: 3 December 2024
bibliography: paper.bib

# Summary

We describe the application `degais` for computing and visualizing
decompositions of Gaifman structures. These are a generalization of 
undirected graphs whose tree-like decomposition often helps visualizing 
specific properties of data.

Indeed, Gaifman structures are obtained from transactional data by 
generalizing an existing notion (that of a Gaifman graph).
In [@IDA2018], we proposed to employ these generalized Gaifman graphs 
as a method of visual data analysis and, specifically, as a way of 
displaying co-occurrence patterns in data. Such a process allows
the user to understand better a given dataset, by showing visually
the roles of each item in the data in terms of their co-occurrence
patterns with other items.

As a very simple example, assume that the dataset `e5.td` 
contains three tuples (or: transactions), namely,

`a b c`

`a b d`

`a b e`

Then, a call `degais e5` will produce the following diagram, 
indicating that items `c`, `d`, and `e` never co-occur but 
all do co-occur with both `a` and `b` which, also, do co-occur:
![...](e5_1.gv.png)\ 

# Statement of need

The software used in [@IDA2018], as well as the implementations
employed for related documents [@LRNTFG; @MEPPhD; @CoIn] was not 
really usable by other people.
These predecessors of `degais` (closed-source in [@LRNTFG] and 
several variants of open-source implementations for [@MEPPhD; @CoIn]) 
get replaced now by `degais`, an implementation with which we hope
to offer the possibility of analyzing easily data, in that way, 
to any interested person.

# Model foundations

Gaifman graphs are mathematical structures introduced 
several decades ago as a means to study limitations 
of the expressivity of logical languages [@Libkin04].
Their basic notion is pretty simple:
given a dataset consisting of observations, each
observation being a set of _items_ (e. g., attribute-value 
pairs or simply categorical values), for each transaction, 
and for each pair of different items `x` and `y` in that 
transaction, we ensure that the edge `(x,y)` is present
in the graph, and that only such edges are: thus, items
coincide with vertices in the graph, and they remain 
disconnected when they don't appear jointly in any transaction.

Sometimes, we may be interested in keeping track of 
quantitative information that the standard Gaifman graph lacks.
Alternative versions were introduced in [@IDA2018]:

- In thresholded graphs, the difference between having
the edge or not, instead of being zero joint occurrences 
versus 1 or more, resorts to a threshold possibly different from 1:
graph connections represent frequencies of co-occurrence higher than 
or equal to the threshold.

- In the simplest version of labeled Gaifman graphs, the edges are 
labeled by the number of tuples containing both of the vertices that 
they connect. This strategy, in practice, most often leads nowhere.

- In more evolved versions, edge labels are obtained from these same
multiplicities via some sort of discretization process. In linear 
Gaifman graphs, labels correspond to frequencies of co-occurrence 
falling in intervals of some fixed width while in the exponential 
Gaifman graphs a log function is applied first, then the fixed-width
intervals are applied.

The data analysis approach proposed in [@IDA2018] consists in applying
a decomposition process to the (possibly labeled) Gaifman graphs;
in some cases the so-called modular graph decomposition suffices 
but, in general, one must resort to so-called clans on 2-structures 
[@ERHbook]. This is a concept that generalizes graphs and, 
specifically, symmetric 2-structures generalize undirected graphs
such as Gaifman graphs. We call Gaifman Structures the symmetric
2-structures obtained as the labeled extensions of Gaifman graphs
enumerated above.

Then, the decomposition procedure is based on the so-called "clans".
They extend the intuitive concept of when a vertex "sees in different 
ways" (or: "distinguishes") two other vertices. We say that an item `x` 
distinguishes two other items if the edges that connect `x` with 
these two items have different labels. Then, a clan is a set of items 
such that any two members of the clan cannot be distinguished by any 
item outside the clan, an idea that motivated the choice of the term.


$-- the rest to revise and mostly delete



This view is also consistent with the claim that in the field of
modular decompositions, the crucial notion is not
presence or absence of an edge, but the difference between them. 
In this sense, a graph and its complement correspond, in fact, 
to the same 2-structure.
The advantage of working with 2-structures is that they allow us 
to work with more than two equivalence classes. 
Thus the notion now corresponding to "module" has been called always a "clan".
For a 2-structure given by a set of vertices $\U$ and an equivalence relation $\E$ on its edges, 
we say that the subset $X \subseteq \U$ is a clan, informally, if, 
for every $y \in \U$$\setminus X$, $y$ cannot distinguish the elements of $X$. Formally~\cite{DBLP:books/daglib/0025562}:

As with the trivial modules, the so called trivial clans are all the singletons $\{x\}$ for $x\in \U$, as well as $\U$ itself and the empty set.
When we see a graph as a 2-structure, as indicated above, its clans are the modules.
Of course the clans can be again of two types, complete or primitive, like the modules: in a
primitive clan, there are no nontrivial clans; in a complete clan, all edges are equivalent. 
In order to  display the decomposition into a tree-like form we look again for non-overlapping clans.


Originally, strong clans were called "prime clans". 
However, in the context of modular decompositions, the adjective
"prime" has received other usages in the literature. We have
deemed better to avoid that adjective, so that previous exposure
of the reader to either modular decompositions or 2-structures
does not result in misunderstandings.

As with modules, strong clans can be collapsed into single
vertices without any ambiguity about how the 2-structure looks like
after the collapse: from the perspective of an outside vertex,
or indeed of a disjoint second clan, all the edges connecting
to nodes inside the clan are of the same equivalence class,
so that class can be chosen for edges upon collapsing
disjoint clans into vertices. The corresponding notion of coarsest quotient
2-structure follows by the same procedure as with modules:
each maximal strong clan collapses to a single vertex.
Then, each of these clans is decomposed recursively so as
to obtain a tree-like decomposition much like those we have
already seen with modules.
We say that $X\subset Y$ is a subclan of $Y$, or alternatively $Y$ is a superior clan of $X$, if $X$ is a maximal strong clan and thus belongs to the coarsest quotient of $Y$.

The internal structure of a clan is also a 2-structure, 
the sub-2-structure that involves the nodes into the clan,
most often organized according to the corresponding 
coarsest quotient.
According to the internal 2-structure of its coarsest quotient, 
each clan can be classified as a complete or a primitive clan:
in a complete clan, all the edges are in the same equivalence class, 
every subset is a clan, and there are no strong clans;
while in a primitive clan there are no nontrivial clans.
It is a theorem of the theory of 2-structures that the nodes of the 
clan decomposition of a symmetric 2-structure 
are all primitive or complete clans. This is the natural
generalization of the modular decomposition of graphs.
Recall that this paper only employs symmetric 2-structures all along;
in the general case, a third type of clan may appear in the
decomposition, namely linear clans.




This last statement was already announced informally
in our Introduction. It leads to a main interest 
of the notion of module, namely, all the vertices of
a module can be collapsed into a single vertex without
ambiguity with respect to how to connect it to the
rest of the vertices: 
the new vertex gets connected to $y$ if all the
members of the module were connected to $y$, and
remains disconnected if all the members were 
disconnected. 
Clearly, the definition given of module is what 
is needed for this process to be applied without 
ambiguity about whether the new vertex should or 
should not be connected to some external vertex $y$. 
More generally, the same considerations
apply if we simultaneously
collapse into single vertices two disjoint modules: either they
are connected, in the sense that  all the respective pairs 
of vertices (one from each module) are, or they are not 
because no such pair is.

Nothing forbids modules to intersect each other;
in that case, though, collapsing one module into 
a single vertex may affect
the other. In order to avoid side effects, it is 
customary to restrict oneself to so-called 
"strong modules" \cite{Gallai1967}
(see also \cite{Gallai1967translation}): 
they allow us to obtain a tree-like decomposition. 

Given a graph, we can focus on its maximal strong modules; %~\cite{DBLP:journals/csr/HabibP10}.
it is known that each vertex belongs to exactly one of them~\cite{survey}.
Thus, one, or more, or even all of these maximal strong modules
can be collapsed into a single vertex each. The resulting graph
is called as "quotient graph". 


Then, a tree-like structure arises from the fact that each
of these modules, taken as a set of vertices, is actually 
a subgraph that can be recursively decomposed, in turn, into maximal 
strong modules, thus generating views of subsequent internal 
structures given by their respective coarsest quotient
graphs. We display the decomposition tree while labeling
each node (a strong module) with the corresponding coarsest
quotient graph, and connect visually each collapsed vertex
to the subtree decomposing the corresponding module.
Of course, the root of the "tree" is the coarsest
quotient of the whole graph.


It is, of course, possible to apply the modular decomposition method
on this sort of graph. In reference to the data on which the graph was
constructed: what can be said of the obtained decomposition, in terms of
data analysis? This paper belongs to a line of research based on
this question.



# Functionality

# Example

# Acknowledgements

# References


Ideas for structure from published papers:
Related Work / State of the field
Target audience
Features / sw features w/subsections / Scope / Functionality and features / Embedded features / Results / Examples
Main Features w/subs + Alternatives
a simple example / Usage / Applications
Ongoing work / Conclusion
ack
refs
