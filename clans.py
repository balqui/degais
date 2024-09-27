from ezGraph import SEP, EZGraph
from auxfun import delbl
from collections import Counter, defaultdict as ddict

class Clan(list):
    '''
    A clan is a list plus a name and a singleton flag.
    Clan names start always with an asterisk '*'.
    (Caveat: THAT MUST CHANGE.)
    In nonsigleton clans, the list contains subclans.

    (They could be alternatively sets. I set up a GitHub issue
    about that.)

    Singleton clans consist of a single vertex. They are created 
    separately and marked as such with the flag. The single
    element of the list is the item.

    In complete clans, self.color indicates the color.
    Primitive clans have self.color == -1.
    Also singleton clans, just to avoid checking an
    undefined value.

    Formerly, clan objects shared a sort-of-static common graph 
    which has now been moved to the DecTree class. There,
    clan names get added as vertices to record their visibility.
    As zero is a valid color of the input graph but here zero
    means no information, and -1 represents "not visible", 
    colors are coded by adding 2 to the integer value instead. 
    These decisions supersede plans about visibility 
    dicts: all visibility issues are handled through the
    visibility graph in the DecTree.
    '''

    # ~ visib = EZGraph()

    def __init__(self, elems = [], color = -1):
        '''
        As elems is traversed repeatedly and can be an iterator,
        need to materialize first.
        Asterisk chosen for being smaller than any letter or digit.
        Caveat: THAT MUST CHANGE.
        Names are immutable surrogates of clans for use in dicts like
        the visibility graph.
        '''
        elems = list(elems) 
        super().__init__(self)
        self.extend(elems)
        self.name = '*' + SEP.join( e.name for e in elems ) # might be empty
        self.color = color
        self.is_sgton = False
        print(" ... created", self.name, "with elems /", elems, 
              "/ color", color)

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

    # ~ def how_seen(self, item, graph):
        # ~ '''
        # ~ Graph color with which the clan is seen from item,
        # ~ if any; -1 otherwise, signals not visible.
        # ~ Color found is stored as a new edge of the graph.
        # ~ PENDING: check first on local visib graph before 
        # ~ deepening, just in case.
        # ~ Caveat: Seems to work now, refactor when sure.
        # ~ Caveat: Maybe instead of item it should be any clan... ?
        # ~ '''
        # ~ if self.is_sgton:
            # ~ p, q = min(item, self[0]), max(item, self[0])
            # ~ print(' ... ... seen', self, p, q, graph[p][q])
            # ~ return graph[p][q]

        # ~ # test whether already found out earlier, -2 if not
        # ~ guess = self.visib[self.name][item] - 2 
        # ~ v = ddict(int)
        # ~ for subclan in self:
            # ~ v[subclan.how_seen(item, graph)] += 1
        # ~ if -1 in v or len(v) > 1:
            # ~ print(' ... ... not seen', self, item, -1, list(v.keys()))
            # ~ self.visib.new_edge(self.name, item, 1, 'how_seen_not_seen')
            # ~ if guess not in [-2, -1]:
                # ~ print(' ... ... repeated and wrong', item, self.name, -1, guess)
            # ~ if guess == -1:
                # ~ print(' ... ... repeated', item, self.name, -1, guess)
            # ~ return -1
        # ~ else:
            # ~ for c in v:
                # ~ 'loop grabs the single element'
                # ~ if guess not in [-2, c]:
                    # ~ print(' ... ... repeated and wrong', item, self.name, c, guess)
                # ~ if guess == c:
                    # ~ print(' ... ... repeated', item, self.name, c, guess)
                # ~ print(' ... ... seen', self, item, c)
                # ~ self.visib.new_edge(self.name, item, c + 2, 'how_seen_seen')
                # ~ return c

    def sibling(self, item_cl, dt):
        '''
        Find among the clans in self one that sees all the rest in the
        very same way as item_cl, return it if found, don't return o/w.
        Caveat: THIS IS A SOURCE OF QUADRATIC COST.
        '''
        print(" --- pursuing a sibling to", item_cl, "in", self)
        for pos_cand, cand_sib in enumerate(self):
            print(" --- candidate", cand_sib, "in position", pos_cand)
            for other in range(len(self)):
                if other != pos_cand:
                    col_ext = dt.how_seen(self[other], item_cl)
                    col_int = dt.how_seen(self[other], cand_sib)
                    print(" --- from", self[other], "to", item_cl, col_ext)
                    print(" --- from", self[other], "to", cand_sib, col_int)
                    if col_ext != col_int:
                        "cand not a sibling"
                        print(" --- not", cand_sib, "due to", self[other], col_int, col_ext)
                        break
            else:
                "if this never happens, no return is like returning None"
                print(" --- found sibling", cand_sib, "in position", pos_cand)
                return pos_cand
        print(" --- no sibling found")

