lines = '''
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
'''.strip().split('\n')

lines = open('18.txt').read().strip().split('\n')

U = (-1, 0)
D = (1, 0)
L = (0, -1)
R = (0, 1)

parsed = [
    (udlr, int(dist), int(colour[2:-1], 16))
    for line in lines
    for udlr, dist, colour in [line.split()]
]
moves_1 = [
    (di * dist, dj * dist)
    for udlr, dist, _ in parsed
    for di, dj in [{'U': U, 'D': D, 'L': L, 'R': R}[udlr]]
]
moves_2 = [
    (di * (hex // 16), dj * (hex // 16))
    for _, _, hex in parsed
    for di, dj in [[R, D, L, U][hex % 16]]
]

def area(moves: list[tuple[int, int]]) -> int:
    x, y = 0, 0
    integral = 0
    length = 0
    for dx, dy in moves:
        integral += x * dy
        length += abs(dx) + abs(dy)
        x, y = x + dx, y + dy
    
    return abs(integral) + length // 2 + 1

print(area(moves_1))
print(area(moves_2))
