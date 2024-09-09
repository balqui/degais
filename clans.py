from collections import Counter, defaultdict as ddict

class Clan(list):
    '''
    A clan is a list of subclans plus a prototype item taken 
    from one of the subclans. "Colors" relating clans are 
    found out by checking the edge connecting the prototypes 
    in the original graph. 
    
    Could be a set instead of a list; but a list will enable
    easy extension to linear clans in the future, if convenient.
    
    Inherits __init__ so we get an empty list.
    
    Singleton clans are created separately.
    
    In complete clans, self.color indicates the color.
    Primitive clans have self.color == -1.
    Also singleton clans, just to avoid checking an
    undefined value.
 
    Clans might get also a visibility dict. Current plan is
    that they map items to further color visibility dicts: 
    in turn, these map non-negative colors to lists of their 
    visible subclans.
    '''

    def __init__(self, elems = [], color = -1, prototype = None):
        super().__init__(self)
        self.extend(elems)
        self.color = color
        self.prototype = prototype

    def __str__(self):
        return (super().__str__()
            + " {prot:" + str(self.prototype) + "; color:" + str(self.color) + "}")


    def sgton(self, item):
        'Creates a singleton clan'
        assert len(self) == 0
        self.append(item)
        self.prototype = item

# Plan was to initialize with size-two clans but that will not
# work well with recursive calls where an item is added to a sgton.
# Thus, the second node is added using method add.

    # ~ def init(self, a, b, color):
        # ~ 'Given two clans, creates a new clan with two elements'
        # ~ assert len(self) == 0
        # ~ self.append(a)
        # ~ self.append(b)
        # ~ self.prototype = a.prototype
        # ~ self.color = color
        # ~ self.visib_dict = ddict(ddict)

# Unclear how to do all this. Postponed.
    # ~ def visib(self, item, graph):
        # ~ '''
        # ~ Constructs visibility dict for item if necessary and returns it
        # ~ '''
        # ~ assert len(self) > 1
        # ~ if not self.visib_dict[item]:
            # ~ v = ddict(list)
            # ~ for subclan in self:
                # ~ if ls := len(subclan) == 1:
                    # ~ v[graph[subclan.prototype][item]].append(subclan)
                # ~ else: 
                    # ~ v = subclan.visib(item, graph)
                    # what now?
            # ~ self.visib_dict[item] = v
        # ~ return self.visib_dict[item]

    def how_seen(self, item, graph):
        '''
        Graph color with which the clan is seen from item,
        if any; -1 otherwise, signals not visible.
        '''
        if len(self) == 1:
            '''
            must be a singleton with item as prototype (but 
            self[0] should allow us to get rid of the prototype)
            '''
            return graph[item][self.prototype]
        v = ddict(int)
        for subclan in self:
            v[subclan.how_seen(item, graph)] += 1
        if -1 in v or len(v) > 1:
            return -1
        else:
            for c in v:
                'loop grabs the single element'
                return c
            

    def add(self, item, graph):
        '''
        Adds item to the clan, assumed to be a root, and returns
        a new root, possibly the same; uses graph to check colors 
        so as to apply the correct case. 
        '''
        new_cl = Clan()
        new_cl.sgton(item)

        if len(self) == 1:
            'new root with both'
            return Clan([self, new_cl], graph[item][self.prototype], self.prototype)

        # Set up subclan visibility lists, by colors, -1 for not visible subclans
        visib = ddict(list)
        for subclan in self:
            'len(self) > 1 here'
            visib[subclan.how_seen(item, graph)].append(subclan)

        # Case analysis
        if len(self) == len(visib[self.color]):
            'case 1a: item sees everything in self in the color of self'
            self.append(new_cl)
            return self

        if len(self) == len(visib[graph[item][self.prototype]]):
            '''
            case 1b: all same color but different from self.color, 
            might encompass case 2c and init case of singleton self, 
            might be encompassed by cases 1c or 1d
            '''
            return Clan([self, new_cl], graph[item][self.prototype], self.prototype)



        return self # might as well be a new root



'''
Planned to subclass but now I find it is likely to be overkill.

class PrimClan(Clan):
    pass

class ComplClan(Clan):
    pass
'''
