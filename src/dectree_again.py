from itertools import combinations as comb
from auxfun import delbl
from ezGraph import EZGraph, SEP
from clans import Clan
import graphviz as gvz # NOT the official bindings, giving it a try again
        # ~ Refactoring everything for using the pip/conda-importable 
        # ~ graphviz instead of the python3-gv official bindings.
        # ~ Caveat: methods in that library do NOT return
        # ~ node/edge/graph handles, must use just names!
        # ~ Caveat on flattening: 
        # ~ see https://github.com/balqui/degais/issues/10

# ~ ALSO: current graphviz does not support colons in node names
class DecTree(dict):
    '''
    The dict keeps a clan pool with all the clans that get created 
    along, with their names as keys. Only part of them belong to the 
    tree. Splitting may fish back in an older clan: now we don't need
    to recreate it with all its visibility properties already known. 
    Thus, this class acts as a Clan factory to create new ones when
    non-repeated.

    This class keeps as well the visibility graph recording all
    colors between clan names and includes the method that calls
    GraphViz to create the image file.

    A separate variable will be recording the current root at
    all times. Only clans reachable from there are actually 
    part of the current tree. 

    Palette as originally designed by Ely, must be reconsidered 
    at some point.

    In the self.visib EZGraph, clan names get added as vertices to 
    record their visibility. As zero is a valid color of the input 
    graph but here zero means no information, and -1 represents 
    "not visible", colors are coded by adding 2 to the value instead. 
    '''

    def __init__(self, graph):
        super().__init__(self)
        self.visib = EZGraph()
        self.graph = graph # the data/input Gaifman graph
        self.palette = ('white', 'black', 'blue', 'blueviolet',
                        'brown', 'burlywood', 'cadetblue', 
                        'chartreuse', 'coral', 'crimson', 'cyan',
                        'darkorange', 'deeppink', 'deepskyblue', 
                        'forestgreen', 'gold', 'greenyellow',
                        'hotpink', 'orangered', 'pink', 'red',
                        'seagreen', 'yellow') # original color sequence by Ely

    def clan(self, elems, color = -1):
        '''
        Only place where non-singleton clans are created.
        Returns the nonempty, nonsingleton clan out of the pool if 
        the clan with these elements already exists in it, or a 
        freshly constructed one otherwise. 
        Possibly elems is any iterable, materialized at sorting.
        '''
        elems = sorted(elems, key = lambda e: e.name) # always a list
        assert len(elems) > 1
        name = '(' + SEP.join( e.name for e in elems ) + ')' # might be empty
        if name in self:
            return self[name]
        cl = Clan(name, elems, color)
        self[name] = cl
        return cl


    def sgton(self, item):
        '''
        Only place where singleton clans are created.
        Return a singleton clan out of the pool if already
        exists in it, or a freshly constructed one.
        '''
        name = delbl(item) 
        if name in self:
            return self[name]
        cl = Clan(name, [ item ])
        cl.is_sgton = True
        self[name] = cl
        return cl


    def how_seen(self, source, target):
        '''
        Color with which the target clan is seen from the 
        source clan, if any; colors are stored here under 
        a +2 increment so that original colors count from 
        2 up. A 1 is stored to signal that clans are not 
        visible from each other and, as EZGraph is a ddict 
        of Counter, 0 signals that we still don't have a 
        color recorded and must check the graph. Most +2/-2 
        noise confined to this particular function but a bit
        left in Clan.add(). Caveat: would be good to refactor 
        that. Answer from here is never -2.
        '''
        s_nm, t_nm = min(source.name, target.name), max(source.name, target.name)
        guess = self.visib[s_nm][t_nm] - 2 
        if guess > -2:
            "otherwise, set it up correctly and only then return it"
            return guess
        if len(source) < len(target):
            "make sure source is not longer than target"
            source, target = target, source
        if source.is_sgton:
                '''
                then target too, fall back into the graph, items to 
                test are first and only elements of the singletons
                '''
                s_it, t_it = min(source[0], target[0]), max(source[0], target[0])
                self.visib.new_edge(s_nm, t_nm, self.graph[s_it][t_it] + 2)
        else:
            "at least 2 subclans in source, traverse them"
            c = None
            for subclan in source:
                d = self.how_seen(subclan, target)
                if c is None:
                    "first color found, could be -1 or not"
                    c = d
                if c != d or d == -1:
                    "two different colors found at some recursion depth"
                    c = -1
                    break
            self.visib.new_edge(s_nm, t_nm, c + 2)
        return self.visib[s_nm][t_nm] - 2


    def _add_clan(self, gvgraph, clan):
        '''
        Add the whole subtree below that nonsingleton clan to the 
        Graphviz graph. Thus, both a big clan node plus a point-shaped 
        stand-in are to be added. Returns cluster and headnode names.
        Rather ugly. Version on top of python3-gv much better but not 
        available for Windows.
        '''
        clus_contents = list()
        clus_name = "CL_" + clan.name
        fl = dict()
        if len(clan) <= 2 or clan.color == 0:
            '''
            flatten the cluster 
            (caveat: some more flattening cases should be added)
            '''
            fl["rank"] = "same"
        with gvgraph.subgraph(name = clus_name,
                graph_attr = { "cluster": "true" } | fl,
                node_attr = { "shape": "point" }) as the_subgraph:
            "gather back the subtree points"
            for subclan in sorted(clan, key = len, reverse = True):
                if subclan.is_sgton:
                    subhead = subclan.name
                    gvgraph.node(subhead)
                    stand_in = "PT_" + subhead
                    subclus = None
                else:
                    subclus, subhead = self._add_clan(gvgraph, subclan)
                    stand_in = "PT_" + subclan.name
                the_subgraph.node(stand_in, shape = 'point')
                clus_contents.append( 
                            (subclan, stand_in, subclus, subhead) )
        clus_contents = sorted(clus_contents, 
                               key = lambda cl: cl[0].name)
        # singletons have been sorted also there
        # identify own head node
        if clan.color == 0:
            "will be flattened, aim at near middle"
            headnode = clus_contents[(len(clan)+1) // 2][1]
        else:
            "aim at the alpha-earliest, which will be on top"
            headnode = clus_contents[0][1]

        for (subclan, stand_in, subclus, subhead) in clus_contents:
            "connect stand_in with subclus"
            if subclan.is_sgton:
                gvgraph.edge(stand_in, subhead, arrowhead = "none")
            else:
                gvgraph.edge(stand_in, subhead, arrowhead = "none",
                             lhead = subclus,   # cluster as head
                             penwidth = "1.3")  # slightly thicker

        for (left,  left_stand_in,  _, _), \
            (right, right_stand_in, _, _)  \
            in comb(clus_contents, 2):
                "Set up colored edges inside current cluster"
                if ((hs := self.how_seen(left, right)) <
                    len(self.palette)): 
                        color = self.palette[hs]
                else:
                    print("Sorry. Too high class numbers", 
                          "or not enough colors.")
                    exit()
                gvgraph.edge(left_stand_in, right_stand_in, 
                    arrowhead = "none", color = color,
                    penwidth = "2.0") # double thickness

        return clus_name, headnode


        # ~ gv-based code:
        # ~ if clan.is_sgton:
            # ~ headnode = gv.node(gvgraph, clan[0])
        # ~ else:
            # ~ "gather back the subtree points"
            # ~ the_subgraph = gv.graph(gvgraph, "CL_" + clan.name)
            # ~ the_nodes = list()
            # ~ sortedclans = list()
            # ~ for subclan in sorted(clan, key = len, reverse = True):
				# ~ "Very unclear how to handle the recursive call - CAVEAT, BLOCKED HERE"
                # ~ the_nodes.append(self._add_clan(gvgraph, subclan))
                # ~ sortedclans.append(subclan)
            # ~ if clan.color == 0:
                # ~ "will be flattened, aim at near middle"
                # ~ headnode = the_nodes[(len(clan)+1) // 2]
            # ~ else:
                # ~ "aim at the alpha-earliest, which will be on top"
                # ~ posmin = min(range(len(sortedclans)), key = lambda pos: sortedclans[pos].name)
                # ~ headnode = the_nodes[posmin]
            # ~ clus_contents = list(zip(sortedclans, the_nodes))
            # ~ _ = gv.setv(the_subgraph, "cluster", "true")
            # ~ for node in the_nodes:
                # ~ _ = gv.node(the_subgraph, gv.nameof(node))
            # ~ for left in clus_contents:
                # ~ "had to be materialized in order to do double traversal"
                # ~ for right in clus_contents:
                    # ~ "Set up edges"
                    # ~ if left[0].name < right[0].name:
                        # ~ if ((hs := self.how_seen(left[0], right[0])) <
                            # ~ len(self.palette)): 
                                # ~ color = self.palette[hs]
                        # ~ else:
                            # ~ print("Sorry. Too high class numbers", 
                                  # ~ "or not enough colors.")
                            # ~ exit()
                        # ~ ed = gv.edge(left[1], right[1])
                        # ~ _ = gv.setv(ed, "arrowhead", "none")
                        # ~ _ = gv.setv(ed, "penwidth", "2.0") # double thickness
                        # ~ _ = gv.setv(ed, "color", color)
            # ~ if len(clan) <= 2 or clan.color == 0:
                # ~ "flatten the cluster - caveat: some more flattening cases should be added"
                # ~ _ = gv.setv(the_subgraph, "rank", "same")
        # ~ stand_in = None
        # ~ if not is_root:
            # ~ stand_in = gv.node(gvgraph, 'PT_' + clan.name)
            # ~ _ = gv.setv(stand_in, "shape", "point")
            # ~ local_edge = gv.edge(stand_in, headnode) # cluster as head
            # ~ _ = gv.setv(local_edge, "arrowhead", "none")
            # ~ _ = gv.setv(local_edge, "penwidth", "1.3") # slightly thicker
            # ~ if not clan.is_sgton:
                # ~ _ = gv.setv(local_edge, "lhead", gv.nameof(the_subgraph))
        # ~ return stand_in


    def draw(self, root, name):
        gvgraph = gvz.Digraph(name, graph_attr = { "compound": "true", "newrank": "true" })
        if root.is_sgton:
            gvgraph.node(root[0].name)
        else:
            self._add_clan(gvgraph, root)

        # ~ gv-based code:
        # ~ gvgraph = gv.strictdigraph(name) # a graph handle
        # ~ gv.setv(gvgraph, "compound", "true") # o/w renderer with clusters fails
        # ~ gv.setv(gvgraph, "newrank", "true") # o/w rank=same in flattening doesn't work
        # ~ self._add_clan(gvgraph, root, is_root = True)
        # ~ ok = gv.layout(gvgraph, "dot")
        # ~ if not ok:
            # ~ print("Layout failed for", name)
            # ~ exit()
        # ~ ok = gv.render(gvgraph, "dot", name + ".gv")
        # ~ if not ok:
            # ~ print("Render failed for", name + ".gv")
            # ~ exit()

