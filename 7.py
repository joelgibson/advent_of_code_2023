# Not what I submitted for the competition.

from collections import Counter

PAIRS: list[tuple[str, int]] = [
    (hand, int(bid))
    for line in open('7.txt').read().strip().split('\n')
    for hand, bid in [line.split()]
]


# Maps a hand to an integer partition of 5, eg 'KTJJT' => (2, 2, 1)
def hand_code(hand: str) -> tuple[int, ...]:
    return tuple(sorted(Counter(hand).values(), reverse=True))

def rank(hand: str):
    return (hand_code(hand), *map('23456789TJQKA'.index, hand))

def rank_jokered(hand: str):
    code = hand_code(hand.replace('J', ''))
    if not code:  # JJJJJ
        code = (0,)
    
    return ((code[0] + hand.count('J'), *code[1:]), *map('J23456789TQKA'.index, hand))

def solve(pairs, rank_fn):
    return sum(
        rank * bid
        for rank, (hand, bid)
        in enumerate(sorted(pairs, key=lambda pair: rank_fn(pair[0])), 1)
    )

print(solve(PAIRS, rank))
print(solve(PAIRS, rank_jokered))