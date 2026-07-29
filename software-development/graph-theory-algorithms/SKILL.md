---
name: graph-theory-algorithms
description: "Use when implementing graph algorithms for network analysis."
category: software-development
tags: [graph, algorithms, bfs, dfs, shortest-path, network]
---
# Graph Theory Algorithms

Graph algorithms for network analysis, pathfinding, and optimization.

## Graph Representations

```python
# Adjacency Matrix (O(1) edge check, O(V²) memory)
matrix = [[0]*n for _ in range(n)]

# Adjacency List (O(V+E) memory, good for sparse)
graph = {0: [1, 2], 1: [2], 2: [0, 3], 3: [3]}

# Edge List (for MST algorithms)
edges = [(0, 1, 5), (1, 2, 3), (2, 3, 1)]
```

## Shortest Path

```python
import heapq

# Dijkstra (non-negative weights)
def dijkstra(graph: dict, start: int, n: int) -> list[int]:
    dist = [float('inf')] * n
    dist[start] = 0
    pq = [(0, start)]

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]: continue
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))
    return dist

# Bellman-Ford (handles negative weights, detects negative cycles)
def bellman_ford(edges: list, n: int, start: int) -> list:
    dist = [float('inf')] * n
    dist[start] = 0
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    # Check for negative cycles
    for u, v, w in edges:
        if dist[u] + w < dist[v]:
            return None  # negative cycle detected
    return dist
```

## Minimum Spanning Tree

```python
# Kruskal (sort edges, union-find)
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py: return False
        if self.rank[px] < self.rank[py]: px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]: self.rank[px] += 1
        return True

def kruskal(edges: list, n: int) -> list:
    edges.sort(key=lambda x: x[2])  # sort by weight
    uf = UnionFind(n)
    mst = []
    for u, v, w in edges:
        if uf.union(u, v):
            mst.append((u, v, w))
            if len(mst) == n - 1: break
    return mst
```

## Topological Sort

```python
from collections import deque

def topological_sort(graph: dict[int, list[int]]) -> list[int]:
    in_degree = {u: 0 for u in graph}
    for u in graph:
        for v in graph[u]:
            in_degree[v] = in_degree.get(v, 0) + 1

    queue = deque([u for u, d in in_degree.items() if d == 0])
    result = []

    while queue:
        u = queue.popleft()
        result.append(u)
        for v in graph.get(u, []):
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    return result if len(result) == len(graph) else []  # cycle detected
```

## Maximum Flow

```python
# Ford-Fulkerson with DFS
def max_flow(capacity: list[list[int]], source: int, sink: int) -> int:
    n = len(capacity)
    flow = [[0]*n for _ in range(n)]

    def dfs(s, t, min_cap):
        if s == t: return min_cap
        for v in range(n):
            residual = capacity[s][v] - flow[s][v]
            if residual > 0 and not visited[v]:
                visited[v] = True
                pushed = dfs(v, t, min(min_cap, residual))
                if pushed:
                    flow[s][v] += pushed
                    flow[v][s] -= pushed
                    return pushed
        return 0

    total = 0
    while True:
        visited = [False] * n
        pushed = dfs(source, sink, float('inf'))
        if not pushed: break
        total += pushed
    return total
```

## Pitfalls

- Dijkstra fails with negative edges — use Bellman-Ford
- Negative cycles make shortest path undefined
- Recursive DFS can overflow stack on large graphs — use iterative
- Union-find path compression is critical for performance
- Topological sort only works on DAGs
