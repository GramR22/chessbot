import sys
import chess
from search import find_best_move
from evaluation import evaluate_curr_pos


# how many moves ahead the bot looks by default
# higher = smarter but slower
DEFAULT_DEPTH = 4


def uci_loop():
    """
    UCI (Universal Chess Interface) is a standard way for chess engines to
    talk to GUIs. the GUI sends us text commands over stdin and we respond over stdout. We just loop
    forever waiting for commands until the GUI tells us to quit.
    """
    board = chess.Board()

    while True:
        line = sys.stdin.readline().strip()

        if not line:
            continue

        # GUI is introducing itself and asking if we speak UCI
        # we say yes by sending back our name and "uciok"
        if line == "uci":
            print("uciok")
            sys.stdout.flush()

        # GUI is asking "you ready?" before sending us any real work
        # if we had something slow to load (opening book, neural net, etc.)
        # we'd do it here before saying readyok
        elif line == "isready":
            print("readyok")
            sys.stdout.flush()

        # new game started, wipe the board back to the start
        elif line == "ucinewgame":
            board = chess.Board()

        # GUI is telling us what the board looks like right now
        # it either sends "startpos" (fresh game) or a FEN string (mid-game)
        # then optionally a list of moves that have been played since
        # FEN is just a compact text snapshot of a board position
        # moves are in UCI format: just source square + target square e2e4
        elif line.startswith("position"):
            parts = line.split()

            if parts[1] == "startpos":
                board = chess.Board()
                if "moves" in parts:
                    for uci in parts[parts.index("moves") + 1:]:
                        board.push_uci(uci)

            elif parts[1] == "fen":
                fen_end = parts.index("moves") if "moves" in parts else len(parts)
                board = chess.Board(" ".join(parts[2:fen_end]))
                if "moves" in parts:
                    for uci in parts[parts.index("moves") + 1:]:
                        board.push_uci(uci)

        # GUI is saying "ok your turn, go think"
        # we run our negamax search and send back the best move we found
        # if the GUI passes "depth N" we use that, otherwise fall back to DEFAULT_DEPTH
        # "0000" is the UCI way of saying we have no move  stalemate)
        elif line.startswith("go"):
            parts = line.split()
            depth = int(parts[parts.index("depth") + 1]) if "depth" in parts else DEFAULT_DEPTH

            move = find_best_move(board, depth, evaluate_curr_pos)

            print(f"bestmove {move.uci() if move else '0000'}")
            sys.stdout.flush()

        # GUI is shutting down, we clean up and exit
        elif line == "quit":
            break


if __name__ == "__main__":
    uci_loop()
