'''PlayerSkeletonA.py
An agent that plays Baroque Chess.
Designed by Fan Yu (fany23) and Dan Wang (daw1230)
'''
import BC_state_etc as BC
import DD_BC_module_zobrist_hashing as zh
import time 
import random

g_useBasicStaticEval = False
g_useZobristHashing = True
n_states_expanded = 0
n_static_evals = 0
n_cutoffs = 0
n_zobrist_hasing = 0
I=J=H=PP=QQ = 0
best_move = []
Player2 = None
best_val = 0

BLACK = 0
WHITE = 1
NEIGHBORS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
BASIC_SCORES = [0, 0, -1, 1, -2, 2, -2, 2, -2, 2, -2, 2, -100, 100, -2, 2]
STATIC_SCORES = [0, 0, 10, 10, 40, 40, 10, 10, 10, 10, 40, 40, 200, 200, 10, 10]
PINCER_MOVES = [(-1, 0), (0, -1), (1, 0), (-1, 0)]
QUEEN_LIKE_MOVES = [(-1, 0), (0, -1), (1, 0), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
my_move = WHITE

def parameterized_minimax(currentState, alphaBeta=False, ply=3,\
    useBasicStaticEval=True, useZobristHashing=False):
    '''Implement this testing function for your agent's basic
    capabilities here.'''
    global n_states_expanded, n_static_evals, n_cutoffs
    
    g_useBasicStaticEval = useBasicStaticEval
    g_useZobristHashing = useZobristHashing    
    if current_state == None:
      raise ValueError("No State entered")

    n_states_expanded = 0
    n_static_evals = 0
    n_cutoffs = 0
    alpha = float('-inf')
    beta = float('inf')

    start = time.time()
    time_limit = 10000 #no time limit

    """By using different variables, the function can achieve minimax,
    minimax with alpha-beta pruning"""
    current_state_static_val = minimax(currentState, ply, alphaBeta, start, time_limit, alpha, beta)
    
    DATA = {}
    DATA['CURRENT_STATE_STATIC_VAL'] = current_state_static_val
    DATA['N_STATES_EXPANDED'] = n_states_expanded
    DATA['N_STATIC_EVALS'] = n_static_evals
    DATA['N_CUTOFFS'] = n_cutoffs
    return(DATA)

def minimax(currentState, plyLeft, alphaBeta, start, time_limit, alpha, beta):
    global n_states_expanded, n_static_evals, n_cutoffs,\
           best_val, n_zobrist_hasing    
    successors = nextMove(currentState)
    n_states_expanded += 1
    if plyLeft == 0 or not successors:     
        if g_useZobristHashing:
            hashValue = zh.hash_state(currentState)
            if hashValue in zh.zobrist_table:
                val = zh.zobrist_table[hashValue]
                n_zobrist_hasing += 1
            else:
                if g_useBasicStaticEval:
                    val = basicStaticEval(currentState)
                else:
                    val = staticEval(currentState)
                zh.zobrist_table[hashValue] = val
                n_static_evals += 1
        else:
            if g_useBasicStaticEval:
                val = basicStaticEval(currentState)
            else:
                val = staticEval(currentState)
            n_static_evals += 1
        return val 

    if currentState.whose_move == WHITE:
        provisional = float('-inf')
    else:
        provisional = float('inf')

    for new in successors:
        if time.time() - start < time_limit:
            newState = new[0]
            newVal = minimax(newState, plyLeft-1, alphaBeta, start, time_limit, alpha, beta)
            if currentState.whose_move == WHITE and newVal > provisional:
                provisional = newVal
                alpha = max(provisional, alpha)
                if alphaBeta and alpha>=beta:
                    n_cutoffs = n_cutoffs + 1
                    break
            elif currentState.whose_move == BLACK and newVal < provisional:
                provisional = newVal
                beta = min(provisional, beta)
                if alphaBeta and alpha>=beta:
                    n_cutoffs = n_cutoffs + 1
                    break
    return provisional

def makeMove(currentState, currentRemark, timelimit=10):
    global my_move
    my_move = currentState.whose_move
    successors = nextMove(currentState)

    depth = 1
    best_val = float('-inf')
    best_move = None
    timeLeft = timelimit
    while True:
        for new in successors:
            start_time = time.time()
            value = minimax(new[0], depth, True, start_time, timelimit, float('-inf'), float('inf'))
            end_time = time.time()
            timeLeft = timeLeft - (end_time - start_time)
            if value >= best_val:
                best_val = value
                best_move = [[new[1], new[0]], utterance(new[0], value)]
            if end_time - start_time + 0.2 * depth > timeLeft:
                return best_move
            if best_val > 20:
                return best_move
        depth = depth + 1

def utterance(currentState, val):
    global I,J,H,PP,QQ
    if val == 0:
      utter = ['This is a close game.','No one is winning.',\
                                 'No one is losing.','It is such a close game.',\
                                 'The odds of winning is the same.']
      utteran = utter[I%4]
      I = I + 1    
    if val > 0:
      if my_move == WHITE:
        utter = ['I am going to win.',\
                 "I have a clear advantage based on my evaluation.",\
                'I am winning.', 'Enjoying the game.',\
                'No conclusion but I have a greater chance to win.',\
                'Love the game!', 'Yeah winning.','Winning.','Wonderful game.',\
                 'What a good day.','My evaluation function is strong.',\
                 'Plause for my evaluation function.']
        utteran = utter[J%11]
        J = J + 1
      else:
        utter = ["You have a clear advantage based on my evaluation. Well Done ",\
                        'You are winning.', 'I am kind of losing.',"Well Done, "+ Player2,\
                        'Good job.', 'Nice move.', 'No, I am losing.']
        utteran = utter[H%6]
        H = H + 1
      
    if val < 0:
      if my_move == BLACK:
        utter = ['I am going to win.',\
                 "I have a clear advantage based on my evaluation.",\
                'I am winning.', 'Enjoying the game.',\
                'No conclusion but I have a greater chance to win.',\
                'Love the game!', 'Yeah winning.','Winning.','Wonderful game.',\
                 'What a good day.','My evaluation function is strong.',\
                 'Plause for my evaluation function.']
        utteran = utter[PP%11]
        PP = PP+1
      else:
        utter = ["You have a clear advantage based on my evaluation. Well Done ",\
                        'You are winning.', 'I am kind of losing.',"Well Done, "+ Player2,\
                        'Good job.', 'Nice move.', 'No, I am losing.']
        utteran = utter[QQ%6]
        QQ = QQ+1    
    return utteran 
    
def nickname():
    return "DD"

def introduce():
    return "I'm Donna Dude, new in Baroque Chess agent. I'm created by\
  Fan Yu (fany23) and Dan Wang (daw1230)"

# return format: [(new_state, move)]
# move format: (old_location, new_location)
# location format: (x, y)
def nextMove(state):
    board = state.board
    who = state.whose_move
    re = []
    for i in range(8):
        for j in range(8):
            curr = board[i][j]
            if curr == 0:
                # Empty
                continue
            elif (curr - who) % 2 != 0:
                # Opponent Piece
                continue
            elif cannotMove(state, i, j):
                continue
            else:
                curr_re = findAllMove(state, i, j)
                if curr_re:
                    re = re + curr_re 
    return re

def findAllMove(state, i, j):
    re = []
    pawn  = state.board[i][j]
    if pawn == 2 or pawn == 3:
        # Pincer
        re = PincerMove(state, i, j)
    elif pawn == 4 or pawn ==5:
        # Coordinator
        re = CoordinatorMove(state, i, j)
    elif pawn == 6 or pawn == 7:
        # Leaper
        re = LeaperMove(state, i, j)
    elif pawn == 8 or pawn == 9:
        # Imitator 
        return []
    elif pawn == 10 or pawn == 11:
        # Withdrawer
        re = WithdrawerMove(state, i, j)
    elif pawn == 12 or pawn == 13:
        # King
        re = KingMove(state, i, j)
    elif pawn == 14 or pawn == 15:
        # Freezer
        re = FreezerMove(state, i, j)
    return re

def PincerMove(state, i, j):
    re = []
    for dx, dy in PINCER_MOVES:
        for amplifier in range(8):
            x = dx * (1 + amplifier) + i
            y = dy * (1 + amplifier) + j
            if x < 0 or x > 7 or y < 0 or y > 7:
                break
            elif state.board[x][y] != 0:
                break
            else:
                new_state = copy(state)
                new_state.board[x][y] = 2 + new_state.whose_move # place pawn to new place
                new_state.board[i][j] = 0 # remove pawn from old place
                captures = [] # set of pawns to remove
                captures = PincerCapture(new_state, x, y)
                for r_x, r_y in captures:
                    new_state.board[r_x][r_y] = 0
                new_state.whose_move = 1 - new_state.whose_move
                re.append([new_state, ((i, j), (x, y))])
    return re

def PincerCapture(state, i, j):
    captures = []
    board = state.board
    whose_move = state.whose_move
    for dx, dy in PINCER_MOVES:
        if i + 2 * dx >= 0 and i + 2 * dx < 8 and j + 2 * dy >= 0 and j + 2 * dy < 8:
            if board[i + dx][j + dy] % 2 != whose_move and board[i + 2*dx][j + 2*dy] % 2 == whose_move and board[i + 2*dx][j + 2*dy] != 0:
                captures.append((i + dx, j + dy))
    return captures


def CoordinatorMove(state, i, j):
    re = []
    for dx, dy in QUEEN_LIKE_MOVES:
        for amplifier in range(8):
            x = dx * (1 + amplifier) + i
            y = dy * (1 + amplifier) + j
            if x < 0 or x > 7 or y < 0 or y > 7:
                break
            elif state.board[x][y] != 0:
                break
            else:
                new_state = copy(state)
                new_state.board[x][y] = 4 + new_state.whose_move # place pawn to new place
                new_state.board[i][j] = 0 # remove pawn from old place
                captures = [] # set of pawns to remove
                captures = CoordinatorCapture(new_state, x, y)
                for r_x, r_y in captures:
                    new_state.board[r_x][r_y] = 0
                new_state.whose_move = 1 - new_state.whose_move
                re.append([new_state, ((i, j), (x, y))])
    return re

def CoordinatorCapture(state, i, j):
    king = getKing(state)
    if not king:
        return []
    else:
        k_x = king[0]
        k_y = king[1]
    captures = []
    if state.board[i][k_y] and state.board[i][k_y] % 2 != state.whose_move:
        captures.append((i, k_y))
    if state.board[k_x][j] and state.board[k_x][j] % 2 != state.whose_move:
        captures.append((k_x, j))
    return captures

def getKing(state):
    board = state.board
    whose_move = state.whose_move
    for i in range(8):
        for j in range(8):
            if board[i][j] == 12 + whose_move:
                return (i, j)

def LeaperMove(state, i, j):
    re = []
    for dx, dy in QUEEN_LIKE_MOVES:
        for amplifier in range(8):
            x = dx * (1 + amplifier) + i
            y = dy * (1 + amplifier) + j
            if x < 0 or x > 7 or y < 0 or y > 7:
                break
            elif state.board[x][y] != 0:
                break
            else:
                new_state = copy(state)
                new_state.board[x][y] = 6 + state.whose_move
                new_state.board[i][j] = 0
                new_state.whose_move = 1 - state.whose_move
                re.append([new_state, ((i, j), (x, y))])
                next_x = x + dx
                next_y = y + dy
                n_next_x = x + dx * 2
                n_next_y = y + dy * 2
                # check if can make a captrue
                if n_next_x >= 0 and n_next_x < 8 and n_next_y >= 0 and n_next_y < 8:
                    if state.board[next_x][next_y] % 2 != state.whose_move and state.board[next_x][next_y] % 2 != 0 and state.board[n_next_x][n_next_y] == 0:
                        another_state = copy(new_state)
                        another_state.board[next_x][next_y] = 0
                        another_state.board[n_next_x][n_next_y] = 6 + state.whose_move
                        another_state.board[x][y] = 0
                        re.append([new_state, ((i, j), (n_next_x, n_next_y))])

'''
def ImitatorMove(state, i, j):
    re = []
    for dx, dy in QUEEN_LIKE_MOVES:
        for amplifier in range(8):
            x = dx * (1 + amplifier) + i
            y = dy * (1 + amplifier) + j
            if x < 0 or x > 7 or y < 0 or y > 7:
                break
            elif state.board[x][y] != 0:
                break
            elif state.board[x][y] == 12 + (1 - state.whose_move):
                new_state = copy(state)
                new_state.board[x][y] = 10 + state

            else:
                new_state = copy(state)
                new_state.board[x][y] = 10 + state

def ImitatorCapture:
'''

def WithdrawerMove(state, i, j):
    re = []
    for dx, dy in QUEEN_LIKE_MOVES:
        for amplifier in range(8):
            x = dx * (1 + amplifier) + i
            y = dy * (1 + amplifier) + j
            if x < 0 or x > 7 or y < 0 or y > 7:
                break
            elif state.board[x][y] != 0:
                break
            else:
                new_state = copy(state)
                new_state.board[x][y] = 10 + state.whose_move
                new_state.whose_move = 1 - state.whose_move
                new_state.board[i][j] = 0
                captures = []
                captures = WithdrawerCapture(state, i - dx, j - dy)
                for r_x, r_y in captures:
                    new_state.board[r_x][r_y] = 0
                re.append([new_state, ((i, j), (x, y))])
    return re

def WithdrawerCapture(state, opposite_x, opposite_y):
    captures = []
    if opposite_x >= 0 and opposite_x < 8 and opposite_y >= 0 and opposite_y < 8:
        if state.board[opposite_x][opposite_y] % 2 != state.whose_move:
            captures.append((opposite_x, opposite_y))
    return captures

def KingMove(state, i, j):
    re = []
    board = state.board
    whose_move = state.whose_move
    for dx, dy in NEIGHBORS:
        x = i + dx
        y = j + dy
        if x >= 0 and x <= 7 and y >= 0 and y <= 7 and (board[x][y] == 0 or board[x][y] % 2 != whose_move):
            new_state = copy(state)
            new_state.board[x][y] = 12 + whose_move
            new_state.whose_move = 1 - whose_move
            re.append([new_state, ((i, j), (x, y))])

def FreezerMove(state, i, j):
    re = []
    for dx, dy in QUEEN_LIKE_MOVES:
        for amplifier in range(8):
            x = dx * (1 + amplifier) + i
            y = dy * (1 + amplifier) + j
            if x < 0 or x > 7 or y < 0 or y > 7:
                break
            elif state.board[x][y] != 0:
                break
            else:
                new_state = copy(state)
                new_state.board[x][y] = 14 + new_state.whose_move # place pawn to new place
                new_state.board[i][j] = 0 # remove pawn from old place
                new_state.whose_move = 1 - new_state.whose_move
                re.append([new_state, ((i, j), (x, y))])
    return re

def cannotMove(state, i, j):
    # check if pawn is neighbor of opponent's freezer
    for dx, dy in NEIGHBORS:
        x = i + dx
        y = j + dy
        if x < 0 or x > 7 or y < 0 or y > 7:
            continue
        if state.board[x][y] - (1 - state.whose_move) == 14:
            return True
    return False

def prepare(player2Nickname):
    ''' Here the game master will give your agent the nickname of
    the opponent agent, in case your agent can use it in some of
    the dialog responses.  Other than that, this function can be
    used for initializing data structures, if needed.'''
    global Player2
    Player2 = player2Nickname
    zh.init_table()

def basicStaticEval(state):
    '''Use the simple method for state evaluation described in the spec.
    This is typically used in parameterized_minimax calls to verify
    that minimax and alpha-beta pruning work correctly.'''
    re = 0
    for i in range(8):
        for j in range(8):
            re = re + BASIC_SCORES[state.board[i][j]]
    return re

def staticEval(state):
    '''Compute a more thorough static evaluation of the given state.
    This is intended for normal competitive play.  How you design this
    function could have a significant impact on your player's ability
    to win games.'''
    re = 0
    global my_move
    for i in range(8):
        for j in range(8):
            ## Base score
            if state.board[i][j] % 2 == my_move:
                re = re + STATIC_SCORES[state.board[i][j] - my_move]
            else:
                re = re - STATIC_SCORES[state.board[i][j] - my_move]
            
            ## Freezer Score
            if state.board[i][j] == my_move + 14:
                for dx, dy in NEIGHBORS:
                    x = i + dx
                    y = j + dy
                    if x >= 0 and x <= 7 and y >= 0 and y <= 7 and state.board[x][y] % 2 != my_move and state.board[x][y] != 0:
                        re = re + 10

            ## King Score
            if state.board[i][j] == 12 + my_move:
                for dx, dy in NEIGHBORS:
                    x = i + dx
                    y = j + dy
                    if x >= 0 and x <= 7 and y >= 0 and y <= 7 and state.board[x][y] % 2 == my_move and state.board[x][y] != 0:
                        re = re + 10
    return re



def copy(state):
    # return a deep copy of given state
    re = BC.BC_state()
    re.board = [r[:] for r in state.board]
    re.whose_move = state.whose_move
    return re
