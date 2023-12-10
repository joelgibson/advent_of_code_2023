from collections import defaultdict

LINES = '''
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
'''.strip().split('\n')

LINES = open('10.txt').read().strip().split('\n')

N, E, S, W = ((-1, 0), (0, 1), (1, 0), (0, -1))

DIRS = {
    '|': (N, S),
    '-': (E, W),
    'L': (N, E),
    'J': (N, W),
    '7': (S, W),
    'F': (S, E),
}

S_POS = [(i, j) for i, line in enumerate(LINES) for j, c in enumerate(line) if c == 'S'][0]

Pair = tuple[int, int]

def make_graph(lines: list[str]) -> dict[Pair, set[Pair]]:
    # Create a directed graph, counting . and S as missing. (May have edges incoming, none outgoing)
    adj = defaultdict(set)
    for i, line in enumerate(LINES):
        for j, c in enumerate(line):
            for di, dj in DIRS.get(c, []):
                adj[i, j] |= {(i + di, j + dj)}
    
    return adj

def find_cycle(adj: dict[Pair, set[Pair]], start: Pair) -> list[Pair]:
    # Find a path beginning at one of the four places around start, and returning to start.
    # Return the cycle of positions [start, ..., start].
    
    for di, dj in [N, S, E, W]:
        node = (start[0] + di, start[1] + dj)
        if start not in adj[node]:
            continue

        path = [start]
        while True:
            nexts = adj[node] - {path[-1]}
            if len(nexts) != 1:
                break
            
            path += [node]
            node, = nexts
            if node == start:
                return path


def enclosed_area(cycle: list[Pair]) -> int:
    # According to Green's theorem, the area enclosed by a curve is the path integral of (i dj).
    # We need to subtract half the cycle length for the overcounting of half-tiles, then
    # add 1 for the under-counting of corner tiles.

    integral = 0
    for (i, j), (x, y) in zip(cycle[:-1], cycle[1:]):
        integral += i * (y - j)

    return abs(integral) - len(cycle) // 2 + 1


adj = make_graph(LINES)
cycle = find_cycle(adj, S_POS)

print(len(cycle) // 2)  # Part 1
print(enclosed_area(cycle))  # Part 2