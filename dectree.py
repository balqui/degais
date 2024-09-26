from ezGraph import EZGraph
import gv # official Python bindings to Graphviz, apt install python3-gv

class DecTree(dict):
    '''
    The dict keeps all the clans that get created along, with their
    names as keys. Only part of them belong to the tree but the
    splitting may fish back in an older clan and we do not want
    to recreate it with all its visibility properties already
    known. The price is that adding an item to a clan (like in 
    case 1a of Clan.add() and such) requires making a duplicate, 
    then updating it. Caveat: worth it?

    This class keeps as well the visibility graph recording all
    colors between clan names.

    A separate variable will be recording the current root at
    all times. Only clans reachable from there are actually 
    part of the current tree.

    Caveat: palette as originally designed by Ely, must be 
    reconsidered at some point.
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

    def store_clan(self, clan):
        "caveat: it may be there already, consistently or not"
        if clan.name in self:
            print(" +++ WARNING: clan name", clan.name, "changed from", self[clan.name], "to", clan) 
        self[clan.name] = clan
        return clan.name

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
        left in add().
        '''
        print(' ... ... how seen', source, target, source.is_sgton, target.is_sgton)
        s_nm, t_nm = min(source.name, target.name), max(source.name, target.name)
        guess = self.visib[s_nm][t_nm] - 2 
        print(' ... ... visibility guess', s_nm, t_nm, guess)
        if guess > -2:
            "otherwise, set it up correctly and only then return it"
            return guess
        # print(' ... ... will swap?', source, target, len(source), len(target))
        if len(source) < len(target):
            "make sure source is not longer than target"
            source, target = target, source
        # print(' ... ... did swap?', source, target)
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
            if c == -1:
                print(' ... ... not seen', source.name, target.name)
            else:
                print(' ... ... seen', source.name, target.name, c)
            self.visib.new_edge(s_nm, t_nm, c + 2)
        return self.visib[s_nm][t_nm] - 2


    def _add_clan(self, gvgraph, clan, is_root = False):
        '''
        Add the whole subtree below that clan to the Graphviz graph,
        return the node handle for the point that represents the clan.
        Caveat: flattening applied to complete clans of color 0,
        this should depend on whether that color is to be left undrawn, 
        not yet decided how to find out that. Affects self.palette[0].
        Must add a big clan node or singleton plus a stand-in.
        '''
        print(" +++ Adding clan:", clan)
        print(" +++ Currently in graph:")
        sss = gv.firstsubg(gvgraph)
        while gv.ok(sss):
            print(" +++", gv.nameof(sss))
            sss = gv.nextsubg(gvgraph, sss)
        if clan.is_sgton:
            headnode = gv.node(gvgraph, clan[0])
        else:
            "gather back the subtree points"
            the_nodes = list()
            for subclan in clan:
                "one of them (e.g. first) taken to receive the edge head"
                the_nodes.append(self._add_clan(gvgraph, subclan))
            headnode = the_nodes[0]
            clus_contents = zip(clan, the_nodes)
            print(" +++ In clus_contents, zip of:")
            print(" +++ +++", list(cl.name for cl in clan))
            print(" +++ +++", list(gv.nameof(cl) for cl in the_nodes))
            for left in clus_contents:
                for right in clus_contents:
                    "Set up edges"
                    if left[0].name < right[0].name:
                        ed = gv.edge(left[1], right[1])
                        _ = gv.setv(ed, "arrowhead", "none")
                        _ = gv.setv(ed, "penwidth", "2.0") # double thickness
                        _ = gv.setv(ed, "color", 
                            self.palette[self.how_seen(left[0], right[0])])
            the_subgraph = gv.graph(gvgraph, "C_" + clan.name)
            _ = gv.setv(the_subgraph, "cluster", "true")
            if len(clan) <= 2 or clan.color == 0:
                "flatten the cluster"
                _ = gv.setv(the_subgraph, "rank", "same")
                print(" +++ Flattened", clan)
        stand_in = None
        if not is_root:
            stand_in = gv.node(gvgraph, 'PT_' + clan.name)
            _ = gv.setv(stand_in, "shape", "point")
            local_edge = gv.edge(stand_in, headnode)
            _ = gv.setv(local_edge, "arrowhead", "none")
            _ = gv.setv(local_edge, "penwidth", "1.3") # slightly thicker
            if not clan.is_sgton:
                _ = gv.setv(local_edge, "lhead", gv.nameof(the_subgraph))
        return stand_in


    def draw(self, root, name):
        gvgraph = gv.strictdigraph(name) # a graph handle
        gv.setv(gvgraph, "compound", "true") # o/w renderer with clusters fails
        _ = self._add_clan(gvgraph, root, is_root = True)
        ok = gv.write(gvgraph, name + "_PRE_layout.gv")
        print("First write answer:", ok)
        ok = gv.layout(gvgraph, "dot")
        print("Layout answer:", ok)
        ok = gv.write(gvgraph, name + "_POST_layout.gv")
        print("Second write answer:", ok)
        ok = gv.render(gvgraph, "dot", name + ".gv")
        print("Render answer:", ok)
        # ~ ok = gv.write(gvgraph, "dot")
        # ~ if not ok:
            # ~ print("Layout failed.")
            # ~ exit()
        # ~ ok = gv.layout(gvgraph, "dot")
        # ~ if not ok:
            # ~ print("Layout failed.")
            # ~ exit()
        # ~ ok = gv.render(gvgraph, "dot", name + ".gv")
        # ~ if not ok:
            # ~ print("Render failed.")
