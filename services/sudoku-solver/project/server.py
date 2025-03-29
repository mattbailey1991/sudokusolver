from flask import Flask, jsonify, render_template, redirect, request, Response
import pymongo
from project.sudoku import *

app = Flask(__name__)

try:
    mongo = pymongo.MongoClient(host="mongodb", 
                                port=27017, 
                                serverSelectionTimeoutMS = 1000,
                                username = "admin",
                                password = "password")
    print("Successfully connected to MongoDB")

except:
    raise RuntimeError("Cannot connect to MongoDB. If using local host, try: docker run mongo")

db = mongo.saved_grids

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
        grid_data = request.get_json()
        print(grid_data)
        sudoku = Sudoku(grid_data, file_type="dict")
        result = sudoku.solve()
        return jsonify({"solution": result})


@app.route("/saved-puzzles")
def saved_puzzles():
    """Provides a list of saved puzzles"""
    return render_template('saved-puzzles.html')


@app.route("/save-puzzle", methods = ["POST"])
def save_puzzle():
    """Saves a puzzle to sudokus collection"""
    try:
        req_data = request.get_json()
        name = req_data["name"]
        grid_data = req_data["grid_data"]
        if db.sudokus.find_one({"name": name}):
            return jsonify({"message": "Name already in use"})
        else:
            dbResponse = db.sudokus.insert_one({"name": name, "grid_data": grid_data})
            print(dbResponse.inserted_id)
            return jsonify({"message": "Sudoku saved"})
    
    except:
        raise RuntimeError("Could not save sudoku data to data")