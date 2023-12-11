import itertools

lines = '''
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
'''.strip().split('\n')

lines = open('11.txt').read().strip().split('\n')


def transpose(lines: list[str]) -> list[str]:
    return [''.join(col) for col in zip(*lines)]

def weights(lines: list[str], factor: int) -> list[int]:
    return [
        factor if all(lines[i][j] == '.' for j in range(len(lines[0]))) else 1
        for i in range(len(lines))
    ]

def dist(src, dest, row_weights, col_weights):
    (a, b), (c, d) = src, dest
    return sum(row_weights[min(a, c) + 1 : max(a, c) + 1]) + sum(col_weights[min(b, d) + 1 : max(b, d) + 1])


def problem(lines: list[str], factor: int):
    row_weights = weights(lines, factor)
    col_weights = weights(transpose(lines), factor)
    positions = [
        (i, j)
        for i, line in enumerate(lines)
        for j, c in enumerate(line)
        if c == '#'
    ]
    return sum(
        dist(src, dst, row_weights, col_weights)
        for src, dst in itertools.combinations(positions, 2)
    )

print(problem(lines, 2))
print(problem(lines, 1_000_000))