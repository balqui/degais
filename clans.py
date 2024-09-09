from collections import Counter, defaultdict as ddict

class Clan(list):
    '''
    A clan is a list of subclans plus a prototype item taken 
    from one of the subclans. "Colors" relating clans are 
    found out by checking the edge connecting the prototypes 
    in the original graph.
    
    Could be a set instead of a list but a list will enable
    easy extension to linear clans in the future, if convenient.
    
    Inherits __init__ so we get an empty list.
    
    Singleton clans are created separately.
    
    In complete clans, self.color indicates the color.
    Primitive clans have self.color == -1.
    Singleton clans don't have a color value.
    
    Clans get also a visibility dict mapping items to their 
    color visibility dicts: these map non-negative colors 
    to lists of their visible subclans; non-visible clans 
    are listed under color -1.
    '''


    def __str__(self):
        return (super.__str__(self) + 
              " {prot:" + self.prototype + ";color:" + str(self.color) + "}")


    def sgton(self, item):
        'Creates a singleton clan'
        assert len(self) == 0
        self.append(item)
        self.prototype = item


    def init(self, a, b, color):
        'Given two clans, creates a new clan with two elements'
        assert len(self) == 0
        self.append(a)
        self.append(b)
        self.prototype = a.prototype
        self.color = color
        self.visib_dict = ddict(ddict)


    def visib(self, item, graph):
        '''
        Constructs visibility dict for item if necessary and returns it
        '''
        assert len(self) > 1
        if not self.visib_dict[item]:
            v = ddict(list)
            for subclan in self:
                if ls := len(subclan) == 1:
                    v[graph[subclan.prototype][item]].append(subclan)
                else: 
                    v = subclan.visib(item, graph)
                    # ~ what now?
            self.visib_dict[item] = v
        return self.visib_dict[item]

    def add(self, item, graph):
        '''
        Adds item to the clan, assumed to be a root, and returns
        a root, possibly different; checks for colors in the graph
        so as to apply the correct case. 
        '''
        new_cl = Clan()
        new_cl.sgton(item)

        # Set up subclan visibility lists        
        v = self.visib(item, graph)

        # Case analysis
        for col in v:
            'does item see everything in self in the same color?'
            if len(v[col]) == len(self):
                break
        else:
            col = -1

        if self.color >= 0 and self.color == col:
            'complete clan of that color, case 1a'
            self.append(new_cl)
            return self
        if col >= 0:
            'all same color but different from self.color, cases 1b and 2c(?)'
            new_root = Clan()
            new_root.init(self, new_cl, col)
            return new_root



        return self # might as well be a new root



'''
Planned to subclass but now I find it is likely to be overkill.

class PrimClan(Clan):
    pass

class ComplClan(Clan):
    pass
'''
