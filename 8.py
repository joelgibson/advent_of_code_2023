import itertools
import math

lines = '''
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
'''.strip().split('\n')

lines = open('8.txt').read().strip().split('\n')

DIRS = lines[0]
MAP = {
    a: (left, right)
    for line in lines[2:]
    for a, b in [line.split(' = ')]
    for left, right in [b[1:-1].split(', ')]
}

def dist(node, should_stop):
    steps = 0
    for rl in itertools.cycle(DIRS):
        node = MAP[node][0] if rl == 'L' else MAP[node][1]
        steps += 1
        if should_stop(node):
            return steps


# Part 1
print(dist('AAA', lambda node: node == 'ZZZ'))

# Part 2
dists = [
    dist(node, lambda n: n[-1] == 'Z')
    for node in MAP.keys()
    if node[-1] == 'A'
]
print(math.lcm(*dists))