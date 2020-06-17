from game import Game
from game import Board
import copy
import math
import time

INF=1000000000

def count_score(board, i, j):
    cnt = 0
    for x, y in [ (0, 1), (1, 0), (1, 1), (1, -1) ]:
        val = board.count_dir(i, j, x, y)
        if j == 3:
            #print(val)
            pass
        if val >= Game.win_count:
            #print("bruh", board.at(i, j), board.h - 1 - i, j)
            return INF
        cnt += val
    return cnt

o = True
def eval_board(board, player: int):
    score = 0
    global o
    for j in range(board.w):
        i = board.h - 1
        #print(i)
        while i >= 0 and board.at(i, j) != None:
            #print("x")
            if player == board.at(i, j):
                score += count_score(board, i, j)
            else:
                score -= count_score(board, i, j)
            if o:
                print(score)
            i -= 1
    
    o = False
    return score

def score_delta(board, i, j):
    d = 0
    for x, y in [ (0, 1), (1, 0), (1, 1), (1, -1) ]:
        val_pos = board.count_dir_single(i, j, x, y)
        val_neg = board.count_dir_single(i, j, -x, -y)

        d += val_pos*(1 + val_neg) + val_neg*(1 + val_pos) + val_neg + val_pos + 1

    return d

states = 0
def next_move(g):
    global states
    states = 0
    start = time.time()
    
    _, val = minimax(g.board, 7, g.curr, g.curr, -INF, INF)
    
    elapsed = time.time() - start
    print("Move: {}".format(val))
    print("Nodes visited: {}".format(states))
    print("Time elapsed: {}".format(elapsed))
    print("Time per node: {}".format(elapsed/states))
    
    return val


def other_player(player: int):
    return (player + 1) % 2


def minimax(board, depth, my_idx, player_idx, alpha, beta):
    global states
    states += 1
    if depth == 0:
        return (eval_board(board, my_idx), None)

    maximize_score = (player_idx == my_idx) 
    mult = 1 if maximize_score else -1

    best = -mult*INF
    move = None

    for col in range(board.w):
        if board.column_full(col):
            continue
        
        board.push(col, player_idx)
        #if board.has_at_least(board.top_idx(col), col, Game.win_count):
        #        board.pop(col)
        #        return (mult*INF, col)

        score, _ = minimax(board, depth-1, my_idx, other_player(player_idx), alpha, beta)
        board.pop(col)

        if move is None or mult*score > mult*best:
            move = col
            best = score

        #print("               "*depth, col, best, "turn:", player_idx)

        if maximize_score:
            alpha = max(alpha, score)
        else:
            beta = min(beta, score)

        if beta <= alpha:
            break

    #if best == -INF:
    #    print("u gonna lose!")

    return (best, move)
