from ezGraph import EZGraph

class DecTree(dict):
    '''
    Dict keeps all the clans that get created along, with their
    names as keys. Only part of them belong to the tree but the
    splitting may fish back in an older clan and we do not want
    to recreate it with all its visibility properties already
    known.

    This class keeps as well the visibility graph recording all
    colors between clan names.

    A separate variable will be recording the current root at
    all times. Only clans reachable from there are actually 
    part of the current tree.
    '''

    def __init__(self):
        super().__init__(self)
        self.visib = EZGraph()
        
    def store_clan(self, clan):
        self[clan.name] = clan

    def how_seen(self, source, target, graph):
        '''
        Color with which the target clan is seen from the 
        source clan, if any; colors are stored here under 
        a +2 increment so that original colors count from 
        2 up. A 1 is stored to signal that clans are not 
        visible from each other and, as EZGraph is a ddict 
        of Counter, 0 signals that we still don't have a 
        color recorded and must check the graph. 
        If one is a 
        '''
        p, q = min(source.name, target.name), max(source.name, target.name)
        guess = self.visib[p][q] - 2 
        print(' ... ... visibility guess', p, q, guess)
        if guess > -2:
            return guess
        if len(source) < len(target):
            "make sure target is not longer than source"
            source, target = target, source_synopsis
        if target.is_sgton:
                "then source too, fall back into the graph"
                self.visib[p][q] = graph[p][q]
        else:
            "at least 2 subclans of target, traverse them"
            c = None
            for subclan in target:
                d = self.how_seen(source, subclan, graph)
                # ~ if c is not None :
                    # ~ c = d
                # ~ elif c != d:
                    # ~ "two different colors found, maybe one was -1"
                    # ~ c = -1
                    # ~ break            

# ~ MUST THINK THAT OUT MORE CAREFULLY !!!


            if c == -1:
                print(' ... ... not seen', source.name, target.name)
            self.visib.new_edge(source, target, c) # PENDING TO HANDLE CORRECTLY
            







        if self.is_sgton:
            p, q = min(item, self[0]), max(item, self[0])
            return graph[p][q]

        # test whether already found out earlier, -2 if not
            if guess not in [-2, -1]:
                print(' ... ... repeated and wrong', item, self.name, -1, guess)
            if guess == -1:
                print(' ... ... repeated', item, self.name, -1, guess)
            return -1
        else:
            for c in v:
                'loop grabs the single element'
                if guess not in [-2, c]:
                    print(' ... ... repeated and wrong', item, self.name, c, guess)
                if guess == c:
                    print(' ... ... repeated', item, self.name, c, guess)
                print(' ... ... seen', self, item, c)
                self.visib.new_edge(self.name, item, c + 2, 'how_seen_seen')
                return c

