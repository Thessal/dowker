import unittest
from unittest import TestCase
from dowker import SimplexTree, Sink

class ExampleOneTestCase(TestCase):

    def setUp(self):
        self.ph_x = sorted([(0, (0.0, float("inf"))), (0, (0.0, 2.0)), (0, (0.0, 1.0))])
        self.ph_y = sorted([(1, (3.0, 4.0)), (0, (0.0, float("inf"))), (0, (0.0, 2.0)), (0, (0.0, 1.0))])

    def build_x(self):
        # Figure 2, graph X
        st = SimplexTree()
        st.add_edge(a=1,b=3,w=4) # Equivalent to : st.update(Sink(center=1, simplex={1,3}, delta=4))
        st.add_edge(3,1,2)
        st.add_edge(3,2,3)
        st.add_edge(2,3,5)
        st.add_edge(2,1,1)
        st.add_edge(1,2,6)
        return st

    def build_y(self):
        # Figure 2, graph Y
        st = SimplexTree()
        st.add_edge(a=1,b=3,w=2) # Equivalent to : st.update(Sink(center=1, simplex={1,3}, delta=4))
        st.add_edge(3,1,4)
        st.add_edge(3,2,3)
        st.add_edge(2,3,5)
        st.add_edge(2,1,1)
        st.add_edge(1,2,6)
        return st
    
    def compare_list(self, a,b):
        self.assertTrue(len(a) == len(b), msg=f"size does not match:\nResult:{a}\nValid:{b}")
        self.assertTrue(all(x==y for x,y in zip(sorted(a), sorted(b))), msg=f"value does not match:\nResult:{a}\nValid:{b}")

    def test_ph_x(self):
        st = self.build_x()
        st.expand(max_dim=2)
        st = st.get_gudhi_simplex_tree()
        diag = st.persistence(min_persistence=0)
        self.compare_list(diag, self.ph_x)

    def test_ph_y(self):
        st = self.build_y()
        st.expand(max_dim=2)
        st = st.get_gudhi_simplex_tree()
        diag = st.persistence(min_persistence=0)
        self.compare_list(diag, self.ph_y)

class ExampleTwoTestCase(TestCase):

    def setUp(self):
        # Figure 4
        self.data = [
            [0, 1, 2, 3, 4, 5, 6],
            [6, 0, 1, 2, 3, 4, 5],
            [5, 6, 0, 1, 2, 3, 4],
            [4, 5, 6, 0, 1, 2, 3],
            [3, 4, 5, 6, 0, 1, 2],
            [2, 3, 4, 5, 6, 0, 1],
            [1, 2, 3, 4, 5, 6, 0]]
        self.ph = [(1, (1.0, 4.0)), (0, (0.0, float("inf"))), (0, (0.0, 1.0)), (0, (0.0, 1.0)), (0, (0.0, 1.0)), (0, (0.0, 1.0)), (0, (0.0, 1.0)), (0, (0.0, 1.0))]
    
    def build(self):
        st = SimplexTree()
        st.add_edge_from_array(self.data, nrow=7, ncol=7)
        return st

    def compare_list(self, a,b):
        self.assertTrue(len(a) == len(b), msg=f"size does not match:\nResult:{a}\nValid:{b}")
        self.assertTrue(all(x==y for x,y in zip(sorted(a), sorted(b))), msg=f"value does not match:\nResult:{a}\nValid:{b}")

    def test_ph(self):
        st = self.build()
        st.expand(max_dim=2)
        diag = st.gudhi.persistence(min_persistence=0)
        self.compare_list(diag, self.ph)


if __name__ == '__main__':
    unittest.main()