# Need to call from split AND from self.add where we need 
# lists of POSITIONS so we do it that way.
    def _color_lists(self, item_cl, dt):
        '''
        Used both to decide which case of add applies
        (where the "somecolor" is useful) and to
        prepare for splitting.
        '''
        visib_dict = ddict(list)
        somecolor = -2 # some color different from self.color if one such appears 
        for pos, subclan in enumerate(self):
            'len(self) > 1 here'
            visib_dict[c := dt.how_seen(subclan, item_cl)].append(pos)
            if -1 < c != self.color and somecolor == -2:
                "if all are -1 then we may get in trouble"
                somecolor = c
        return visib_dict, somecolor


    def split(self, item_cl, dt, k = 1):
        '''
        With complete in mind. Caveat: changes for primitive?
        k: recursion depth for report-printing, remove some day
        Older pairs clan+color now changed into single clan positions
        '''
        print(" ---"*k, "splitting", self.name, "of color", self.color, "from", item_cl.name)
        v, _ = self._color_lists(item_cl, dt)
        out_clans = list()
        for color in v:
            "visib edges already set up in _color_lists"
            if color > -1:
                "handle a visible clan"
                if len(v[color]) == 1 or self.color == -1:
                    "the primitive case works this way"
                    out_clans.extend(self[pos_vis] for pos_vis in v[color]) 
                    print(" ---"*k, "output includes", list(self[pos_vis].name for pos_vis in v[color]))
                else:
                    out_clans.append(r := Clan((self[cl] for cl in v[color]), self.color))
                    dt.store_clan(r)
                    print(" ---"*k, "output includes", r.name, "with", self.color)
        # and now split the rest, nonvisible subclans
        print(" ---"*k, "pending calls on:", ' '.join(self[cl].name for cl in v[-1]))
        out_clans.extend( cl for pos_not_v in v[-1]
                             for cl in self[pos_not_v].split(item_cl, dt, k + 1) )
        print(" ---"*k, "answer is:", out_clans)
        return out_clans

    def add(self, item_cl, dt):
        '''
        Adds item to the clan, assumed to be a root, and returns
        a new root, possibly the same; uses visibility graph 
        in dt (which has the data graph inside as a fallback) 
        to check colors so as to apply the correct case. 
        Stores all clans created along the way in the DecTree dt.
        '''
        if self.is_sgton:
            'second item, new root with both - caveat: maybe particular case of some other case below?'
            print(' ... ... second item', item_cl, 'for', self)
            new_cl = Clan([self, item_cl], dt.how_seen(self, item_cl))
            dt.store_clan(new_cl)
            return new_cl

        # Set up subclan visibility lists, by colors, -1 for not visible subclans.
        # They contain POSITIONS of the clan list, not the subclans proper:
        # reason is to profit from set difference in case 1b
        # Sept 20th: call new _color_lists instead
        visib_dict, somecolor = self._color_lists(item_cl, dt)
        if visib_dict[-1]:
            print(" ...", ','.join(self[cl].name for cl in visib_dict[-1]), 
                  "not seen from", item_cl, "at", self.name)

        # Case analysis, selfc > -1 iff complete clan
        if self.color > -1 and len(self) == len(visib_dict[self.color]):
            '''
            Case 1a: item sees everything in self in the color of self.
            Careful: the test might add self.color to the keys of 
            visib_dict even if it is with an empty list as value.
            '''
            print(' ... 1a', self, item_cl)
            new_cl = Clan(self + [item_cl], self.color)
            # ~ self.append(item_cl) 
            print(' ... results in', new_cl)
            dt.store_clan(new_cl)
            return new_cl

        if self.color > -1 and 0 < len(visib_dict[self.color]): # < len(self) o/w 1a
            '''
            Case 1b: some, but not all, seen as self.color, then clan
            reduces to these, recursive call on new clan with the rest.
            '''
            print(' ... 1b')

            # current solution: self is left alone, two new clans are created instead
            rest_pos = list(set(range(len(self))).difference(visib_dict[self.color]))
            print(' ... same color:', list(self[pos].name for pos in visib_dict[self.color]))
            print(' ... rest:', list(self[pos].name for pos in rest_pos))
            if len(rest_pos) == 1:
                cl_rest = self[rest_pos[0]]
            else:
                "caveat: this Clan may already exist, created along"
                cl_rest = Clan((self[pos] for pos in rest_pos), self.color)
                dt.store_clan(cl_rest)
            cl_rest = cl_rest.add(item_cl, dt) # recursive call
            cl_same_c = Clan((self[pos] for pos in visib_dict[self.color]), self.color) 
            dt.visib.new_edge(cl_same_c.name, item_cl.name, self.color + 2, '1b')
            cl_same_c.append(cl_rest) # not fiddling with the name yet, should we?
            dt.store_clan(cl_same_c)
            return cl_same_c

        if len(self) == len(visib_dict[somecolor]): 
            '''
            Note: if somecolor still -2 w/ len zero, != len(self),
             and  if somecolor == self.color then already caught in 1a.
            Case 1c: all same color but different from self.color, 
            seems a particular case of 1b but subtly different
            because no clans would remain in self, all in rest,
            recursive call would not reduce size.
            Caveat: might encompass the init case of sgton self,
            if I find a way to handle the color.
            Covers 2b as well when self is primitive.
            '''
            if self.color == -1:
                print(' ... 2b', item_cl, somecolor, visib_dict[somecolor], len(self))
            else:
                print(' ... 1c', item_cl, somecolor, visib_dict[somecolor], len(self))
            dt.visib.new_edge(self.name, item_cl.name, somecolor + 2, '1c/2b')
            new_cl = Clan([self, item_cl], somecolor)
            dt.store_clan(new_cl)
            return new_cl

        if self.color > -1:
            '''
            case 1d: negations of previous conditions lead to:
            either some are nonvisible, maybe all, 
            or at least 2 different colors present.
            '''
            print(' ... 1d')
            print(' ... must split:', list(self[pos].name for pos in visib_dict[-1]))
            # ~ new_cls = [ item_cl ]
            new_cls = list()
            print(" ... traverse visib_dict:", visib_dict) 
            for col in visib_dict:
                if col == -1:
                    "must split"
                    for pos_no_visib in visib_dict[col]:
                        new_cls.extend(self[pos_no_visib].split(item_cl, dt))
                elif len(visib_dict[col]) == 1:
                    "just get the clan"
                    new_cls.append(self[visib_dict[col][0]])
                elif visib_dict[col]:
                    "make a single clan with them all"
                    a_cl = Clan((self[pos_visib] for pos_visib in visib_dict[col]), self.color)
                    dt.store_clan(a_cl)
                    new_cls.append(a_cl)
                # else potential empty list added in the test of 1a, to be ignored
            new_cls.append(item_cl)
            res_cl = Clan(new_cls, -1) # caveat: I BELIEVE THIS -1 IS WRONG
            dt.store_clan(res_cl)
            return res_cl

        elif (pos_sibl := self.sibling(item_cl, dt)) is not None:
            '''
            Case 2a: self is primitive and a sibling is found 
            that sees everyone else in self in the same way as item.
            '''
            print(' ... 2a, sibling is', self[pos_sibl], "in position", pos_sibl)
            added_cl = self[pos_sibl].add(item_cl, dt)
            # ~ dt.store_clan(added_cl) # clans returned from add are all stored
            new_cl = Clan([added_cl] + list(self[i] for i in range(len(self)) if i != pos_sibl), -1)
            dt.store_clan(new_cl)
            return new_cl
            # caveat: Alternative self[pos_sibl] = self[pos_sibl].add(item_cl, dt) but then not tracked

        else:
            '''
            Case 2c: very similar to 1d, caveat: MUST TRY TO UNIFY THEM
            All previous conditions failing must imply somehow that 
            after the splits we keep having a single primitive clan: THINK.
            '''
            print(' ... 2c')
            print(' ... must split:', list(self[pos].name for pos in visib_dict[-1]))
            new_cls = [ item_cl ]
            print(" ... traverse visib_dict:", visib_dict) 
            for col in visib_dict:
                if col == -1:
                    "must split"
                    for pos_no_visib in visib_dict[col]:
                        new_cls.extend(self[pos_no_visib].split(item, dt))
                elif visib_dict[col]:
                    "just get the clans as they are"
                    for pos_visib in visib_dict[col]:
                        new_cls.append(self[pos_visib])
                # else potential empty list added in the test of 1a, to be ignored
            res_cl = Clan(new_cls, -1)
            dt.store_clan(res_cl)
            return res_cl

        print('Unhandled case', visib_dict, self.color, somecolor) # this should never happen
