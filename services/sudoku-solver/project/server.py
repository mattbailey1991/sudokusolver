from flask import Flask, jsonify, render_template, redirect, request, Response
from project.sudoku import *

app = Flask(__name__)

@app.route("/")
def redirect_to_sudoku():
    return redirect("/sudoku")


@app.route("/sudoku", methods=["GET","POST"])
def sudoku():
    """Provides an interface for inputting a sudoku puzzle and getting solution"""
    # Sudoku input page
    if request.method == "GET":
        return render_template('sudoku.html')
    
    # Return solved sudoku
    if request.method == "POST":
        data = request.get_json()
        print(data)
        sudoku = Sudoku(data, file_type="dict")
        result = sudoku.solve()
        return jsonify({"solution": result})

@app.route("/saved-puzzles")
def saved_puzzles():
    """Provides a list of saved puzzles"""
    return render_template('saved-puzzles.html')