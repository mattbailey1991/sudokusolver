from flask import Flask, jsonify, render_template, redirect

app = Flask(__name__)

@app.route("/")
def redirect_to_sudoku():
    return redirect("/sudoku")


@app.route("/sudoku")
def sudoku():
    """Provides an interface for inputting a sudoku puzzle and getting solution"""
    return render_template('sudoku.html')


@app.route("/saved-puzzles")
def saved_puzzles():
    """Provides a list of saved puzzles"""
    return render_template('saved-puzzles.html')