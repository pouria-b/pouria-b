import unittest
from algorithms.sorting import merge_sort, quick_sort
from algorithms.searching import binary_search, interpolation_search
from algorithms.dp import knapsack, fibonacci_memo
from algorithms.graph import prim, kruskal, dfs, bfs, bellman_ford, dijkstra, floyd_warshall
from algorithms.greedy import coin_change_greedy, huffman_coding
from algorithms.recursion import hanoi
class Correctness(unittest.TestCase):
 def test_sorting(self):
  for f in (merge_sort,quick_sort):
   for a in ([],[1],[3,-1,3,0]): self.assertEqual(f(a),sorted(a))
 def test_searching(self):
  for f in (binary_search,interpolation_search):
   self.assertEqual(f([],2),-1);self.assertEqual(f([1,2,3],2),1);self.assertEqual(f([1,2,3],9),-1);self.assertIn(f([2,2,2],2),range(3))
 def test_dp(self):
  self.assertEqual(knapsack([2,3,4],[3,4,5],5),7);self.assertEqual(fibonacci_memo(10),55)
 def test_mst(self):
  g={0:[(1,1),(2,3)],1:[(0,1),(2,1)],2:[(0,3),(1,1)]}
  m=prim(g,0);self.assertEqual(len(m),2);self.assertEqual(sum(x[2] for x in m),2)
  self.assertEqual(sum(x[2] for x in kruskal([0,1,2],[(0,1,1),(1,2,1),(0,2,3)])),2)
 def test_traversal(self):
  g={0:[1],1:[0,2],2:[],3:[]};self.assertEqual(dfs(g,0),{0,1,2});self.assertEqual(bfs(g,0),{0,1,2})
 def test_paths(self):
  self.assertEqual(dijkstra({0:[(1,4),(2,1)],1:[],2:[(1,2)]},0),{0:0,1:3,2:1})
  self.assertEqual(bellman_ford([(0,1,-1),(1,2,2)],3,0),[0,-1,1])
  inf=float('inf');self.assertEqual(floyd_warshall([[0,2,10],[inf,0,3],[inf,inf,0]])[0][2],5)
 def test_greedy(self):
  self.assertEqual(sum(coin_change_greedy([1,5,10,25],63)),63)
  self.assertEqual(huffman_coding(''),{});self.assertEqual(huffman_coding('aaa'),{'a':'0'})
  codes=huffman_coding('hello world');self.assertEqual(set(codes),set('hello world'))
  for a in codes:
   for b in codes:
    if a!=b:self.assertFalse(codes[b].startswith(codes[a]))
 def test_hanoi(self):
  moves=hanoi(3,'A','C','B');self.assertEqual(len(moves),7)
  pegs={'A':[3,2,1],'B':[],'C':[]}
  for source,target in moves:
   disk=pegs[source].pop();self.assertTrue(not pegs[target] or pegs[target][-1]>disk);pegs[target].append(disk)
  self.assertEqual(pegs['C'],[3,2,1])
