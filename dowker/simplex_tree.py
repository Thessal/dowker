from collections import defaultdict, namedtuple
from .sink import Sink

class SimplexTree:
    # A Simplex tree for Dowker complex.

    def rec_dd(self, delta=None):
        return self.Vertex(delta=delta, children=defaultdict(self.rec_dd))
    
    def __init__(self):
        self.Vertex = namedtuple("Vertex", ['delta', 'children'])
        self.root = self.rec_dd()

    def __repr__(self):
        outstr=""
        def _print(outstr, label:int, delta, children:defaultdict, level=0):
            outstr += f'{" "*level} [{label}], d={delta}\n'
            for k,v in children.items():
                outstr = _print(outstr, k, v.delta, v.children, level+1)
            return outstr
        return _print(outstr, 0, self.root.delta, self.root.children, 0) 
    
    def find(self, sink:Sink):
        cur = self.root
        for v in sink.vertices:
            if v in cur.children:
                cur = cur.children[v]
            else:
                ValueError("SimplexTree.find : Not found")
        return cur
    
    def update(self, sink:Sink):
        delta = sink.delta
        cur = self.root
        vs = sink.vertices
        for v in vs[:-1]:
            cur = cur.children[v]
            if (cur.delta is not None) and (cur.delta > delta) : 
                delta = cur.delta
        cur.children[vs[-1]] = self.rec_dd(delta=delta)

    def add_edge(self, a, b, w):
        self.update(Sink(center=a, simplex={a,b}, delta=w))

    def add_edge_from_array(self, arr, nrow, ncol):
        for i in range(nrow):
            for j in range(ncol):
                if i != j:
                    self.add_edge(i, j, arr[i][j])

    def get_all_vertices(self):
        def _get(children, prev=[]):
            output = [{"delta":v.delta, "simplex":prev + [k]} for k,v in children.items()]
            output += [x for k,v in children.items() for x in _get(v.children, prev + [k])]
            return output 
        output = [] 
        for k,v in self.root.children.items():
            output.extend([Sink(center=k, simplex=set([k]+x["simplex"]), delta=x["delta"]) for x in _get(v.children)])
        return output    
    
    def expand(self, max_dim):
        all_vertices = self.get_all_vertices()
        assert all(len(sink.vertices)<=2 for sink in all_vertices)
        for cur_dim in range(1,max_dim):
            self._expand(cur_dim)

    def _expand(self, cur_dim):
        for sink in [x for x in self.get_all_vertices() if len(x.vertices)==cur_dim+1]: # find leaf
            center_vertex = self.root.children[sink.center]
            for label, vertex in center_vertex.children.items(): # edges that shares center
                delta = vertex.delta
                if label > sink.vertices[-1]:
                    new_sink = Sink(center=sink.center, simplex=sink.simplex.union({label}), delta=max(sink.delta, delta))
                    self.update(new_sink) # unnecessary lookup

    def get_gudhi_simplex_tree(self):
        from gudhi import SimplexTree
        st = SimplexTree()
        for node in self.root.children.keys():
            # print(f"[node]:{node}")
            st.insert(simplex=[node], filtration=0)
        for simplex in self.get_all_vertices():
            # print(f"[simplex]:{simplex}")
            st.insert(simplex=list(simplex.simplex), filtration=simplex.delta)
        return st
    
    @property
    def gudhi(self):
        return self.get_gudhi_simplex_tree()