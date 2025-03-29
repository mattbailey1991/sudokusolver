// Sends puzzle to server
$(document).ready(function(){

    // sudoku-form submission
    // Sends the grid to the server using AJAX, gets a solution using AC3 and backtrack, and updates page with solution 
    $('#sudoku-form').submit(function (event) {
        event.preventDefault();
        var sudoku = grid_data()
        console.log(JSON.stringify(sudoku))

        // Post the data to /sudoku route using AJAX to obtain solution
        $.ajax({
            type: 'POST',
            url: "",
            contentType: 'application/json;charset=UTF-8',
            dataType: 'json',
            data: JSON.stringify(sudoku),
            success: function(response) {
                solution = JSON.parse(response["solution"]);
                update_page(solution);
            }
        });
    });


    // save-form submission
    // Sends the grid to the server and saves to a mongodb database
    $('#save-form').submit(function (event) {
        event.preventDefault();

        // Get sudoku grid data
        var sudoku = grid_data()
        console.log(JSON.stringify(sudoku))

        // Get save name
        var name = document.getElementById('sudoku-name').value

        // Posts the grid data to save-form route using AJAX
        $.ajax({
            type: "POST",
            url: "/save-puzzle",
            contentType: 'application/json;charset=UTF-8',
            dataType: 'json',
            data: JSON.stringify({"name":name, "grid_data":sudoku}),
            success: function(response) {
                var message = response["message"];
                $('#message-area').html('<div class="container-fluid px-0"> <div class="alert alert-info" role="alert">' + message + '</div> </div>');
            }
        });
    });


    function grid_data() {
        // Create a list of inputs
        var inputs = document.getElementsByTagName('input'),
        input_list = {};
        for (var i = 0; i < inputs.length-3; i++) {
            input_list[i] = inputs[i].value;
        }
        
        // Parse input list such that number in row, column is sudoku[row][column]
        let sudoku = {};

        for (let i = 0; i < 9; i++) {
            sudoku[i] = {};
        }
        
        for (const [k, v] of Object.entries(input_list)) {
            let row = Math.floor(k / 9);
            let column = k % 9;
            sudoku[row][column] = parseInt(v);
        }

        return sudoku;
    }

    // Updates a page with a grid
    function update_page(grid) {
        if (solution == 9999) {
            console.log("No solution")
        }
        else {
            console.log(JSON.stringify(solution))
            var inputs = document.getElementsByTagName('input');
            for (let i = 0; i < 9; i++) {
                for (let j = 0; j < 9; j++) {
                    inputs[i*9 + j].value = solution[i][j]
                } 
            }
        }
    }
})