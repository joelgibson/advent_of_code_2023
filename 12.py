from typing import Iterable, TypeVar, Sequence
from collections import Counter

T = TypeVar('T')

# Accumulate a list of (key, count) pairs into a dict, adding counts when keys are repeated.
def accumulate_dict(counts: Iterable[tuple[T, int]]) -> Counter[T]:
    result = Counter()
    for key, count in counts:
        result[key] += count
    
    return result


# A partially evaluated line can be represented as a "state" (vector, trailing_char), in such a
# way that we can still know how to append a new char on the end. Some example states:
#     ..####..#. => ((4, 1), .)
#     .##.##.### => ((2, 2, 3), #)
# The rules for appending a . or # at the end depend on what the current trailing character is.
# For instance:
#     ((2, 2, 3), #) append #  =>  ((2, 2, 4), #)
# We can also prune later on, for instance we know that ((2, 2, 4), #) can only ever be associated
# with a vector starting with (2, 2, ...); note we can't assume anything about the 4 yet 
State = tuple[tuple[int, ...], str]
def append(state: State, char: str):
    assert char in '.#'
    vec, trailing = state
    match (trailing, char):
        case ('.', '#'): return ((*vec, 1), '#')
        case ('.', '.'): return (vec, '.')
        case ('#', '#'): return ((*vec[:-1], vec[-1] + 1), '#')
        case ('#', '.'): return (vec, '.')


# Accumulate counts from left to right, pruning down to states which could be prefixes of
# the reference vector.
def count_states(line: str, reference: tuple[int]) -> Counter[State]:
    counts = Counter([((), '.')])                     # Start with a count of 1 in the empty state.
    
    #print(reference)
    for c in line:                                    # Iterate the line from left to right, appending on each character to the state counts.
        counts = accumulate_dict([
            ((vec, trail), count)
            for state, count in counts.items()        # Iterate over existing states and their counts,
            for char in ('#.' if c == '?' else c)     # Where char is either a literal . or #, or both if ?
            for vec, trail in [append(state, char)]   # Producing the new state,
            if (                                      # Pruning criteria to rule out vecs which cannot be a prefix of the reference:
                len(vec) <= len(reference)                           # Vec cannot exceed reference length.    
                and vec[:-1] == reference[:len(vec[:-1])]            # All but the last entry must match.
                and (vec == () or vec[-1] <= reference[len(vec)-1])  # The last entry of vec must be at most the corresponding reference entry.
            )
        ])

    # Accumulate only the vectors, we don't care about the trailing character now.
    return accumulate_dict([(vec, count) for (vec, char), count in counts.items()])


pairs = [
    (left, tuple(int(x) for x in right.split(',')))
    for line in open('12.txt').read().strip().split('\n')
    for left, right in [line.split()]
]
print(sum(count_states(line, vector)[vector] for line, vector in pairs))
print(sum(count_states('?'.join([line]*5), vector*5)[vector*5] for line, vector in pairs))