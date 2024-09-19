from ezGraph import SEP, EZGraph
from auxfun import delbl
from collections import Counter, defaultdict as ddict

class Clan(list):
    '''
    A clan is a list of subclans plus a name and a singleton flag.
    Clan names start always with an asterisk '*'.

    They could be alternatively sets. I set up a GitHub issue
    about that.

    Singleton clans consist of a single vertex. They are created 
    separately and marked as such with the flag.

    In complete clans, self.color indicates the color.
    Primitive clans have self.color == -1.
    Also singleton clans, just to avoid checking an
    undefined value.

    Clan objects share a sort-of-static common graph where
    clan names get added as vertices to record their visibility.
    As zero is a valid color of the input graph but here zero
    means no information, and -1 represents "not visible", 
    colors are coded by adding 2 to the integer value instead. 
    These decisions supersede plans about visibility 
    dicts: all visibility issues are handled on local variables 
    and then the info gets added to the shared graph.
    '''

    visib = EZGraph()

    def __init__(self, elems = [], color = -1): #, prototype = None):
        '''
        As elems is traversed repeatedly and can be an iterator,
        need to materialize first.
        '''
        elems = list(elems) 
        super().__init__(self)
        self.extend(elems)
        self.name = '*' + SEP.join( e.name for e in elems ) # might be empty
        self.color = color
        self.is_sgton = False
        print(" ... created", self.name, "with elems /", elems, "/")

    def __str__(self):
        return (super().__str__() + " {"
            + "name:" + self.name 
            + "; color:" + str(self.color) + "}")

    def sgton(self, item):
        'Creates a singleton clan'
        assert len(self) == 0
        self.append(item)
        self.name = '*' + delbl(item)
        self.is_sgton = True
        print(' ... sgton name:', self.name, item)

