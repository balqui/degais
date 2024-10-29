'''
Author: Jose Luis Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)
'''

from auxfun import delbl, comb
from collections import Counter, defaultdict as ddict

class Clan(list):
    '''
    A clan is a list plus a name and a singleton flag.

    Names are immutable surrogates of clans for use in dicts like
    self and its visibility graph. Parentheses chosen for names 
    due to being smaller than any letter or digit, get sorted first.
    In nonsigleton clans, the list contains subclans. Singleton clans 
    consist of a single item. They are created separately and marked 
    as such with the flag. 

    In complete clans, self.color indicates the color. Primitive 
    clans have self.color == -1. Also singleton clans, just to avoid 
    checking an undefined value.

    Users should create clans only through the factory in class DecTree 
    instead of using the call to __init__() through Clan().
    '''

    def __init__(self, name, elems, color = -1):
        '''
        Clan creation resorted to only if clan not in factory pool.
        '''
        assert len(elems) > 0
        super().__init__(self)
        self.extend(elems) 
        self.name = name
        self.color = color
        self.is_sgton = False


    def path(self, dt):
        '''
        Check whether it is a single-color path, discounting
        the color 0, transparent; if so, reorder members so
        that it is drawn indeed as a path later.
        '''
        count = 0
        seencol = 0
        neigh = ddict(list) # adjacency lists on names
        for cl_a, cl_b in comb(self, 2):
            col = dt.how_seen(cl_a, cl_b)
            if col > 0:
                count += 1
                if seencol == 0:
                    seencol = col
                elif col != seencol:
                    "not a single-color path if path at all"
                    return False
                neigh[cl_a.name].append(cl_b.name)
                neigh[cl_b.name].append(cl_a.name)
        if count != len(self) - 1:
            "not a path, wrong number of edges"
            return False
        for scl in neigh:
            if len(neigh[scl]) > 2:
                "not a path, vertex of degree higher than 2"
                return False
        # attempt at constructing path, name by name
        curr = None
        for scl in neigh:
            "start with some vertex of deg 1"
            if len(neigh[scl]) == 1:
                curr = scl
                break
        if curr is None:
            "not a path, no vertex of degree 1"
            return False
        attempt = list() # order the names following the path
        attempt.append(dt[curr])
        nxt = neigh[curr][0] # uniquely defined here
        while len(neigh[nxt]) == 2:
            "keep constructing path"
            for scl in neigh[nxt]:
                if scl != curr:
                    curr = nxt
                    attempt.append(dt[curr])
                    nxt = scl
                    break
        attempt.append(dt[nxt])
        if len(attempt) < len(self):
            "path too short, rest may have cycles"
            return False
        else:
            "path found"
            return Clan(self.name, attempt, self.color) # color must say primitive


    def sibling(self, item_cl, dt):
        '''
        Find among the clans in self one that sees all the rest in the
        very same way as item_cl, return it if found, don't return o/w.
        If self is complete, all are siblings but we would have run case
        1a before checking it out.
        This might be a potential source of quadratic cost, see
        https://github.com/balqui/degais/issues/7
        '''
        for pos_cand, cand_sib in enumerate(self):
            for other in range(len(self)):
                if other != pos_cand:
                    col_ext = dt.how_seen(self[other], item_cl)
                    col_int = dt.how_seen(self[other], cand_sib)
                    if col_ext != col_int:
                        "cand not a sibling"
                        break
            else:
                "if this never happens, no return is like returning None"
                return pos_cand

