from flask import Flask, render_template, request, jsonify
import chess
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from search import find_best_move
from evaluation import evaluate_curr_pos

app = Flask(__name__)
board = chess.Board()
DEPTH = 3


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/move", methods=["POST"])
def move():
    global board
    data = request.json
    uci = data.get("move", "")

    try:
        player_move = chess.Move.from_uci(uci)
        if player_move not in board.legal_moves:
            return jsonify({"error": "illegal move"}), 400
        board.push(player_move)
    except Exception:
        return jsonify({"error": "invalid move"}), 400

    if board.is_game_over():
        return jsonify({"fen": board.fen(), "game_over": True, "result": board.result()})

    # add timer wait random 4 seconds - 6 seconds

    bot_move = find_best_move(board, DEPTH, evaluate_curr_pos)
    if bot_move:
        board.push(bot_move)

    return jsonify({
        "fen": board.fen(),
        "bot_move": bot_move.uci() if bot_move else None,
        "game_over": board.is_game_over(),
        "result": board.result() if board.is_game_over() else None
    })

@app.route('/legal_moves', methods=['POST'])
def legal_moves():
    data = request.json
    square = data['square']

    moves = []
    for move in board.legal_moves:
        if chess.square_name(move.from_square) == square:
            moves.append(chess.square_name(move.to_square))

    return jsonify({ "moves": moves })

@app.route("/reset", methods=["POST"])
def reset():
    global board
    board = chess.Board()
    return jsonify({"fen": board.fen()})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
