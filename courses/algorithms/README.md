# Algorithm Design and Analysis — Python Coursework

University coursework by Pouria Babaei. Sixteen educational algorithms spanning sorting, searching, dynamic programming, graphs, greedy methods and recursion. Uses the Python standard library only; Python 3.9+ recommended.

## Run

From the extracted course directory:

```bash
python main.py
python -m unittest discover -s tests -p test_correctness.py -v
```

`main.py` is a demonstration runner, not a correctness test or benchmark. It prints sample results and fixed theoretical complexity labels. The separate assertion suite checks representative outputs.

## Layout

- `algorithms/`: implementations grouped by topic.
- `tests/test_algorithms.py`: demonstration runner from the upload.
- `tests/test_correctness.py`: added assertions.
- `original/`: unchanged uploaded Python sources, including `min.py`.
- `CHANGELOG.md`: packaging changes and correction.

## Algorithm reference

| Function | Input → output | Complexity and assumptions |
| --- | --- | --- |
| merge_sort | Comparable sequence → sorted sequence | O(n log n); not stable for equal tagged keys |
| quick_sort | Comparable sequence → sorted list | Average O(n log n), worst O(n²) |
| binary_search | Ascending sorted sequence, target → index or −1 | O(log n) |
| interpolation_search | Ascending numeric sequence, target → index or −1 | Average O(log log n) for uniform data, worst O(n) |
| knapsack | Integer weights, values, capacity W → maximum value | O(nW) time and space; 0/1 choices |
| fibonacci_memo | Nonnegative integer n → Fibonacci number | O(n) states, unit-cost arithmetic |
| prim | Undirected weighted adjacency dictionary, start → MST edges | O(E log E); start component only |
| kruskal | Nodes, (u,v,weight) edges → minimum spanning forest | O(E log E) sorting plus union-find |
| dfs | Adjacency dictionary, start → reachable vertex set | O(V+E), recursive |
| bfs | Adjacency dictionary, start → reachable vertex set | O(V+E); duplicate queue entries may use O(E) memory |
| bellman_ford | Edge list, vertex count, source → distance list | O(VE); no negative-cycle detection |
| dijkstra | Weighted adjacency dictionary, source → distances | O((V+E) log V) for simple graphs; nonnegative weights |
| floyd_warshall | Square distance matrix → all-pairs distances | O(V³) time, O(V²) space |
| coin_change_greedy | Positive integer denominations, amount → coin list | O(c log c+k); not always optimal or exact |
| huffman_coding | Text → character-to-bit-string dictionary | O(n+k log k) construction, plus emitted code lengths |
| hanoi | Positive integer n and three peg labels → move list | O(2ⁿ) time and output space; n=0 unsupported |

## Example

```python
from algorithms.sorting import merge_sort
from algorithms.dp import knapsack
assert merge_sort([3, 1, 2]) == [1, 2, 3]
assert knapsack([2, 3, 4], [3, 4, 5], 5) == 7
```

## Limitations

Educational code with limited validation. Search inputs must be sorted. Knapsack needs aligned weights/values and nonnegative integer capacity/weights. Graph vertices for Bellman–Ford are indexed 0 through V−1. Dijkstra requires nonnegative weights and every vertex as a dictionary key. Floyd–Warshall expects zero diagonal and infinity for absent edges. Bellman–Ford and Floyd–Warshall do not detect negative cycles. Greedy change may leave an unrepresented remainder. Recursive algorithms can exceed Python's recursion limit. The complexity labels in utils.py are classroom summaries, not empirical measurements; the table above adds implementation-specific qualifications.

No instructor, semester or course grade has been supplied.
