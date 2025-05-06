"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    if x_count > o_count:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] is EMPTY}


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    if i < 0 or i > 2 or j < 0 or j > 2:
        raise ValueError("Invalid action")
    if board[i][j] is not EMPTY:
        raise ValueError("Invalid action")
    new_board = [row[:] for row in board]
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in board:
        if row.count(X) == 3:
            return X
        if row.count(O) == 3:
            return O
    for col in range(3):
        if all(board[row][col] == X for row in range(3)):
            return X
        if all(board[row][col] == O for row in range(3)):
            return O
    if board[0][0] == board[1][1] == board[2][2] == X:
        return X
    if board[0][0] == board[1][1] == board[2][2] == O:
        return O
    if board[0][2] == board[1][1] == board[2][0] == X:
        return X
    if board[0][2] == board[1][1] == board[2][0] == O:
        return O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    for row in board:
        for cell in row:
            if cell is EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_value = winner(board)
    if winner_value == X:
        return 1
    elif winner_value == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    player_now = player(board)
    alpha = -math.inf
    beta = math.inf
    if terminal(board):
        return None
    if player_now == X:
        value = -math.inf
        best_action = None
        for action in actions(board):
            new_board = result(board, action)
            move_value = min_value(new_board,alpha, beta)
            if move_value > value:
                value = move_value
                best_action = action
                alpha = max(alpha, value)
        return best_action
    else:  
        value = math.inf
        best_action = None
        for action in actions(board):
            new_board = result(board, action)
            move_value = max_value(new_board , alpha, beta)
            if move_value < value:
                value = move_value
                best_action = action
                beta = min(beta, value)
        return best_action
    
    


def max_value(board , alpha , beta):
    if terminal(board):
        return utility(board)
    value = -math.inf
    for action in actions(board):
        new_board = result(board, action)

        value = max(value, min_value(new_board , alpha , beta))
        if value >= beta:
            return value
        alpha = max(alpha, value)
    return value




def min_value(board , alpha , beta):
    if terminal(board):
        return utility(board)
    value = math.inf
    for action in actions(board):
        new_board = result(board, action)
        value = min(value, max_value(new_board , alpha, beta))
        if value <= alpha:
            return value
        beta = min(beta, value)
    return value
