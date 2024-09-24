from ezGraph import EZGraph

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
    '''

    def __init__(self, graph):
        super().__init__(self)
        self.visib = EZGraph()
        self.graph = graph # the data/input Gaifman graph

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

