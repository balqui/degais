class Clan(list):
    '''
    A clan is a list of subclans plus a prototype item taken 
    from one of the subclans. "Colors" relating clans are 
    found out by checking the edge connecting the prototypes 
    in the original graph.
    
    Inherits __init__ so we get an empty list.
    
    Nonsingleton clans are created separately.
    '''

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

    


class PrimClan(Clan):
    pass

class ComplClan(Clan):
    pass

