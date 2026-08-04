---
name: data-structures-algorithms
description: "Use when implementing data structures and algorithms."
category: software-development
tags: [data-structures, algorithms, dsa, programming]
---
# Data Structures & Algorithms

Common data structures and algorithms for production code and interviews.

## Arrays & Hashing

```python
# Two-pointer
def two_sum(nums: list[int], target: int) -> tuple:
    seen = {}
    for i, n in enumerate(nums):
        complement = target - n
        if complement in seen:
            return (seen[complement], i)
        seen[n] = i

# Sliding window
def max_subarray_sum(nums: list[int], k: int) -> int:
    window_sum = sum(nums[:k])
    max_sum = window_sum
    for i in range(k, len(nums)):
        window_sum += nums[i] - nums[i - k]
        max_sum = max(max_sum, window_sum)
    return max_sum
```

## Trees

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# DFS traversals
def inorder(root):      # left, root, right
    if not root: return []
    return inorder(root.left) + [root.val] + inorder(root.right)

def preorder(root):     # root, left, right
    if not root: return []
    return [root.val] + preorder(root.left) + preorder(root.right)

def postorder(root):    # left, right, root
    if not root: return []
    return postorder(root.left) + postorder(root.right) + [root.val]

# BFS
from collections import deque
def bfs(root):
    q = deque([root]); result = []
    while q:
        node = q.popleft()
        result.append(node.val)
        if node.left: q.append(node.left)
        if node.right: q.append(node.right)
    return result
```

## Graphs

```python
# Adjacency list
def build_graph(edges: list[tuple]) -> dict:
    graph = {}
    for u, v in edges:
        graph.setdefault(u, []).append(v)
        graph.setdefault(v, []).append(u)
    return graph

# DFS (iterative)
def dfs(graph: dict, start: str) -> list:
    visited, stack = set(), [start]
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            stack.extend(n for n in graph[node] if n not in visited)
    return list(visited)

# Dijkstra
import heapq
def shortest_path(graph: dict, start: str, end: str) -> list:
    pq = [(0, start, [start])]
    visited = set()
    while pq:
        cost, node, path = heapq.heappop(pq)
        if node == end: return path
        if node in visited: continue
        visited.add(node)
        for neighbor, weight in graph[node]:
            if neighbor not in visited:
                heapq.heappush(pq, (cost + weight, neighbor, path + [neighbor]))
    return []
```

## Dynamic Programming

```python
# Fibonacci (memoization)
from functools import lru_cache
@lru_cache(maxsize=None)
def fib(n: int) -> int:
    if n < 2: return n
    return fib(n-1) + fib(n-2)

# 0/1 Knapsack (tabulation)
def knapsack(weights: list[int], values: list[int], capacity: int) -> int:
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i-1][w], dp[i-1][w - weights[i-1]] + values[i-1])
            else:
                dp[i][w] = dp[i-1][w]
    return dp[n][capacity]
```

## Sorting & Searching

```python
# Binary search
def binary_search(arr: list[int], target: int) -> int:
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target: return mid
        if arr[mid] < target: left = mid + 1
        else: right = mid - 1
    return -1

# Quick sort (in-place)
def quicksort(arr: list, lo: int = 0, hi: int = None):
    if hi is None: hi = len(arr) - 1
    if lo >= hi: return
    pivot = partition(arr, lo, hi)
    quicksort(arr, lo, pivot - 1)
    quicksort(arr, pivot + 1, hi)

def partition(arr, lo, hi):
    pivot = arr[hi]; i = lo
    for j in range(lo, hi):
        if arr[j] <= pivot:
            arr[i], arr[j] = arr[j], arr[i]; i += 1
    arr[i], arr[hi] = arr[hi], arr[i]
    return i
```

## Pitfalls

- Recursive tree depth can overflow stack — use iterative for deep trees
- Dijkstra doesn't work with negative weights (use Bellman-Ford)
- DP tabulation vs memoization — tabulation avoids recursion limit
- Hash collisions degrade performance — use good hash functions
- In-place algorithms modify input — copy if original needed
