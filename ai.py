from game import Game
from game import Board
import copy
import math


def count_score(board, i, j):
    cnt = 0
    for x, y in [ (0, 1), (1, 0), (1, 1), (1, -1) ]:
        val = board.count_dir(i, j, x, y)
        if val >= Game.win_count:
            #print("bruh", board.at(i, j), i, j)
            return math.inf
        cnt += val
    return cnt


def eval_board(board, player: int):
    score = 0

    for j in range(board.w):
        i = board.h - 1
        while i >= 0 and board.at(i, j) != None:
            if player == board.at(i, j):
                score += count_score(board, i, j)
            else:
                score -= count_score(board, i, j)
            i -= 1

    return score


def next_move(g):
    val = minimax(g.board, 5, g.curr, g.curr)[1]
    #print("\n")
    return val


def other_player(player: int):
    return (player + 1) % 2


def minimax(board, depth, my_idx: int, player_idx: int):
    if depth == 0:
        return (eval_board(board, my_idx), None)

    if player_idx == my_idx:
        best = -math.inf
        move = None
        for col in range(board.w):
            pushed = False
            if not board.column_full(col):
                board.push(col, player_idx)
                pushed = True
                if board.has_at_least(board.top_idx(col), col, Game.win_count):
                    board.pop(col)
                    return (math.inf, col)
            score, _ = minimax(board, depth - 1, my_idx, other_player(player_idx))
            if pushed:
                board.pop(col)
            #print("max:", score)
            #print("-----------------------")
            if move is None or score > best:
                move = col
                best = score
        return (best, move)
    else:
        best = math.inf
        move = None
        for col in range(board.w):
            pushed = False
            if not board.column_full(col):
                board.push(col, player_idx)
                pushed = True
                if board.has_at_least(board.top_idx(col), col, Game.win_count):
                    board.pop(col)
                    return (-math.inf, col)
            score, _ = minimax(board, depth - 1, my_idx, other_player(player_idx))
            if pushed:
                board.pop(col)
            if move is None or score < best:
                move = col
                best = score
           # print("min:", score, "best:", best)
        return (best, move)


def  simle():
    move = None
    best = None
    mark = g.current_mark()
    for j in range(Game.W):
        i = Game.H - g.heights[j] - 1
        if i < 0:
            continue 
        g.board[i][j] = mark
        val = eval_board(g, g.curr)
        if best is None or val > best:
            best = val
            move = j
        g.board[i][j] = Game.EMPTY

    print(move)
    return move
