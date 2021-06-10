'''daw1230_TTS_agent.py
A TTS agent that plays Toro-Tile Straight.

If you need to import additional custom modules, use
a similar naming convention... e.g.,
YourUWNetID_TTS_custom_static.py


'''

from TTS_State import TTS_State
import time
from random import choice

class MY_TTS_State(TTS_State):
  def static_eval(self):
    if USE_CUSTOM_STATIC_EVAL_FUNCTION:
      return self.custom_static_eval()
    else:
      return self.basic_static_eval()

  def basic_static_eval(self):
    TWF = 0
    TBF = 0
    N = len(self.board) # height of the board
    M = len(self.board[0]) # width of the board
    for i in range(N):
      for j in range(M):
        if self.board[i][j] == 'W':
          if self.board[i][(j+1+M) % M]==' ': TWF+=1
          if self.board[(i+1+N) % N][(j+1+M) % M]==' ': TWF+=1
          if self.board[(i-1+N) % N][(j+1+M) % M]==' ': TWF+=1
          if self.board[i][(j-1+M) % M]==' ': TWF+=1
          if self.board[(i+1+N) % N][(j-1+M) % M]==' ': TWF+=1
          if self.board[(i-1+N) % N][(j-1+M) % M]==' ': TWF+=1
          if self.board[(i+1+N) % N][j]==' ': TWF+=1
          if self.board[(i-1+N) % N][j]==' ': TWF+=1

        if self.board[i][j] == 'B':
          if self.board[i][(j+1+M) % M]==' ': TBF+=1
          if self.board[(i+1+N) % N][(j+1+M) % M]==' ': TBF+=1
          if self.board[(i-1+N) % N][(j+1+M) % M]==' ': TBF+=1
          if self.board[i][(j-1+M) % M]==' ': TBF+=1
          if self.board[(i+1+N) % N][(j-1+M) % M]==' ': TBF+=1
          if self.board[(i-1+N) % N][(j-1+M) % M]==' ': TBF+=1
          if self.board[(i+1+N) % N][j]==' ': TBF+=1
          if self.board[(i-1+N) % N][j]==' ': TBF+=1
    return TWF-TBF   
    

  def custom_static_eval(self):
    global COUNTS
    COUNTS = self.count_s()
    if COUNTS['B'][K] > 0:
        return -1000000000
    if COUNTS['W'][K] > 0:
        return 1000000000
    B = sum([COUNTS['B'][i] * 10 ** i for i in range(K)])
    W = sum([COUNTS['W'][i] * 10 ** i for i in range(K)])
    return W - B

  def count_s(self):
    COUNTS = {'W': [0 for n in range(K + 1)],
              'B': [0 for n in range(K + 1)]}
    
    board = self.board
    N = len(board) # height of the board
    M = len(board[0]) # width of the board
    for i in range(N):
      for j in range(M):
        # For forbidden position, no connecting lines
        if board[i][j] == '-':
          continue           
        East = [board[i][(j + n) % M] for n in range(K)]
        South = [board[(i - n) % N][j] for n in range(K)]
        SE = [board[(i + n) % N][(j + n) % M] for n in range(K)]
        NE = [board[(i - n) % N][(j + n) % M] for n in range(K)]
        # East
        if '-' not in East:
          if 'W' in East and 'B' not in East:
            COUNTS['W'][East.count('W')] += 1
          elif 'B' in East and 'W' not in East:
            COUNTS['B'][East.count('B')] += 1
        # South
        if '-' not in South:
          if 'W' in South and 'B' not in South:
            COUNTS['W'][South.count('W')] += 1
          elif 'B' in South and 'W' not in South:
            COUNTS['B'][South.count('B')] += 1
        # Southeast
        if '-' not in SE:
          if 'W' in SE and 'B' not in SE:
            COUNTS['W'][SE.count('W')] += 1
          elif 'B' in SE and 'W' not in SE:
            COUNTS['B'][SE.count('B')] += 1
        # Northeast
        if '-' not in NE:
          if 'W' in NE and 'B' not in NE:
            COUNTS['W'][NE.count('W')] += 1
          elif 'B' in NE and 'W' not in NE:
            COUNTS['B'][NE.count('B')] += 1
    return COUNTS

  def move(self, coord):
    s_new = self.copy()
    i,j = coord
    s_new.board[i][j] = s_new.whose_turn
    if self.whose_turn == 'W':
      s_new.whose_turn = 'B'
    else:
      s_new.whose_turn = 'W'
    s_new.__class__ = MY_TTS_State
    return s_new

# The following is a skeleton for the function called parameterized_minimax,
# which should be a top-level function in each agent file.
# A tester or an autograder may do something like
# import ABC_TTS_agent as player, call get_ready(),
# and then it will be able to call tryout using something like this:
# results = player.parameterized_minimax(**kwargs)
USE_CUSTOM_STATIC_EVAL_FUNCTION = True
n_states_expanded = 0
n_static_evals = 0
n_cutoffs = 0
K = 3
best_move = []
MYSIDE = None
Player2 = None
I=J=H=PP=QQ = 0

