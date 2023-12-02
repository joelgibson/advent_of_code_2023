lines = open('1.txt').read().strip().split('\n')

DIGITS = {str(n): n for n in range(10)}
WORDS = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9}

def solve(line: str, nums: dict[str, int]) -> int:
    digits = [
        num
        for i in range(len(line))
        for word, num in nums.items()
        if line[i:].startswith(word)
    ]
    return 10 * digits[0] + digits[-1]

print(sum(solve(line, DIGITS) for line in lines))
print(sum(solve(line, DIGITS | WORDS) for line in lines))