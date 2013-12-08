class Sample():
    def __init__(self, T, index, l):
        triplet_i = lambda i: T[i] if i < l else 0
        self.t = (triplet_i(index), triplet_i(index + 1), triplet_i(index + 2))
        self.p = None
        self.r = None
        self.i = index

    def __repr__(self):
        return "({0},{1},{2},{3})".format(self.t, self.i, self.r, self.p)

    def get_triplet(self):
        return self.t
    
    def get_index(self):
        return self.i

    def get_position(self):
        return self.p

    def get_rank(self):
        return self.r

    def set_position(self, position):
        self.p = position
        
    def set_rank(self, rank):
        self.r = rank

class Nonsample():
    def __init__(self, T, index, rank):
        self.i = index
        self.pr = None

        if index >= len(T):
            self.pr = (0, rank)
        else:
            self.pr = (T[self.i], rank)

    def __repr__(self):
        return "({0},{1})".format(self.pr, self.i)