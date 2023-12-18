import re
import itertools
import functools
import operator
import dataclasses
import math
from collections import defaultdict
import heapq

def product(vals):
    return functools.reduce(operator.mul, vals, 1)

lines = r'''
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
'''.strip().split('\n')

lines = open('17.txt').read().strip().split('\n')

board = [list(map(int, line)) for line in lines]

U = (-1, 0)
D = (1, 0)
L = (0, -1)
R = (0, 1)

VERT = (U, D)
HORIZ = (L, R)

# Each (i, j) position on the board becomes two nodes (i, j, axis) where axis = VERT or HORIZ.
# Outgoing paths from a VERT node must be in the vertical direction, and leading to a HORIZ node,
# and vice-versa.
def build_graph(board: list[list[int]], rs: list[int]):
    adj = defaultdict(list)
    for i, j, axis in itertools.product(range(len(board)), range(len(board[0])), [VERT, HORIZ]):
        comp_axis = VERT if axis == HORIZ else HORIZ
        for di, dj in axis:
            weight = 0
            for r in rs:
                x, y = i + di*r, j + dj*r
                if not (0 <= x < len(board) and 0 <= y < len(board[0])):
                    continue

                weight = sum(board[i + di*s][j + dj*s] for s in range(1, 1+r))
                adj[(i, j, axis)] += [((x, y, comp_axis), weight)]
    
    return adj

def djikstra(adj, source):
    dist = {node: float('inf') for node in adj}
    prev = {node: node for node in adj}

    dist[source] = 0

    queue = [(0, source)]
    visited = set()

    while queue:
        _, node = heapq.heappop(queue)
        if node in visited:
            continue

        visited.add(node)

        for neigh, weight in adj[node]:
            if dist[node] + weight < dist[neigh]:
                dist[neigh] = dist[node] + weight
                prev[neigh] = node
                heapq.heappush(queue, (dist[neigh], neigh))
    
    return dist, prev


def best_distance(board: list[list[int]], rs: list[int]) -> int:
    adj = build_graph(board, rs)
    return min([
        dist[len(board) - 1, len(board[0]) - 1, end_axis]
        for start_axis in [VERT, HORIZ]
        for dist, prev in [djikstra(adj, (0, 0, start_axis))]
        for end_axis in [VERT, HORIZ]
    ])

print(best_distance(board, [1, 2, 3]))
print(best_distance(board, [4, 5, 6, 7, 8, 9, 10]))