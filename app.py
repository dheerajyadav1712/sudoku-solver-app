from flask import Flask, request, jsonify, render_template
from itertools import product
import os

app = Flask(__name__)

# ---------------- Sudoku Logic ---------------- #

def is_valid(board, row, col, num):
    # Row & Column check
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    # 3x3 Box check
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False

    return True


def solve_sudoku(board):
    for row, col in product(range(9), repeat=2):
        if board[row][col] == 0:
            for num in range(1, 10):
                if is_valid(board, row, col, num):
                    board[row][col] = num
                    if solve_sudoku(board):
                        return True
                    board[row][col] = 0
            return False
    return True


# ---------------- Routes ---------------- #

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/solve", methods=["POST"])
def solve():
    try:
        data = request.get_json()

        if not data or "grid" not in data:
            return jsonify({"error": "Invalid input"}), 400

        # Convert string → int safely
        board = [[int(cell) if str(cell).isdigit() else 0 for cell in row] for row in data["grid"]]

        if solve_sudoku(board):
            return jsonify({"solution": board})
        else:
            return jsonify({"error": "No solution found"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------- Run (Render Compatible) ---------------- #

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))