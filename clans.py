from ezGraph import SEP # , EZGraph
from auxfun import delbl
from collections import Counter, defaultdict as ddict

class Clan(list):
    '''
    A clan is a list of subclans plus a name and a singleton flag. 

    They could be alternatively sets. I set up a GitHub issue
    about that.

    Singleton clans consist of a single vertex. They are created 
    separately and marked as such with the flag.

    Clan names get added as vertices to the underlying graph.
    Might need a separate dict to get them back from their names.

    In complete clans, self.color indicates the color.
    Primitive clans have self.color == -1.
    Also singleton clans, just to avoid checking an
    undefined value.
 
    Clans might get also later a visibility dict. Current plan
    is that they map items to further color visibility dicts: 
    in turn, these map non-negative colors to lists of their 
    visible subclans. For the time being, all visibility
    issues are handled on local variables but the clan names
    get added to the graph to maintain their visibility info.
    '''

    def __init__(self, elems = [], color = -1): #, prototype = None):
        super().__init__(self)
        self.extend(elems)
        self.name = SEP.join( e.name for e in elems ) # might be empty
        self.color = color
        self.is_sgton = False
        # ~ self.prototype = prototype

    def __str__(self):
        return (super().__str__() + " {"
            # ~ + "prot:" + str(self.prototype) 
            + "name:" + self.name 
            + "; color:" + str(self.color) + "}")

    def sgton(self, item):
        'Creates a singleton clan'
        assert len(self) == 0
        self.append(item)
        self.name = delbl(item)
        self.is_sgton = True
        # ~ self.prototype = item

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
        Color found is stored as a new edge of the graph.
        '''
        if self.is_sgton:
            # ~ print(' ... seen', self, item, graph[item][self[0]])
            return graph[item][self[0]]
        v = ddict(int)
        for subclan in self:
            v[subclan.how_seen(item, graph)] += 1
        if -1 in v or len(v) > 1:
            # ~ print(' ... seen', self, item, -1)
            graph.new_edge(item, subclan.name, -1)
            return -1
        else:
            for c in v:
                'loop grabs the single element'
                # ~ print(' ... seen', self, item, c)
                graph.new_edge(item, subclan.name, c)
                return c
            

    def add(self, item, graph):
        '''
        Adds item to the clan, assumed to be a root, and returns
        a new root, possibly the same; uses graph to check colors 
        so as to apply the correct case. 
        '''
        item_cl = Clan()
        item_cl.sgton(item)

        if self.is_sgton:
            'second item, new root with both'
            # ~ print(' ... second item', item)
            return Clan([self, item_cl], graph[item][self[0]]) #, item)

        # Set up subclan visibility lists, by colors, -1 for not visible subclans
        # They contain POSITIONS of the clan list, not the subclans proper
        visib = ddict(list)
        somecolor = -2 # some color different from self.color if one such appears 
        for pos, subclan in enumerate(self):
            'len(self) > 1 here'
            visib[somec := subclan.how_seen(item, graph)].append(pos)
            if somec != self.color and somecolor == -2:
                somecolor = somec
        selfc = visib[self.color]

        # Case analysis
        if len(self) == len(selfc):
            'case 1a: item sees everything in self in the color of self'
            print(' ... 1a')
            self.append(item_cl)
            return self

        if 0 < len(selfc) < len(self):
            '''
            case 1b: some, but not all, seen as self.color, then clan
            reduces to these, recursive call on new clan with the rest.
            '''
            print(' ... 1b')
            to_new_cl_pos = sorted(set(range(len(self))).difference(selfc), 
                                   reverse = True)
            to_new_cl = list()
            # ~ print(' ...clan', self)
            for pos in to_new_cl_pos:
                # ~ print(' ...switching pos', pos, self[pos])
                to_new_cl.append(self[pos])
                del self[pos]
            new_cl = Clan(to_new_cl, self.color)
            # ~ print(' ...new_cl auxiliar', new_cl)
            # ~ print(' ...reduced clan', self)
            new_cl = new_cl.add(item, graph) # recursive call
            self.append(new_cl)
            return self

        if len(self) == len(visib[somecolor]):
            '''
            case 1c: all same color but different from self.color, 
            seems a particular case of 1b but subtly different
            because no clans would remain in self;
            might encompass case 2c and/or the init case of sgton self
            also: somecolor might still be -2 w/ len zero != len(self)
            '''
            print(' ... 1c', item, somecolor, visib[somecolor])
            return Clan([self, item_cl], somecolor)





'''
Planned to subclass but now I find it is likely to be overkill.

class PrimClan(Clan):
    pass

class ComplClan(Clan):
    pass
'''
