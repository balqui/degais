    def add(self, item_cl, dt):
        if self.is_sgton:
            return dt.clan([self, item_cl], dt.how_seen(self, item_cl))
        visib_dict, somecolor = self._color_lists(item_cl, dt)
        if self.color > -1 and len(self) == len(visib_dict[self.color]):
            'Case 1a: item sees everything in self in the color of self.'
            return dt.clan(self + [ item_cl ], dt.how_seen(self, item_cl))
        if self.color > -1 and 0 < len(visib_dict[self.color]): # < len(self) o/w 1a
            '''
            Case 1b: some, but not all, seen as self.color, then clan
            reduces to these, recursive call on new clan with the rest.
            '''
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
            Covers 2b as well when self is primitive.
            '''
            dt.visib.new_edge(self.name, item_cl.name, somecolor + 2, '1c/2b')
            new_cl = dt.clan([self, item_cl], somecolor)
            return new_cl
        if self.color > -1:
            '''
            case 1d: negations of previous conditions lead to:
            either some are nonvisible, maybe all, 
            or at least 2 different colors present.
            '''
            new_cls = list()
            for col in visib_dict:
                if col == -1:
                    for pos_no_visib in visib_dict[col]:
                        new_cls.extend(self[pos_no_visib].split(item_cl, dt))
                elif len(visib_dict[col]) == 1:
                    new_cls.append(self[visib_dict[col][0]])
                elif visib_dict[col]:
                    a_cl = dt.clan( (self[pos_visib] for pos_visib in visib_dict[col]), self.color )
                    new_cls.append(a_cl)
            new_cls.append(item_cl)
            res_cl = dt.clan(new_cls, -1)
            return res_cl
        elif (pos_sibl := self.sibling(item_cl, dt)) is not None:
            '''
            Case 2a: self is primitive and a sibling is found 
            that sees everyone else in self in the same way as item.
            '''
            added_cl = self[pos_sibl].add(item_cl, dt)
            new_cl = dt.clan( list(self[i] for i in range(len(self)) if i != pos_sibl) + [added_cl], -1)
            return new_cl
        else:
            '''
            Case 2c: very similar to 1d, but simpler.
            All previous conditions failing must imply somehow that 
            after the splits we keep having a single primitive clan: THINK.
            '''
            new_cls = [ item_cl ]
            for col in visib_dict:
                if col == -1:
                    for pos_no_visib in visib_dict[col]:
                        new_cls.extend(self[pos_no_visib].split(item_cl, dt))
                elif visib_dict[col]:
                    for pos_visib in visib_dict[col]:
                        new_cls.append(self[pos_visib])
            res_cl = dt.clan(new_cls, -1)
            return res_cl
