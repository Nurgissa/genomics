class Sample():
    def __init__(self, T, index, l):
        triplet_i = lambda i: T[i] if i < l else 0
        self.t = (triplet_i(index), triplet_i(index + 1), triplet_i(index + 2))
        self.p = None
        self.r = None
        self.i = index

    
    def get_triplet(self):
        """Character for R_k strings"""
        return self.t
    
    def get_index(self):
        """Position of R_k character in source string"""
        return self.i

    def get_position(self):
        return self.p

    def get_rank(self):
        return self.r

    def set_position(self, position):
        self.p = position
        
    def set_rank(self, rank):
        self.r = rank

    def __repr__(self):
        return "s[{0}, {1}, {2}]".format(self.t, self.i, self.r)
 


class Nonsample():
    def __init__(self, T, index, rank):
        self.i = index
        self.pr = None
        print "len T", len(T)
        #max_i = len(T)
        #if index < max_i:
        #print "T_pos", T[self.i]
        print rank
        if index >= len(T):
            self.pr = (0, rank)
        else:
            self.pr = (T[self.i], rank)
        print self


    def __repr__(self):
        return "ns({0}, {1})".format(self.i, self.pr)