# The second node is added using method add.


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
        PENDING: check first on local visib graph before 
        deepening, just in case.
        Caveat: Seems to work now, refactor when sure.
        Caveat: Maybe instead of item it should be any clan... ?
        '''
        if self.is_sgton:
            p, q = min(item, self[0]), max(item, self[0])
            print(' ... ... seen', self, p, q, graph[p][q])
            return graph[p][q]
        # test whether already found out earlier, -2 if not
        guess = self.visib[self.name][item] - 2 
        v = ddict(int)
        for subclan in self:
            v[subclan.how_seen(item, graph)] += 1
        if -1 in v or len(v) > 1:
            print(' ... ... not seen', self, item, -1, list(v.keys()))
            self.visib.new_edge(self.name, item, 1)
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
                self.visib.new_edge(self.name, item, c + 2)
                return c


    def _color_lists(self, item, graph):
        '''
        With complete in mind. Caveat: changes for primitive?
        '''
        v = ddict(list)
        for subclan in self:
            col = subclan.how_seen(item, graph)
            self.visib.new_edge(subclan.name, item, col + 2)
            v[col].append(subclan, self.color)
        return v


    def split(self, item, out_clans = list()):
        '''
        With complete in mind. Caveat: changes for primitive?
        '''
        v = self._color_lists(item)
        for color in v:
            pass # think this out again very carefully

            # ~ if len(v[color]) == 1:
                # ~ 'must add new edge item - v[color][0] of color color'
                # ~ out_clans.append(v[color][0])
            # ~ else:
                # ~ 'must add new edges, which ones?'
                # ~ out_clans.append(Clan(v[color], dontknowwhichcoloryet))




        # ~ return Clan(out_clans, dontknowwhichcoloreither)


        # ~ pending = v[-1] # "not seen" from item: those will be taken 
        # ~ v[-1] = list()  #  care of next, so don't split them again later
        # ~ for subclan in pending:
            # ~ subclan.color_lists(item, graph, v)



    def add(self, item, graph):
        '''
        Adds item to the clan, assumed to be a root, and returns
        a new root, possibly the same; uses graph to check colors 
        so as to apply the correct case. 
        '''
        if self.is_sgton:
            'second item, new root with both'
            print(' ... ... second item', item, 'for', self[0])
            item_cl = Clan()
            item_cl.sgton(item)
            return Clan([self, item_cl], graph[min(item, self[0])][max(item, self[0])]  )

        # Set up subclan visibility lists, by colors, -1 for not visible subclans
        # They contain POSITIONS of the clan list, not the subclans proper
        visib_dict = ddict(list)
        somecolor = -2 # some color different from self.color if one such appears 
        for pos, subclan in enumerate(self):
            'len(self) > 1 here'
            visib_dict[somec := subclan.how_seen(item, graph)].append(pos)
            if -1 < somec != self.color and somecolor == -2:
                "if all are -1 then we may get in trouble"
                somecolor = somec
        selfc = visib_dict[self.color]

        # Case analysis, selfc > -1 iff complete clan
        if self.color > -1 and len(self) == len(selfc):
            'case 1a: item sees everything in self in the color of self'
            print(' ... 1a')
            self.visib.new_edge(self.name, item, self.color + 2)
            item_cl = Clan()
            item_cl.sgton(item)
            self.append(item_cl) # not fiddling with the name yet, should we?
            return self

        if self.color > -1 and 0 < len(selfc): # < len(self) o/w 1a
            '''
            case 1b: some, but not all, seen as self.color, then clan
            reduces to these, recursive call on new clan with the rest.
            '''
            print(' ... 1b')

            # current solution: self is left alone, two new clans are created
            rest_pos = list(set(range(len(self))).difference(selfc))
            print(' ... same color:', list(self[pos].name for pos in selfc))
            print(' ... rest:', list(self[pos].name for pos in rest_pos))
            if len(rest_pos) == 1:
                "caveat: make sure I want this instead of checking for singleton"
                cl_rest = self[rest_pos[0]]
            else:
				"caveat: this Clan may already exist, created along"
                cl_rest = Clan((self[pos] for pos in rest_pos), self.color)
            cl_rest = cl_rest.add(item, graph) # recursive call
            cl_same_c = Clan((self[pos] for pos in selfc), self.color) 
            self.visib.new_edge(cl_same_c.name, item, self.color + 2)
            cl_same_c.append(cl_rest) # not fiddling with the name yet, should we?
            return cl_same_c

            # earlier solution: self is reduced and one new clan is created
            # ~ to_new_cl_pos = sorted(set(range(len(self))).difference(selfc), 
                                   # ~ reverse = True)
            # ~ to_new_cl = list()
            # ~ print(' ...clan', self)
            # ~ for pos in to_new_cl_pos:
                # ~ print(' ...switching pos', pos, self[pos])
                # ~ to_new_cl.append(self[pos])
                # ~ del self[pos]
            # ~ new_cl = Clan(to_new_cl, self.color)
            # ~ print(' ...new_cl auxiliar', new_cl)
            # ~ print(' ...reduced clan', self)
            # ~ new_cl = new_cl.add(item, graph) # recursive call
            # ~ self.append(new_cl)
            # ~ return self

        if len(self) == len(visib_dict[somecolor]): # if self.color > -1 then 1c, o/w 2b
            '''
            case 1c: all same color but different from self.color, 
            seems a particular case of 1b but subtly different
            because no clans would remain in self, all in rest,
            recursive call would not reduce size;
            might encompass case 2c and/or the init case of sgton self, think.
            Covers 2b as well when self is primitive.
            Also: somecolor might still be -2 w/ len zero != len(self).
            '''
            if self.color == -1:
                print(' ... 2b', item, somecolor, visib_dict[somecolor], len(self))
            else:
                print(' ... 1c', item, somecolor, visib_dict[somecolor], len(self))
            self.visib.new_edge(self.name, item, somecolor + 2)
            item_cl = Clan()
            item_cl.sgton(item)
            return Clan([self, item_cl], somecolor)

        if self.color > -1:
            '''
            case 1d: negations of previous conditions lead to:
            either some are nonvisible, maybe all, 
            or at least 2 different colors present.
            '''

        # ~ if len(visib_dict[-1]):
            # ~ return Clan(self.split(item).append(item), -1) # mark as primitive





        
        
        print('Unhandled case', visib_dict, self.color, somecolor) # at end, should not happen

        # ~ # Alternative approach, starts by calling colorlists.
        # ~ vlists = self.color_lists(item, graph)

        # ~ split_clans = list()
        # ~ nonempty = set()
        # ~ for color in vlists:
            # ~ if len(vlists[color]):
                # ~ nonempty.add(color)
            # ~ if len(vlists[color]) == 1:
                # ~ split_clans.append(vlists[color][0][0]) # first half of single member
            # ~ else:
                # ~ '''
                # ~ Caveat: A subclan of a primitive clan might be complete,
                # ~ so second parameter likely to be wrong in certain cases.
                # ~ ALSO caveat: In mapping here case 1a we do not join 
                # ~ them all into a single clan.
                # ~ '''
                # ~ split_clans.append(Clan((pair[0] for pair in vlists[color]), vlists[color][0][1]))
        




