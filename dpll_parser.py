import time

def input_parser(filename):
    """
    This function takes the file path of a DIMACS CNF file (.cnf format) and parses it,
    returning a tuple: (clauses, number of variables, number of clauses)

    DIMACS format details:
      - Comment lines: start with "c" (or "%") and are ignored.
      - Problem line: starts with "p", e.g., "p cnf 3 4" where the third and fourth tokens denote
        the number of variables and clauses.
      - Clause lines: consist of integer literals ending with 0; e.g., "1 -2 0" represents a clause
    """
    num_variables = 0
    num_clauses = 0
    clauses = []
    current_clause = []  # temporary list for accumulating literals for the current clause

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('c') or line.startswith('%'):
                continue
            if line.startswith('p'):
                parts = line.split()
                if len(parts) >= 4:
                    try:
                        num_variables = int(parts[2])
                        num_clauses = int(parts[3])
                    except ValueError:
                        raise ValueError("Invalid number format in problem line")
                else:
                    raise ValueError("Problem line is missing required information")
                continue
            tokens = line.split()
            for token in tokens:
                try:
                    literal = int(token)
                except ValueError:
                    raise ValueError(f"Invalid literal encountered: {token}")
                if literal == 0:
                    if current_clause:
                        clauses.append(current_clause)
                        current_clause = []
                else:
                    current_clause.append(literal)
    if current_clause:
        clauses.append(current_clause)
    return clauses, num_variables, num_clauses


def propagate(clauses, literal):
    """given a list of clauses and a literal that is assigned True, the function returns a new list of clauses updated as follows:
      1.Any clause that is satisfied (contains the literal) is removed
      2.In all remaining clauses, the negation of the literal is removed
    If a clause becomes empty, the propagation results in a conflict and returns None
   ex) propagate([[1,2,-3],[-1,4]], 1)  ==  [[4]]
    """
    new_clauses = []
    for clause in clauses:  #clauses=[[1, -2], [-1, 3], [2, 4]], literal=1 will return: new_clauses=[[3],[2, 4]]
        #check if the clause is satisfied by the literal, if so we skip it
        if literal in clause:
            #clause is satisfied so we skip it, not adding it to new_clauses
            continue
        #remove the negated literal from the clause
        new_clause = [l for l in clause if l != -literal] #includes if it is not equal to -literal, remove the -literal from the clause
        # len==0, empty clause means there is a contradict, no way to satisfy this clause, so return None
        # which exits the function and return None to indicate confilict
        if len(new_clause) == 0:       #empty clause means a conflict has been detected. refer to example of propagate([[1,-2],[2],[3,-1]], [2]) and then on literal [1]

            return None
        new_clauses.append(new_clause)
    return new_clauses 






def dpll(clauses, assignment):
    """    dpll recursively attempts(dpll inside dpll) to find a satisfying assignment.
    - clauses: list of clauses (each clause is a list of literals)
    - assignment: list of literals representing current variable assignments
    Returns a complete assignment if one exists, otherwise None.
    
    """
    # Base case: if no clauses remain, the formula is satisfied
    if not clauses:
        return assignment

    # Conflict: if any clause is empty, the current branch is unsatisfiable
    if any(len(clause) == 0 for clause in clauses):
        return None

    # Boolean constraint propagation (BCP): applying unit clause rule, repeatedly assign unit literals
    unit_clauses = [c for c in clauses if len(c) == 1]
    while unit_clauses:
        unit = unit_clauses[0][0]
        assignment.append(unit)
        clauses = propagate(clauses, unit)
        if clauses is None:
            return None  # Conflict detected during propagation.
        unit_clauses = [c for c in clauses if len(c) == 1]

    # Pure literal elimination:
    # Find all unique literals in the formula.
    all_literals = {lit for clause in clauses for lit in clause}
    # Identify pure literals (appear with only one polarity).
    pure_literals = {lit for lit in all_literals if -lit not in all_literals}
    for lit in pure_literals:
        assignment.append(lit)
        clauses = propagate(clauses, lit)
        if clauses is None:
            return None

    #if after simplification no clauses remain, return the assignment
    if not clauses:
        return assignment

    #Branching (may be add algorithms to Backtrack??): choose a literal and try assignments
    chosen_literal = clauses[0][0]

    # try to set the chosen literal to True
    result = dpll(propagate(clauses, chosen_literal), assignment + [chosen_literal])
    if result is not None:
        return result

    # Otherwise, try setting the chosen literal to False
    result = dpll(propagate(clauses, -chosen_literal), assignment + [-chosen_literal])
    return result


def solve_sat(filename):
    """
    as a wrapper function, combines the input parser and the DPLL solver, reads the CNF from the DIMACS file, runs the DPLL algorithm,
    print the results along with the runtime of the simulation
    """
    start_time = time.time()  # Start the timer before processing
    
    clauses, num_variables, num_clauses = input_parser(filename)
    #print("Parsed Clauses:", clauses) # uncomment this to print out parsed clauses
    print("Number of Variables:", num_variables)
    print("Number of Clauses:", num_clauses)
    
    solution = dpll(clauses, [])
    if solution is None:
        print("UNSAT")
    else:
        print("SAT:", solution)
        # Optionally, convert the list of assigned literals into a dictionary
        assignment_dict = {}
        for literal in solution:
            assignment_dict[abs(literal)] = (literal > 0)
        # print("Assignment:", assignment_dict)
    
    end_time = time.time()  # End the timer after processing
    print("Run time: {:.6f} seconds".format(end_time - start_time))


# Example usage:
if __name__ == "__main__":
    # Replace the path below with the actual location of your .cnf file
    # filename = "C:\\path\\to\\your\\file.cnf"
    #filename = "C:\\Users\\hokie\\OneDrive - purdue.edu\\2025 Spring\\ECE 51216\\Project\\uf50-218\\uf50-01.cnf"
    #filename = "C:\\Users\\hokie\\OneDrive - purdue.edu\\2025 Spring\\ECE 51216\\Project\\UUF50.218.1000\\uuf50-01.cnf"
    #filename = "C:\\Users\\hokie\\OneDrive - purdue.edu\\2025 Spring\\ECE 51216\\Project\\UF250.1065.100\\uf250-01.cnf"
    filename = "C:\\Users\\hokie\\OneDrive - purdue.edu\\2025 Spring\\ECE 51216\\Project\\UUF250.1065.100\\uuf250-01.cnf"    
    solve_sat(filename)
