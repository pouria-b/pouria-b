import time

def complexity(algorithm_name, func, *args, **kwargs):
    complexities = {
        "merge_sort": "O(n log n)",
        "quick_sort": "O(n log n) average, O(n^2) worst",
        "coin_change_greedy": "O(n log n + k)",
        "knapsack": "O(nW)",
        "huffman_coding": "O(n log n)",
        "prim": "O(E log V)",
        "kruskal": "O(E log V)",
        "dfs": "O(V + E)",
        "bfs": "O(V + E)",
        "bellman_ford": "O(VE)",
        "dijkstra": "O(E log V)",
        "floyd_warshall": "O(V^3)",
        "fibonacci_memo": "O(n)",
        "hanoi": "O(2^n)",
        "binary_search": "O(log n)",
        "interpolation_search": "O(log log n) avg, O(n) worst",
    }

    
    result = func(*args, **kwargs)
    end = time.perf_counter()

    s = str(result)
    sample = s if len(s) < 120 else s[:120] + "..."

    return {
        "algorithm": algorithm_name,
        "theoretical": complexities.get(algorithm_name, "Unknown"),
        "result_sample": sample,
    }