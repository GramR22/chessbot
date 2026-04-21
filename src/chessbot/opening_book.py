import chess
import chess.polyglot
import pathlib

book_path = pathlib.Path(__file__).with_name("book.bin")

def get_polyglot_move(board: chess.Board):
    # try to get an opening-book move for the current position
    # returns a chess.Move if the the position exists in the polyglot book
    # returns nothing if the position is not found

    # crash avoidance
    if not book_path.exists():
        return None
    
    try:
        with chess.polyglot.open_reader(str(book_path)) as reader:
            entry = reader.weighted_choice(board)
            return entry.move if entry else None

    except Exception:
        return None
