SEQS = [
    [int(x) for x in line.split()]
    for line in open('9.txt').read().strip().split('\n')
]

def extrapolate(seq):
    if not seq:
        return 0

    diffs = [i - j for i, j in zip(seq[1:], seq[:-1])]
    return seq[-1] + extrapolate(diffs)

print(sum(map(extrapolate, SEQS)))
print(sum(extrapolate(nums[::-1]) for nums in SEQS))