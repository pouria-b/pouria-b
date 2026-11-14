from algorithms.sorting import merge_sort, quick_sort
from algorithms.searching import binary_search, interpolation_search
from algorithms.dp import knapsack, fibonacci_memo
from algorithms.graph import prim, kruskal, dfs, bfs, bellman_ford, dijkstra, floyd_warshall
from algorithms.greedy import coin_change_greedy, huffman_coding
from algorithms.recursion import hanoi
from algorithms.utils import complexity


def run_tests():
    tests = [
        ("merge_sort", merge_sort, [[3,1,4,1,5,9,2]]),
        ("quick_sort", quick_sort, [[3,1,4,1,5,9,2]]),
        # ("coin_change_greedy", coin_change_greedy, [[1,5,10,25], 63]),
        ("knapsack", knapsack, [[2,3,4], [3,4,5], 5]),
        ("huffman_coding", huffman_coding, ["hello world"]),
        ("prim", prim, [{0: [(1,1),(2,3)], 1:[(0,1),(2,1)], 2:[(0,3),(1,1)]}, 0]),
        ("kruskal", kruskal, [[0,1,2], [(0,1,1),(1,2,2),(0,2,3)]]),
        ("dfs", dfs, [{0:[1,2],1:[0,2],2:[0,1,3],3:[2]}, 0]),
        ("bfs", bfs, [{0:[1,2],1:[0,2],2:[0,1,3],3:[2]}, 0]),
        ("bellman_ford", bellman_ford, [[(0,1,-1),(0,2,4),(1,2,3),(1,3,2),(1,4,2),(3,2,5),(3,1,1),(4,3,-3)], 5, 0]),
        ("dijkstra", dijkstra, [{0:[(1,4),(2,1)],1:[(3,1)],2:[(1,2),(3,5)],3:[]}, 0]),
        # ("floyd_warshall", floyd_warshall, [[[0,5,float('inf')],[50,0,15],[30,float('inf'),0]]]),
        ("fibonacci_memo", fibonacci_memo, [10]),
        ("hanoi", hanoi, [3,'A','C','B']),
        ("binary_search", binary_search, [[1,2,3,4,5,6], 4]),
        ("interpolation_search", interpolation_search, [[10,20,30,40,50], 30]),
    ]

    print("===== Algorithm Tests =====")
    for name, func, args in tests:
        print(f"Testing-> {name} :")
        result = complexity(name, func, *args)
        for k, v in result.items():
            print(f"{k}: {v}")   
        print("-")


if __name__ == "__main__":
    run_tests()
