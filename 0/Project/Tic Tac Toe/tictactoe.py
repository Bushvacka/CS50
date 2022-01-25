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
    moves = 0
    for row in board:
        for spot in row:
            if spot:
                moves += 1
    return X if moves % 2 == 0 else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = []
    for i, row in enumerate(board):
        for j, spot in enumerate(row):
            if(spot is EMPTY):
                actions.append((i, j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    #Make a copy of the current board
    newBoard = [[], [], []]
    for i in range(len(board)):
        for j in range(len(board[i])):
            newBoard[i].insert(j, board[i][j])
    #Apply the action to the copied board
    newBoard[action[0]][action[1]] = player(board)
    return newBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if rowCheck(board):
        return rowCheck(board)
    if diagnolCheck(board):
        return diagnolCheck(board)
    if verticalCheck(board):
        return verticalCheck(board)
    
def rowCheck(board):
    """
    Checks row win condition
    Returns X, O, or False
    """
    for row in board:
        rSet = set(row)
        if len(rSet) == 1 and EMPTY not in rSet:
            if X in rSet:
                return X
            else:
                return O
    return False

def diagnolCheck(board):
    """
    Checks diagnol win condition
    Returns X, O, or False
    """
    dSet = set(board[i][i] for i in range(len(board)))
    if len(dSet) == 1 and EMPTY not in dSet:
        if X in dSet:
            return X
        else:
            return O
    dSet = set(board[i][len(board)-i-1] for i in range(len(board)))
    if len(dSet) == 1 and EMPTY not in dSet:
        if X in dSet:
            return X
        else:
            return O
    return False

def verticalCheck(board):
    """
    Checks vertical win condition
    Returns X, O, or False
    """
    for j in range(len(board)):
        vSet = set(board[i][j] for i in range(len(board)))
        if len(vSet) == 1 and EMPTY not in vSet:
            if X in vSet:
                return X
            else:
                return O
    return False

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    #Check for a full board
    c = 0
    for row in board:
        for spot in row:
            if spot:
                c+=1
    if c >= 9:
        return True
    #Check for win conditions
    if rowCheck(board) or diagnolCheck(board) or verticalCheck(board):
        return True
    #If we reach this, the game is not complete
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winUser = winner(board)
    if winUser == X:
        return 1
    elif winUser == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    Makes use of Alpha-Beta Pruning
    """
    if terminal(board):
        return None
    actionValues = {}
    if player(board) == X:
        for action in actions(board):
            actionValues[action] = minValue(result(board, action), -100, 100)
    else:
        for action in actions(board):
            actionValues[action] = maxValue(result(board, action), -100, 100)
    if player(board) == X:
        best_action = max(actionValues, key=actionValues.get)
    else:
        best_action = min(actionValues, key=actionValues.get)
    return best_action
    
        
def maxValue(board, alpha, beta):
    if terminal(board):
        return utility(board)
    v = -100
    for action in actions(board):
        v = max(v, minValue(result(board, action), alpha, beta))
        alpha = max(alpha, v)
        if alpha >= beta:
            break
    return v

def minValue(board, alpha, beta):
    if terminal(board):
        return utility(board)
    v = 100
    for action in actions(board):
        v = min(v, maxValue(result(board, action), alpha, beta))
        beta = min(beta, v)
        if beta <= alpha:
            break
    return v