import chess



def evaluate_curr_pos(board: chess.Board) -> int:
    """
        Each peice is given a value based on how powerful it is in the game. 
        Honestly not a chess pro so AI gave these values to me
        WE NEED TO CHECK LATER
        """
    piece_value = {
        chess.PAWN: 100,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 0
    }
    