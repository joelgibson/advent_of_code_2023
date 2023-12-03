import re
import itertools
import functools
import operator

def product(vals):
    return functools.reduce(operator.mul, vals, 1)


lines = '''
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
'''.strip().split('\n')

lines = open('3.txt').read().strip().split('\n')


total = 0
gears = {}
for i in range(len(lines)):
    for match in re.finditer('[0-9]+', lines[i]):
        jl, jr = match.start(), match.end()
        number = int(lines[i][jl:jr])
        block = ''.join([line[max(jl-1, 0):jr+1] for line in lines[max(i-1, 0):i+2]])
        if re.search('[^.0-9]', block):
            total += number
        
        # Inserted this bit for part 2
        for x in range(max(i-1, 0), min(i+2, len(lines))):
            for y in range(max(jl-1, 0), min(jr + 1, len(lines[0]))):
                if lines[x][y] == '*':
                    gears[x, y] = gears.get((x, y), []) + [number]

print(total)
print(sum(product(vals) for vals in gears.values() if len(vals) == 2))