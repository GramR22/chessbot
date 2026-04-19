from evaluation import evaluate_curr_pos as evaluator
import chess
"""
board -  is our chess board
depth -  is how many moves in the future do we check
alpha -  is the lower bound of the score we can get
beta  -  is the upper of the score we can get
evalulator is our evaluation.py

In this file it will recursivly using alpha beta pruning
"""




def negamax(board, depth, alpha, beta, evaluator):
    if depth == 0 or board.is_game_over():  
        score = evaluator(board)
        return score if board.turn == chess.WHITE else -score
    
    #init something
    best = -float("inf")  

    for move in board.legal_moves:
        board.push(move)
        score = -negamax(board, depth - 1, -beta, -alpha, evaluator)
    # is this move better than what we have if yes update
        if score > best:
            best = score
    
    # have we passed our lower bound if yes update because we are sure we can get atleast this much
        if best > alpha:
            alpha = best
    
    # if our best is greater than beta we exit because our opponent has beeten us beyond this
        if best >= beta:
            break
        
    # this is our best move
    return best


def find_best_move(board, depth, evaluator, alpha = -float("inf"), beta = float("inf")):
    
    #init our variables
    best_move = None
    best_score = -float("inf")

    # once again we check the moves and scores to see if we have the best score
    for move in board.legal_moves:
        
        # same as before
        board.push(move)
        score = -negamax(board, depth-1, -beta, -alpha, evaluator)
        board.pop()
        
        # get best move based on score
        if score > best_score:
            best_score = score
            best_move = move
            alpha = max(alpha,score)
    return best_move