# Need to call from split AND from self.add where we need 
# lists of POSITIONS so we do it that way.
    def _color_lists(self, item_cl, dt):
        '''
        Used both to decide which case of add applies (where the 
        "somecolor" is useful) and to prepare for splitting.
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


    def split(self, item_cl, dt):
        '''
        Recursive splitting.
        '''
        v, _ = self._color_lists(item_cl, dt)
        out_clans = list()
        for color in v:
            "visib edges already set up in _color_lists"
            if color > -1:
                "handle a visible clan"
                if len(v[color]) == 1 or self.color == -1:
                    "the primitive case works this way"
                    out_clans.extend(self[pos_vis] for pos_vis in v[color]) 
                else:
                    out_clans.append(dt.clan( (self[cl] for cl in v[color]), self.color ))
        # and now split the rest, nonvisible subclans
        out_clans.extend( cl for pos_not_v in v[-1]
                             for cl in self[pos_not_v].split(item_cl, dt) )
        return out_clans

    def add(self, item_cl, dt):
        '''
        Adds item to the clan, assumed to be a root, and returns
        a new root, possibly the same; uses visibility graph 
        in dt (which has the data graph inside as a fallback) 
        to check colors so as to apply the correct case. 
        The DecTree dt acts also as a factory, with a pool of
        all the clans created along the way.
        '''
        if self.is_sgton:
            '''
            Second item, new root with both; could be merged with
            other cases below, but these other cases do need the 
            call to _color_lists, which then has to work for 
            singletons so we just change the place of the test
            but would not really simplify the code.
            '''
            return dt.clan([self, item_cl], dt.how_seen(self, item_cl))

        # Call _color_lists to set up subclan visibility lists, by colors, 
        # -1 for not visible subclans.
        # They contain POSITIONS of the clan list, not the subclans proper:
        # reason is to profit from set difference in case 1b
        visib_dict, somecolor = self._color_lists(item_cl, dt)

        # Case analysis, selfc > -1 iff complete clan
        if self.color > -1 and len(self) == len(visib_dict[self.color]):
            '''
            Case 1a: item sees everything in self in the color of self.
            Careful: the test might add self.color to the keys of 
            visib_dict even if it is with an empty list as value.
            '''
            return dt.clan(self + [ item_cl ], dt.how_seen(self, item_cl))

        if self.color > -1 and 0 < len(visib_dict[self.color]): # < len(self) o/w 1a
            '''
            Case 1b: some, but not all, seen as self.color, then clan
            reduces to these, recursive call on new clan with the rest.
            '''

            # self is left alone, two new clans are created instead
            rest_pos = list(set(range(len(self))).difference(visib_dict[self.color]))
            if len(rest_pos) == 1:
                cl_rest = self[rest_pos[0]]
            else:
                cl_rest = dt.clan( (self[pos] for pos in rest_pos), self.color )
            cl_rest = cl_rest.add(item_cl, dt) # recursive call
            cl_same_c = dt.clan( list(self[pos] for pos in visib_dict[self.color]) + [ cl_rest ], 
                             self.color)
            dt.visib.new_edge(cl_same_c.name, item_cl.name, self.color + 2, '1b')
            return cl_same_c

        if len(self) == len(visib_dict[somecolor]): 
            '''
            Note: if somecolor still -2 w/ len zero, != len(self),
             and  if somecolor == self.color then already caught in 1a.
            Case 1c: all same color but different from self.color, 
            seems a particular case of 1b but subtly different
            because no clans would remain in self, all in rest,
            recursive call would not reduce size.
            Covers 2b as well when self is primitive.
            '''
            dt.visib.new_edge(self.name, item_cl.name, somecolor + 2, '1c/2b')
            new_cl = dt.clan([self, item_cl], somecolor)
            return new_cl

        pos_sibl = None
        if self.color == -1:
            pos_sibl = self.sibling(item_cl, dt)

        if pos_sibl is not None:
            '''
            Case 2a: self is primitive and a sibling is found 
            that sees everyone else in self in the same way as item.
            '''
            added_cl = self[pos_sibl].add(item_cl, dt)
            new_cl = dt.clan( list(self[i] for i in range(len(self)) if i != pos_sibl) + [added_cl], -1)
            return new_cl

        '''
        If none of them, then cases 1d or 2c.
        If complete, negations of previous conditions lead to:
        either some are nonvisible, maybe all, 
        or at least 2 different colors present.
        '''
        new_cls = [ item_cl ]
        for col in visib_dict:
            if col == -1:
                "must split"
                for pos_no_visib in visib_dict[col]:
                    new_cls.extend(self[pos_no_visib].split(item_cl, dt))
            elif (visib_dict[col] and 
                 (len(visib_dict[col]) == 1 or self.color == -1)):
                "just get the clans as they are, 2c or 1d with only one"
                for pos_visib in visib_dict[col]:
                    new_cls.append(self[pos_visib])
            elif visib_dict[col]:
                "1d, make a single clan with them all"
                a_cl = dt.clan( (self[pos_visib] for pos_visib in visib_dict[col]), self.color )
                new_cls.append(a_cl)
            # else potential empty list added in the test of 1a, to be ignored
        res_cl = dt.clan(new_cls, -1)
        return res_cl

