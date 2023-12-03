import re
import itertools
import functools
import operator

lines = '''
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
'''.strip().split('\n')

lines = open('2.txt').read().strip().split('\n')

LIM = {'red': 12, 'green': 13, 'blue': 14}

def parse_game(line):
    _, rest = line.split(': ')
    rounds = []
    for part in rest.split('; '):
        round = {}
        for thing in part.split(', '):
            num, colour = thing.split()
            round[colour] = round.get(colour, 0) + int(num)
        
        rounds += [round]
    
    return rounds

def game_possible(game):
    for round in game:
        for colour, count in round.items():
            if count > LIM[colour]:
                return False
    return True


count = 0
for i, line in enumerate(lines, 1):
    if game_possible(parse_game(line)):
        count += i


def min_cubes(game):
    mins = {colour: 0 for colour in LIM}
    for round in game:
        for colour, count in round.items():
            mins[colour] = max(mins[colour], count)
    
    return functools.reduce(operator.mul, mins.values())

powers = 0
for line in lines:
    powers += min_cubes(parse_game(line))

print(powers)