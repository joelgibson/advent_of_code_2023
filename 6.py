import re
import itertools
import functools
import operator
import dataclasses
import math

def product(vals):
    return functools.reduce(operator.mul, vals, 1)

lines = '''
Time:      7  15   30
Distance:  9  40  200
'''.strip().split('\n')

lines = open('6.txt').read().strip().split('\n')

TIMES = [int(x) for x in lines[0].split()[1:]]
DISTS = [int(x) for x in lines[1].split()[1:]]

def ways_to_win(max_time, best_dist):
    return sum(1 for h in range(max_time) if dist(h, max_time) > best_dist)


def ways_to_win_2(max_time, best_dist):
    delta = max_time**2 - 4*best_dist
    left = (-max_time - delta**0.5)/2
    right = (-max_time + delta**0.5)/2
    return math.floor(right) - math.ceil(left) + 1


def dist(hold, max_time):
    if not 0 <= hold < max_time:
        return 0
    
    return (max_time - hold) * hold


print(product(ways_to_win_2(TIMES[i], DISTS[i]) for i in range(len(TIMES))))

print(ways_to_win(35696887, 213116810861248))