def parameterized_minimax(
       current_state=None,
       max_ply=2,
       alpha_beta=False, 
       use_custom_static_eval_function=False):
  
  # All students, add code to replace these default
  # values with correct values from your agent (either here or below).
  if current_state == None:
    raise ValueError("No State entered")

  global USE_CUSTOM_STATIC_EVAL_FUNCTION, n_states_expanded, n_static_evals, \
         n_cutoffs, max_depth_reached
  
  USE_CUSTOM_STATIC_EVAL_FUNCTION = use_custom_static_eval_function
  n_states_expanded = 0
  n_static_evals = 0
  n_cutoffs = 0
  alpha = -100000000000
  beta = 100000000000

  current_state.__class__ = MY_TTS_State
  start = time.time()
  time_limit = 10000 #no time limit

  """By using different variables, the function can achieve minimax,
  minimax with alpha-beta pruning"""
  current_state_static_val = minimax(current_state, max_ply, alpha_beta, start, time_limit, alpha, beta)

  DATA = {}
  DATA['CURRENT_STATE_STATIC_VAL'] = current_state_static_val
  DATA['N_STATES_EXPANDED'] = n_states_expanded
  DATA['N_STATIC_EVALS'] = n_static_evals
  DATA['N_CUTOFFS'] = n_cutoffs

  # Actually return all results...
  return(DATA)

def minimax(current_state, plyLeft, alpha_beta, start, time_limit, alpha, beta):
  global n_states_expanded, n_static_evals, n_cutoffs,\
         best_move
  if plyLeft == 0:
      val = current_state.static_eval()
      n_static_evals += 1
      return val

  if current_state.whose_turn == 'W':
    provisional = -100000000000
  else:
    provisional = 100000000000

  successors = _find_next_vacancy(current_state)
  n_states_expanded += 1
  best_move = successors[0]

  for coord in successors:
    if time.time() - start < time_limit:
      new_state = current_state.move(coord)
      newVal = minimax(new_state, plyLeft-1, alpha_beta, start, time_limit, alpha, beta)
      if current_state.whose_turn == 'W' and newVal > provisional:
        provisional = newVal
        best_move = coord
        alpha = max(provisional, alpha)
        if alpha_beta and alpha>=beta:
          n_cutoffs += 1
          break
      elif current_state.whose_turn == 'B' and newVal < provisional:
        provisional = newVal
        best_move = coord
        beta = min(provisional, beta)
        if alpha_beta and alpha>=beta:
          n_cutoffs += 1
          break
  return provisional

def take_turn(current_state, last_utterance, time_limit):

    # Compute the new state for a move.
    # Start by copying the current state.
    start = time.time()
    current_state.__class__ = MY_TTS_State
    new_state = MY_TTS_State(current_state.board)

    successors = _find_next_vacancy(current_state)
    max_depth = 1
    alpha = -100000000000
    beta = 100000000000
    
    while max_depth <= len(successors) and time.time()-start < time_limit:
      minimax(current_state, max_depth, True, start, time_limit, alpha, beta)
      max_depth += 1
      if time.time() - start > time_limit:
        break
    new_state = current_state.move(best_move)
    
    # Make up a new remark
    new_utterance = utterance(new_state)

    return [[best_move, new_state], new_utterance]

def utterance(current_state):
    val = current_state.static_eval()
    global I,J,H,PP,QQ
    if val == 0:
      utter = ['This is a close game.','No one is winning.',\
                                 'No one is losing.','It is such a close game.',\
                                 'The odds of winning is the same.']
      utteran = utter[I%4]
      I += 1    
    if val > 0:
      if MYSIDE == 'W':
        utter = ['I am going to win.',\
                 "I have a clear advantage based on my evaluation.",\
                'I am winning.', 'Enjoying the game.',\
                'No conclusion but I have a greater chance to win.',\
                'Love the game!', 'Yeah winning.','Winning.','Wonderful game.',\
                 'What a good day.','My evaluation function is strong.',\
                 'Plause for my evaluation function.']
        utteran = utter[J%11]
        J += 1
      else:
        utter = ["You have a clear advantage based on my evaluation. Well Done ",\
                        'You are winning.', 'I am kind of losing.',"Well Done, "+ Player2,\
                        'Good job.', 'Nice move.', 'No, I am losing.']
        utteran = utter[H%6]
        H += 1
      
    if val < 0:
      if MYSIDE == 'B':
        utter = ['I am going to win.',\
                 "I have a clear advantage based on my evaluation.",\
                'I am winning.', 'Enjoying the game.',\
                'No conclusion but I have a greater chance to win.',\
                'Love the game!', 'Yeah winning.','Winning.','Wonderful game.',\
                 'What a good day.','My evaluation function is strong.',\
                 'Plause for my evaluation function.']
        utteran = utter[PP%11]
        PP += 1
      else:
        utter = ["You have a clear advantage based on my evaluation. Well Done ",\
                        'You are winning.', 'I am kind of losing.',"Well Done, "+ Player2,\
                        'Good job.', 'Nice move.', 'No, I am losing.']
        utteran = utter[QQ%6]
        QQ += 1    
    return utteran  
    
  

def _find_next_vacancy(self):
    """changed to find all the vacant postions on board"""
    successors = []
    for i in range(len(self.board)):
      for j in range(len(self.board[0])):
        if self.board[i][j]==' ': successors.append((i,j))
    return successors

def moniker():
    return "Donna" # Return your agent's short nickname here.

def who_am_i():
    return """My name is Donna, created by Dan Wang.
I try hard to be a nice person, but it's hard."""

def get_ready(initial_state, k, who_i_play, player2Nickname):
    global MYSIDE, Player2
    MYSIDE = who_i_play
    Player2 = player2Nickname
    return "OK"
