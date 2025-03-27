// Sends puzzle to server
$(document).ready(function(){

    // 
    $('#sudoku-form').submit(function (event) {
        event.preventDefault();
        
        // Create a list of inputs
        var inputs = document.getElementsByTagName('input'),
        input_list = {};
        for (var i = 0; i < inputs.length-1; i++) {
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
        console.log(JSON.stringify(sudoku))

        // Post the data to server using AJAX and obtain solution
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

    function update_page(solution) {
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