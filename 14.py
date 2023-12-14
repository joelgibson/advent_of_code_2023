Board = tuple[str, ...]
board = tuple(open('14.txt').read().strip().split('\n'))


def transpose(board: Board) -> Board:
    return tuple(map(''.join, zip(*board)))

def rotate_right(board: Board) -> Board:
    return tuple(line[::-1] for line in transpose(board))

def rotate_left(board: Board) -> Board:
    return rotate_right(rotate_right(rotate_right(board)))

def push_left(board: Board) -> Board:
    return tuple(
        '#'.join('O' * part.count('O') + '.' * part.count('.') for part in line.split('#'))
        for line in board
    )

def load(board: Board) -> int:
    return sum((len(board) - i) * line.count('O') for i, line in enumerate(board))

MOVES = {'L': rotate_left, 'R': rotate_right, 'P': push_left}
def spin_cycle(board: Board) -> Board:
    for move in 'LPRPRPRPRR':
        board = MOVES[move](board)
    
    return board

def spin_times(board: Board, desired: int) -> list[str]:
    cycle = 0
    seen = {board: 0}

    while True:
        board = spin_cycle(board)
        cycle += 1
        
        if board in seen:
            break
        else:
            seen[board] = cycle

    print(f"Cycle found: spin({cycle}) = spin({seen[board]})")
    remainder = (desired - cycle) % (cycle - seen[board])
    for _ in range(remainder):
        board = spin_cycle(board)
    
    return load(board)

print(load(rotate_right(push_left(rotate_left(board)))))
print(load(spin_times(board, 1_000_000_000)))