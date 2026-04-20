from flask import Flask, render_template, request, jsonify
import chess
import sys
import os
import time
import random

sys.path.insert(0, os.path.dirname(__file__))
from search import find_best_move
from evaluation import evaluate_curr_pos

app = Flask(__name__)
board = chess.Board()
DEPTH = 3


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/player_move", methods=["POST"])
def player_move():
    global board

    # Guard against the client calling this out of turn
    if board.turn != chess.WHITE:  # assuming the human plays White
        return jsonify({"error": "not your turn"}), 400

    uci = (request.json or {}).get("move", "")
    try:
        move = chess.Move.from_uci(uci)
        if move not in board.legal_moves:
            return jsonify({"error": "illegal move"}), 400
        board.push(move)
    except Exception:
        return jsonify({"error": "invalid move"}), 400

    return jsonify({
        "fen": board.fen(),
        "game_over": board.is_game_over(),
        "result": board.result() if board.is_game_over() else None,
    })
# Make it so when bot moves have a green boarder around piece that moved

@app.route("/bot_move", methods=["POST"])
def bot_move():
    global board

    if board.is_game_over():
        return jsonify({"error": "game over"}), 400
    if board.turn == chess.WHITE:
        return jsonify({"error": "not bot's turn"}), 400

    time.sleep(random.uniform(2, 3))
    move = find_best_move(board, DEPTH, evaluate_curr_pos)
    if move is None:
        return jsonify({"error": "no legal move"}), 400

    board.push(move)

    return jsonify({
        "fen": board.fen(),
        "bot_move": move.uci(),
        "game_over": board.is_game_over(),
        "result": board.result() if board.is_game_over() else None,
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
