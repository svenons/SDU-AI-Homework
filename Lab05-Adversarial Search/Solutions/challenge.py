import copy

BOARD_SIZE = 8
WHITE, BLACK, EMPTY = 'W', 'B', '.'

def initial_board():
    board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    for col in range(BOARD_SIZE):
        board[0][col] = WHITE
        board[1][col] = WHITE
        board[6][col] = BLACK
        board[7][col] = BLACK
    return board

def print_board(board):
    for row in board:
        print(' '.join(row))
    print()

def get_opponent(player):
    return BLACK if player == WHITE else WHITE

def is_terminal(board, player):
    opponent = get_opponent(player)
    # Win if any piece reaches home row
    if player == WHITE and any(cell == WHITE for cell in board[BOARD_SIZE-1]):
        return True
    if player == BLACK and any(cell == BLACK for cell in board[0]):
        return True
    # Lose if no pieces left
    white_exists = any(cell == WHITE for row in board for cell in row)
    black_exists = any(cell == BLACK for row in board for cell in row)
    return not white_exists or not black_exists

def evaluate(board, player):
    """
    Simple evaluation: number of pieces + distance to goal.
    Positive = good for 'player', negative = good for opponent.
    """
    score = 0
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == player:
                score += 10
                if player == WHITE:
                    score += r  # closer to row 7
                else:
                    score += (7 - r)
            elif board[r][c] == get_opponent(player):
                score -= 10
    return score

def generate_moves(board, player):
    moves = []
    direction = 1 if player == WHITE else -1
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == player:
                for dc in [-1, 0, 1]:
                    nr, nc = r + direction, c + dc
                    if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                        target = board[nr][nc]
                        if dc == 0 and target == EMPTY:
                            # Forward move
                            new_board = copy.deepcopy(board)
                            new_board[r][c] = EMPTY
                            new_board[nr][nc] = player
                            moves.append(new_board)
                        elif dc != 0 and target in [EMPTY, get_opponent(player)]:
                            # Diagonal move or capture
                            new_board = copy.deepcopy(board)
                            new_board[r][c] = EMPTY
                            new_board[nr][nc] = player
                            moves.append(new_board)
    return moves

def alpha_beta_search(board, depth, player):
    def max_value(state, alpha, beta, depth):
        if is_terminal(state, player) or depth == 0:
            return evaluate(state, player), state
        v, best_move = float('-inf'), None
        for move in generate_moves(state, player):
            val, _ = min_value(move, alpha, beta, depth - 1)
            if val > v:
                v, best_move = val, move
            if v >= beta:
                return v, best_move
            alpha = max(alpha, v)
        return v, best_move

    def min_value(state, alpha, beta, depth):
        opponent = get_opponent(player)
        if is_terminal(state, opponent) or depth == 0:
            return evaluate(state, player), state
        v, best_move = float('inf'), None
        for move in generate_moves(state, opponent):
            val, _ = max_value(move, alpha, beta, depth - 1)
            if val < v:
                v, best_move = val, move
            if v <= alpha:
                return v, best_move
            beta = min(beta, v)
        return v, best_move

    _, best_state = max_value(board, float('-inf'), float('inf'), depth)
    return best_state

def play_breakthrough():
    board = initial_board()
    current_player = WHITE
    depth = 3

    while not is_terminal(board, current_player):
        print_board(board)
        print(f"{current_player}'s turn...")
        board = alpha_beta_search(board, depth, current_player)
        current_player = get_opponent(current_player)

    print_board(board)
    print(f"{get_opponent(current_player)} wins!")

if __name__ == "__main__":
    play_breakthrough()