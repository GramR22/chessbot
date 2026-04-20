import chess



def evaluate_curr_pos(board: chess.Board) -> int:
    """
        Each peice is given a value based on how powerful it is in the game. 
    """
    if board.is_game_over():
        if board.is_checkmate():
            return -10000  # the side to move is mated
        return 0  # stalemate, repetition, 50-move rule, insufficient material

    piece_value = {
        chess.PAWN: 100,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 10000
    }
    
    """     
    wt = is white peice type
    vt = peice value
    ∑ wt⋅vt
    """
    white_score = sum([len(board.pieces(chess.PAWN, chess.WHITE)) * piece_value[chess.PAWN],\
                        len(board.pieces(chess.KNIGHT, chess.WHITE)) * piece_value[chess.KNIGHT],\
                        len(board.pieces(chess.BISHOP, chess.WHITE)) * piece_value[chess.BISHOP],\
                        len(board.pieces(chess.ROOK, chess.WHITE)) * piece_value[chess.ROOK],\
                        len(board.pieces(chess.QUEEN, chess.WHITE)) * piece_value[chess.QUEEN],\
                        len(board.pieces(chess.KING, chess.WHITE)) * piece_value[chess.KING]])
    """
    bt = is black peice type
    vt = peice value
    ∑ wt⋅vt
    """
    black_score = sum([len(board.pieces(chess.PAWN, chess.BLACK)) * piece_value[chess.PAWN], \
                        len(board.pieces(chess.KNIGHT, chess.BLACK)) * piece_value[chess.KNIGHT],\
                        len(board.pieces(chess.BISHOP, chess.BLACK)) * piece_value[chess.BISHOP],\
                        len(board.pieces(chess.ROOK, chess.BLACK)) * piece_value[chess.ROOK],\
                        len(board.pieces(chess.QUEEN, chess.BLACK)) * piece_value[chess.QUEEN],\
                        len(board.pieces(chess.KING, chess.BLACK)) * piece_value[chess.KING]])
    
    
    # to give an evaluation of how the game is going we return white score-black score
    return (white_score-black_score)
