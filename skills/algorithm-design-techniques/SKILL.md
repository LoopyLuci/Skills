---
name: algorithm-design-techniques
description: "Use when designing algorithms: greedy, DP, divide-conquer."
category: software-development
tags: [algorithms, design, greedy, dynamic-programming, backtracking]
---
# Algorithm Design Techniques

Core algorithm design paradigms.

## Greedy Algorithms

```python
# Make locally optimal choice at each step
# Works when local optimum = global optimum

# Activity Selection
def max_activities(intervals: list[tuple[int,int]]):
    intervals.sort(key=lambda x: x[1])  # sort by end time
    selected = [intervals[0]]
    for start, end in intervals[1:]:
        if start >= selected[-1][1]:
            selected.append((start, end))
    return selected
```

## Divide and Conquer

```python
# 1. Divide into subproblems
# 2. Conquer subproblems recursively
# 3. Combine results

def merge_sort(arr):
    if len(arr) <= 1: return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []; i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:] or right[j:])
    return result
```

## Dynamic Programming

```python
# Optimal substructure + overlapping subproblems
# Top-down (memoization) vs Bottom-up (tabulation)

# Longest Common Subsequence
def lcs(text1: str, text2: str) -> int:
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]
```

## Backtracking

```python
# Explore all candidates, abandon (prune) when impossible

# N-Queens
def solve_n_queens(n: int) -> list[list[str]]:
    result = []
    cols, diag1, diag2 = set(), set(), set()

    def backtrack(row, board):
        if row == n:
            result.append(["".join(r) for r in board])
            return
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            cols.add(col); diag1.add(row - col); diag2.add(row + col)
            board[row][col] = 'Q'
            backtrack(row + 1, board)
            board[row][col] = '.'
            cols.remove(col); diag1.remove(row - col); diag2.remove(row + col)

    backtrack(0, [['.']*n for _ in range(n)])
    return result
```

## Binary Search (Advanced)

```python
# Search in sorted rotated array
def search_rotated(nums: list[int], target: int) -> int:
    l, r = 0, len(nums) - 1
    while l <= r:
        mid = (l + r) // 2
        if nums[mid] == target: return mid
        if nums[l] <= nums[mid]:  # left half sorted
            if nums[l] <= target < nums[mid]:
                r = mid - 1
            else:
                l = mid + 1
        else:  # right half sorted
            if nums[mid] < target <= nums[r]:
                l = mid + 1
            else:
                r = mid - 1
    return -1
```

## Pitfalls

- Greedy fails when choices have future consequences
- DP needs well-defined state and transition — wrong state = wrong answer
- Backtracking without pruning is brute force — always prune
- Binary search edge cases: off-by-one on l/r bounds
- Divide and conquer has log n depth; recursion may overflow for large n
