class Sink:
    def __init__(self, center:int, simplex:set, delta):
        assert center in simplex
        assert len(simplex) > 1
        self.center = center
        self.simplex = simplex
        self.delta = delta
    def __len__(self):
        return len(self.simplex)
    def __repr__(self):
        return f"Sink(center={self.center}, simplex={self.simplex}, delta={self.delta})"
    @property
    def vertices(self):
        # returns center + sorted list of nodes except center node
        return [self.center] + sorted(x for x in self.simplex if x!=self.center)
