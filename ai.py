from game import Game
from game import Board
import copy
import math
import time

def count_score(board, i, j):
    cnt = 0
    for x, y in [ (0, 1), (1, 0), (1, 1), (1, -1) ]:
        val = board.count_dir(i, j, x, y)
        if val >= Game.win_count:
            #print("bruh", board.at(i, j), board.h - 1 - i, j)
            return math.inf
        cnt += val
    return cnt

#o = True
def eval_board(board, player: int):
    score = 0
    #global o
    for col in range(board.w):
        row = 0
        #print(i)
        while row < board.top_idx(col):
            #print("x")
            if player == board.at(col, row):
                score += count_score(board, col, row)
            else:
                score -= count_score(board, col, row)
            #if o:
            #    print(score)
            row += 1
    
    #o = False
    return score

def calculate_score(board, player: int):
    done = [ False for _ in range(board.w*board.h) ]

    for col in range(board.w):
        for i in range(board.top_idx(col)):
            pass

def score_delta(board, i, j):
    d = 0
    for x, y in [ (0, 1), (1, 0), (1, 1), (1, -1) ]:
        val_pos = board.count_dir_single(i, j, x, y)
        val_neg = board.count_dir_single(i, j, -x, -y)

        d += val_pos*(1 + val_neg) + val_neg*(1 + val_pos) + val_neg + val_pos + 1

    return d

states = 0
DEPTH = 8
NODE_ORDER = [3, 2, 4, 1, 5, 0, 6]
def next_move(g):
    global states
    states = 0
    
    start = time.time()
    #_, val = minimax(g.board, DEPTH, g.curr, g.curr, -math.inf, math.inf)
    #print()
    #print()
    #print()
    score, val2 = negamax(g.board, DEPTH, g.curr, g.curr, -math.inf, math.inf)
    elapsed = time.time() - start

    #if val != val2:
    #    print("WROOOOOOOOOOOOOOOOOOOOOONG!!!!!!!!!!!")

    #print("Move: {} X {}".format(val, val2))
    print("Score: {}".format(score))
    print("Nodes visited: {}".format(states))
    print("Time elapsed: {}".format(elapsed))
    #print("Time per node: {}".format(elapsed/states))
    
    return val2


def other_player(player: int):
    return (player + 1) % 2


def negamax(board, depth, main_player, curr_player, alpha, beta):
    # ew a global
    global states
    states += 1

    if depth == 0:
        return eval_board(board, curr_player), None

    best = -math.inf
    move = None

    for col in NODE_ORDER:
        if board.column_full(col):
            continue
        
        board.push(col, curr_player)
        if board.has_at_least(col, board.top_idx(col) - 1, Game.win_count):
            board.pop(col)
            return math.inf, col

        score, _ = negamax(board, depth-1, main_player, other_player(curr_player), -beta, -alpha)
        board.pop(col)

        if move is None or -score > best:
            move = col
            best = -score

        #print("               "*(DEPTH - depth), col, best, "turn:", curr_player)
        
        alpha = max(alpha, best)
        if alpha >= beta:
            break
    
    return best, move



def minimax(board, depth, my_idx, player_idx, alpha, beta):
    global states
    states += 1
    if depth == 0:
        return (eval_board(board, my_idx), None)

    maximize_score = (player_idx == my_idx) 
    mult = 1 if maximize_score else -1

    best = -mult*math.inf
    move = None

    for col in range(board.w):
        if board.column_full(col):
            continue
        
        board.push(col, player_idx)
        if board.has_at_least(col, board.top_idx(col) - 1, Game.win_count):
            board.pop(col)
            return (mult*math.inf, col)

        score, _ = minimax(board, depth-1, my_idx, other_player(player_idx), alpha, beta)
        board.pop(col)

        if move is None or mult*score > mult*best:
            move = col
            best = score

        #print("               "*(DEPTH - depth), col, best, "turn:", player_idx)

        if maximize_score:
            alpha = max(alpha, score)
        else:
            beta = min(beta, score)

        if beta <= alpha:
            break

    #if best == -INF:
    #    print("u gonna lose!")

    return (best, move)
