blocks = '''
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
'''.split('\n\n')


blocks = open('13.txt').read().strip().split('\n\n')

def transpose(lines: list[str]) -> list[str]:
    return [''.join(col) for col in zip(*lines)]

def mismatch_row(lines: list[str], i: int, j: int):
    assert i + 1 == j
    return sum(
        1
        for rowi, rowj in zip(lines[:i+1][::-1], lines[j:])
        for x, y in zip(rowi, rowj)
        if x != y
    )

def refl_row(lines: list[str], smudge: bool = False):
    for l, r in zip(range(len(lines)), range(1, len(lines))):
        err = mismatch_row(lines, l, r)
        if (not smudge and err == 0) or (smudge and err == 1):
            return l + 1

    return 0

count = 0
count_smudge = 0
for block in blocks:
    lines = [line.strip() for line in block.split()]

    count += refl_row(transpose(lines)) + 100*refl_row(lines)
    count_smudge += refl_row(transpose(lines), smudge=True) + 100*refl_row(lines, smudge=True)

print(count)
print(count_smudge)