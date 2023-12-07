# I wrote this very fast it's kinda bad lol.

import re
import itertools
import functools
import operator
import dataclasses

def product(vals):
    return functools.reduce(operator.mul, vals, 1)

lines = '''
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4

'''.strip().split('\n\n')

lines = open('5.txt').read().strip().split('\n\n')


@dataclasses.dataclass
class Range:
    dst_start: int
    src_start: int
    length: int

    @property
    def a(self) -> int:
        return self.src_start
    
    @property
    def b(self) -> int:
        return self.src_start + self.length
    
    def contains(self, n: int) -> bool:
        return self.src_start <= n < self.src_start + self.length

    def apply(self, n: int) -> int:
        return self.dst_start + (n - self.src_start)
    

SEEDS = [int(x) for x in lines[0].split()[1:]]
MAPS = [
    [Range(*(int(x) for x in line.split())) for line in block.split('\n')[1:]]
    for block in lines[1:]
]

def map_seed(seed: int, map: list[Range]):
    for range in map:
        if range.src_start <= seed < range.src_start + range.length:
            return range.dst_start + (seed - range.src_start)

    return seed

def many_map_seed(seed: int):
    for map in MAPS:
        seed = map_seed(seed, map)
    
    return seed

def map_interval(a: int, b: int, maps: list[Range]) -> list[tuple[int, int]]:
    """Map [a, b) through the range, returning a list of intervals."""
    assert a < b
    ret = []
    while a < b:
        # Are there any ranges containing a?
        contains_a = [r for r in maps if r.contains(a)]
        if contains_a:
            # Map the largest subinterval and recurse.
            r, = contains_a
            end = min(b, r.b)
            assert r.apply(a) < r.apply(end)
            ret += [(r.apply(a), r.apply(end))]
            a = end
            continue

        # Otherwise, are there any ranges overlapping this interval?
        overlapping = [r for r in maps if a < r.a <= b]
        if overlapping:
            o, = overlapping
            assert a < o.a
            ret += [(a, o.a)]
            a = o.a
            continue

        ret += [(a, b)]
        a = b
    
    return ret
        

print(min(many_map_seed(seed) for seed in SEEDS))

PAIRS = list(zip(SEEDS[::2], SEEDS[1::2]))
PAIRS = [(a, a+l) for a, l in PAIRS]

def map_many_interval(pairs: list[tuple[int, int]]) -> list[tuple[int, int]]:
    for i, map in enumerate(MAPS):
        #print("map", i)
        pairs = [result for a, b in pairs for result in map_interval(a, b, map)]
    
    return pairs


for pair in PAIRS:
    print(pair, min(a for a, b in map_many_interval([pair])))

print(min(
    a
    for pair in PAIRS
    for a, b in map_many_interval([pair])
    
))