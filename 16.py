import re
import itertools
import functools
import operator
import dataclasses
import math

def product(vals):
    return functools.reduce(operator.mul, vals, 1)

lines = r'''

'''.strip().split('\n')

lines = open('16.txt').read().strip().split('\n')

# (i, j), (di, dj)
State = tuple[int, int, int, int]

def new_directions(char: str, di: int, dj: int) -> list[tuple[int, int]]:
    assert di*dj == 0 and abs(di) <= 1 and abs(dj) <= 1, f"{(di, dj)}"
    match char:
        case '.':
            return [(di, dj)]
        case '/':
            return [(-dj, -di)]
        case '\\':
            return [(dj, di)]
        case '|':
            if di != 0: # Moving vertically
                return [(di, dj)]
            elif di == 0:
                return [(1, 0), (-1, 0)]
        case '-':
            if dj != 0: # Moving horizontally
                return [(di, dj)]
            elif dj == 0:
                return [(0, 1), (0, -1)]
        case _:
            assert False, f"Found character {char}"

def drive(map: list[str], start: State):
    states = [start]
    energised = set()
    en = [
        ['.']*len(map[0]) for _ in range(len(map))
    ]
    seen_states = set()
    while states:
        new_states = []
        seen_states |= set(states)
        for i, j, di, dj in states:
            if not (0 <= i < len(map) and 0 <= j < len(map[0])):
                continue

            energised |= {(i, j)}
            en[i][j] = '#'
            new_states += [
                (i + new_di, j + new_dj, new_di, new_dj)
                for new_di, new_dj in new_directions(map[i][j], di, dj)
            ]
        
        states = set(new_states) - seen_states
    
    #print('\n'.join(''.join(line) for line in en))
    return len(energised)

print(drive(lines, (0, 0, 0, 1)))

starts = [
    *[(i, 0, 0, 1) for i in range(len(lines))],  # Left edge
    *[(i, len(lines[0]) - 1, 0, -1) for i in range(len(lines))],  # Right edge
    *[(0, j, 1, 0) for j in range(len(lines[0]))],  # Top edge
    *[(len(lines) - 1, j, -1, 0) for j in range(len(lines[0]))],  # Bottom edge
]
print(max(drive(lines, start) for start in starts))