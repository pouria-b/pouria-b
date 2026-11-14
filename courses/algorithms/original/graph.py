import heapq

def prim(graph, start):
    visited = set()
    edges = [(0, start, None)]
    mst = []
    while edges:
        cost, node, parent = heapq.heappop(edges)
        if node not in visited:
            visited.add(node)
        if parent is not None:
            mst.append((parent, node, cost))
        for neighbor, weight in graph.get(node, []):
            if neighbor not in visited:
                heapq.heappush(edges, (weight, neighbor, node))
    return mst




def kruskal(nodes, edges):
    parent = {node: node for node in nodes}
    rank = {node: 0 for node in nodes}

    def find(node):
        if parent[node] != node:
            parent[node] = find(parent[node])
        return parent[node]

    def union(u, v):
        ru, rv = find(u), find(v)
        if ru != rv:
            if rank[ru] > rank[rv]:
                parent[rv] = ru
            elif rank[ru] < rank[rv]:
                 parent[ru] = rv
            else:
                parent[rv] = ru
                rank[ru] += 1

    mst = []
    for u, v, w in sorted(edges, key=lambda x: x[2]):
        if find(u) != find(v):
            union(u, v)
            mst.append((u, v, w))
    return mst



def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            dfs(graph, neighbor, visited)  # ← حتماً visited را پاس بده
    return visited




def bfs(graph, start):
    from collections import deque
    visited = set()
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            queue.extend(graph.get(node, []))
    return visited




def bellman_ford(graph, V, start):
    dist = [float("inf")] * V
    dist[start] = 0
    for _ in range(V-1):
        updated = False
        for u, v, w in graph:
            if dist[u] != float("inf") and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                updated = True
        if not updated:
            break
    return dist




def dijkstra(graph, start):
    dist = {node: float("inf") for node in graph}
    dist[start] = 0
    pq = [(0, start)]
    while pq:
        current_dist, node = heapq.heappop(pq)
        if current_dist > dist[node]:
            continue
        for neighbor, weight in graph.get(node, []):
            nd = current_dist + weight
            if nd < dist[neighbor]:
                dist[neighbor] = nd
                heapq.heappush(pq, (nd, neighbor))
    return dist




def floyd_warshall(graph):
    V = len(graph)
    dist = [[graph[i][j] for j in range(V)] for i in range(V)]
    for k in range(V):
        for i in range(V):
            for j in range(V):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist