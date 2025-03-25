import copy
import sys

class Square():
    def __init__(self, i, j, value = None):
        """Create a new square at location (i, j)"""
        self.i = i
        self.j = j
        self.initial_value = value
        if value:
            self.domain = {value}
        else:
            self.domain = {1,2,3,4,5,6,7,8,9}
        self.quadrant = self.get_quadrant(i, j)


    def __eq__(self, other):
        return (
            (self.i == other.i) and
            (self.j == other.j)
        )
    

    def __hash__(self):
        return hash((self.i, self.j))
    
        
    def __str__(self):
        return f"({self.i},{self.j})"
    
    
    def __repr__(self):
        return f"({self.i},{self.j})"
    

    def get_quadrant(self, i, j):
        """Returns a tuple with the quadrant. For example, the top left quadrant is (0,0)"""
        # Find row quadrant
        if i <= 2:
            quad_i = 0
        elif i <= 5:
            quad_i = 1
        else: 
            quad_i = 2
        
        # Find column quadrant
        if j <= 2:
            quad_j = 0
        elif j <= 5:
            quad_j = 1
        else:
            quad_j = 2

        return (quad_i, quad_j)



class Sudoku():
    
    def __init__(self, structure_file):
        """Create a new sudoku by reading a structure.txt file"""
        with open(structure_file) as f:
            contents = f.read().splitlines()
            self.height = len(contents)
            self.width = max(len(line) for line in contents)
            if not self.height == 9 or not self.width == 9:
                raise Exception("Sudoku board must be 9 x 9")
        
        # Create a set of squares
        self.squares = set()
        for i in range(9):
            for j in range(9):
                if not contents[i][j] == "#":
                    sq = Square(i, j, int(contents[i][j]))
                else:
                    sq = Square(i, j)
                self.squares.add(sq)
        
        # Create a dictionary of neighbors for each square. A neighbor is any other square in the same column, row, or quadrant. 
        self.neighbors = dict()
        for square in self.squares:
            self.neighbors[square] = self.get_neighbors(square)


    def print(self, assignment):
        grid = [["#" for i in range(9)] for j in range(9)]
        for var, value in assignment.items():
            grid[var.i][var.j] = value
        
        for i in range(9):
            for j in range(9):
                print(grid[i][j], end = "")
            print()

    
    def solve(self):
        """Return a complete assignment of squares to values"""
        # Load the initial values into the assignment
        initial_assignment = dict()
        for square in self.squares:
            if square.initial_value:
                initial_assignment[square] = square.initial_value
        
        # Simplify the sudoku using induction 
        self.ac3()

        for square in self.squares:
            if len(square.domain) == 1 and square not in initial_assignment:
                initial_assignment[square] = next(iter(square.domain))

        # Run the backtrack algorithm interweaved with ac3 to find the solution
        result = self.backtrack(initial_assignment)

        if result == None:
            print("No solution")
        else:
            self.print(result)

        return result
    
    def ac3(self, squares = None):
        queue = {}
        if squares == None:
            queue = copy.deepcopy(self.squares)
        else:
            queue = copy.deepcopy(squares)
        while not len(queue) == 0:
            x = queue.pop()
            revision = self.revise(x)
            if revision == 1000:
                return False
            if revision == 1:
                if len(x.domain) == 0:
                    return False
                for neighbor in self.neighbors[x]:
                    if len(neighbor.domain) != 1:
                        queue.add(neighbor)
        return True


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Check if crossword is complete
        t_assignment = copy.deepcopy(assignment)
        if self.assignment_complete(t_assignment):
            return t_assignment
        
        # Select a variable and loop over its domain
        square = self.select_unassigned_square(t_assignment)
        
        for val in list(square.domain):
            
            # If the assignment would still be consistent, add square = val to assignment
            test_assignment = copy.deepcopy(t_assignment)
            test_assignment[square] = val
            if self.consistent(test_assignment):
                t_assignment[square] = val

                # Check for inferences
                # Capture the original state of the square domains
                saved_domains = self.save_domains()

                # Limit the domain of any assigned squares to their assigned value
                for k, v in t_assignment.items():
                    k.domain = {v}
                
                # Run AC3, and if it finds a contradiction, remove var = val from assignment and move on to next val
                possible = self.ac3(squares = self.neighbors[square])
                if possible == False:
                    self.load_domains(saved_domains)
                    del t_assignment[square]
                    continue
                
                # Get a list of inferences
                inferences = dict()
                for x in self.squares:
                    if len(x.domain) == 1 and x not in t_assignment:
                        inferences[x] = next(iter(x.domain))
                t_assignment.update(inferences)
                
                # Recursively call backtrack
                result = self.backtrack(t_assignment)
                
                if result != None:
                    return result
                else:
                    # Restore square domains to original state
                    self.load_domains(saved_domains)
                    # Remove inferences and square = val from assignment
                    t_assignment = {k: v for k, v in t_assignment.items() if k not in inferences}
                    del t_assignment[square]  
                    
        # Return None once iterating through all possible values in the domain of the selected square
        return None
    

    def revise(self, x):
        """
        Make square 'x' node consistent with all of its neighbors and create inferences.
        i) Remove value from the domain of x if they are the only possible value of a neighbor of x
        ii) Check if the domain of x contains any values which are not in the domain of
        any other squares in the same row, column or grid
        """
        revision = 0
        # Remove assigned neighbor values from domain of x
        for neighbor in self.neighbors[x]:
            if len(neighbor.domain) == 1 and next(iter(neighbor.domain)) in x.domain:
                x.domain.remove(next(iter(neighbor.domain)))
                revision = 1

        # Check for inferences where a value is not in the domain of any other squares in the same row, column or grid 
        for val in range(1,10):
            # Check for row inferences
            open = False
            row_neighbors = []
            for neighbor in self.neighbors[x]:
                if neighbor.i == x.i:
                    row_neighbors.append(neighbor)
            for neighbor in row_neighbors:    
                if val in neighbor.domain:
                    open = True
            if not open:
                # If value is in the domain of x, infer that x must be value
                if val in x.domain and len(x.domain) != 1:
                    x.domain = {val}
                    revision = 1
                elif val in x.domain and len(x.domain) == 1:
                    revision = 0
                # Otherwise, the current assignment is impossible
                else:
                    revision = 1000
                    return revision
                
            # Check for column inferences
            open = False
            column_neighbors = []
            for neighbor in self.neighbors[x]:
                if neighbor.j == x.j:
                    column_neighbors.append(neighbor)
            for neighbor in column_neighbors:  
                if val in neighbor.domain:
                    open = True
            if not open:
                # If value is in the domain of x, infer that x must be value
                if val in x.domain and len(x.domain) != 1:
                    x.domain = {val}
                    revision = 1
                elif val in x.domain and len(x.domain) == 1:
                    revision = 0
                # Otherwise, the current assignment is impossible
                else:
                    revision = 1000
                    return revision
            
            # Check for grid inferences
            open = False
            quadrant_neighbors = []
            for neighbor in self.neighbors[x]:
                if neighbor.quadrant == x.quadrant:
                    quadrant_neighbors.append(neighbor)
            for neighbor in quadrant_neighbors:  
                if val in neighbor.domain:
                    open = True
            if not open:
                # If value is in the domain of x, infer that x must be value
                if val in x.domain and len(x.domain) != 1:
                    x.domain = {val}
                    revision = 1
                elif val in x.domain and len(x.domain) == 1:
                    revision = 0
                # Otherwise, the current assignment is impossible
                else:
                    revision = 1000
                    return revision
        return revision


    def get_neighbors(self, x):
        """
        Return a set of squares which cannot be equal to x
        This includes 
        x: Square -> set() 
        """
        neighbors = set()
        for square in self.squares:
            if x != square: 
                if x.i == square.i or x.j == square.j or x.quadrant == square.quadrant:
                    neighbors.add(square)
        return neighbors


    def select_unassigned_square(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Chooses the variable with the minimum number of remaining values
        in its domain.
        """
        selected_variable = None
        min_domain_size = sys.maxsize

        for square in self.squares:

            # Ignore squares already in assignment
            if square in assignment:
                continue

            # Check for lowest domain size
            domain_size = len(square.domain)
            if domain_size < min_domain_size:
                selected_variable = square
                min_domain_size = domain_size

        return selected_variable

    def assignment_complete(self, assignment):
        """Checks if an assignment contains values for all squares"""
        for square in self.squares:
            if square not in assignment:
                return False
        return True
    

    def consistent(self, assignment):
        """Check whether an assignment satisfies all sudoku constraints"""
        # Loop over all squares in assignment, and check that they are unique from neighbors
        for square in assignment:
            neighbors = self.neighbors[square]
            for neighbor in neighbors:
                if neighbor in assignment:
                    if assignment[square] == assignment[neighbor]:
                        return False
        return True
    

    def save_domains(self):
        """Saves domains to a dictionary"""
        saved_domains = dict()
        for square in self.squares:
            saved_domains[square] = set()
            for val in square.domain:
                saved_domains[square].add(val)
        return saved_domains
    

    def load_domains(self, saved_domains):
        """Loads domains from a dictionary"""
        for load_square in self.squares:
            load_square.domain = set()
            for load_val in saved_domains[load_square]:
                load_square.domain.add(load_val)

    
    def print_domains(self):
        """Prints current domains for each variable"""
        for i in range(9):
            for j in range(9):
                for square in self.squares:
                    if square.i == i and square.j == j:
                        print(f"Domain for square: ({square.i},{square.j}) is: ", end="")
                        for val in square.domain:
                            print(val, end="")
                        print()