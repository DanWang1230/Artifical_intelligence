'''DD_BC_module_zobrist_hashing.py
by Yu Fan (fany23) and Dan Wang (daw1230)

Zobrist hashing for Baroque Chess.
'''

import random

PIECES = {2:'p',3:'P',4:'c',5:'C',6:'l',7:'L',10:'w',11:'W',12:'k',13:'K',14:'f',15:'F'}
# We are not considering imitator (8:'i',9:'I') in DD_BC_Player.py
TABLE = []
zobrist_table = {}

# Assign a random number to initial board
def init_table():
    global TABLE
    for row in range(8):
        rowhash = []
        for column in range(8):
            cell = {}
            for piece in PIECES:
                cell[piece] = random.getrandbits(64)
            rowhash.append(cell)
        TABLE.append(rowhash)

# Return the hash value for a given state
def hash_state(state):
    global TABLE
    h = 0
    board = state.board
    for row in range(8):
        for column in range(8):
            piece = board[row][column]
            if piece != 0:
                h ^= TABLE[row][column][piece]
    return h
