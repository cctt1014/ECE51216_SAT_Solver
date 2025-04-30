def input_parser(filename):
    """
    This function takes the file path of a DIMACS CNF file (.cnf format) and parses it,
    returning a tuple: (clauses, number of variables, number of clauses)

    DIMACS format details:
      - Comment lines: start with "c" (or "%") and are ignored.
      - Problem line: starts with "p", e.g., "p cnf 3 4" where the third and fourth tokens denote
        the number of variables and clauses.
      - Clause lines: consist of integer literals ending with 0; e.g., "1 -2 0" represents a clause.
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
    """
    Given a list of clauses and a literal that is assigned True,
    the function returns a new list of clauses updated as follows:
      - Any clause that is satisfied (i.e., contains the literal) is removed.
      - In all remaining clauses, the negation of the literal is removed.
    If a clause becomes empty, the propagation results in a conflict and returns None.
    """
    new_clauses = []
    for clause in clauses:
        if literal in clause:
            # Clause is satisfied so we skip it.
            continue
        # Remove the negated literal from the clause.
        new_clause = [l for l in clause if l != -literal]
        # An empty clause means a conflict has been detected.
        if len(new_clause) == 0:
            return None
        new_clauses.append(new_clause)
    return new_clauses


def dpll(clauses, assignment):
    """
    The DPLL algorithm recursively attempts to find a satisfying assignment.
    - clauses: list of clauses (each clause is a list of literals)
    - assignment: list of literals representing current variable assignments
    Returns a complete assignment if one exists, otherwise None.
    """
    # (1) Success check: if there is no clauses remaining, the formula is satisfied(SAT)
    if not clauses:
        return assignment

    # (2) Conflict: if any clause is empty (e.g.,[]), the current branch is unsatisfiable(UNSAT), backtrack immediately(return None)
    if any(len(clause) == 0 for clause in clauses):
        return None

    # (3) Unit propagation: repeatedly assign unit literals
    unit_clauses = [c for c in clauses if len(c) == 1]
    while unit_clauses:
        unit = unit_clauses[0][0] # the single literal
        assignment.append(unit)   # record the decision in the assignment
        clauses = propagate(clauses, unit)  
        if clauses is None: #conflict is discovered during propagation
            return None  
        unit_clauses = [c for c in clauses if len(c) == 1]

    # (4) Eliminate literals that appear with only one polarity(pure literals)
    all_literals = {lit for clause in clauses for lit in clause}
    # Identify pure literals 
    pure_literals = {lit for lit in all_literals if -lit not in all_literals}
    for lit in pure_literals:
        assignment.append(lit)
        clauses = propagate(clauses, lit)
        if clauses is None:
            return None

    # If after simplification (1) ~ (4) no clauses remain, return the assignment
    if not clauses:
        return assignment

    # 5) Branching: choose a literal (from the first clause) and try assignments True/False.
    # other advanced heuristics for choosing variables could improve performance
    chosen_literal = clauses[0][0]  # choose the first literal from the first clause<<<< there might be better heuristic like DLIS(Dynamic Largest Individual Sum):How many clauses can be satisfied if we set the literal True/False?
    
    #recursive call DPLL inside DPLL, you are calling DPLL on the smaller/ simplified formula
    # <chosen_literal = True>: Try setting the chosen literal to True
    result = dpll(propagate(clauses, chosen_literal), assignment + [chosen_literal])
    if result is not None:
        return result
    
    # [Backtracking] <chosen_literal = False>: if result = None is returned, backtrack to the other branch, try setting the chosen literal to False.
    result = dpll(propagate(clauses, -chosen_literal), assignment + [-chosen_literal])
    return result


def solve_sat(filename):
    """
    Combines the input parser and the DPLL solver.
    Reads the CNF from the DIMACS file, runs the DPLL algorithm,
    and prints the results.
    """
    clauses, num_variables, num_clauses = input_parser(filename)
    #print("Parsed Clauses:", clauses)
    print("Number of Variables:", num_variables)
    print("Number of Clauses:", num_clauses)
    
    solution = dpll(clauses, [])
    if solution is None:
        print("UNSAT")
    else:
        print("SAT:", solution)
        # Convert the list of assigned literals into a dictionary for clarity.
        assignment_dict = {}
        for literal in solution:
            assignment_dict[abs(literal)] = (literal > 0)
        #print(assignment_dict)
        #print("Assignment:", solution)
        #print("Number of Assigned Variables:", len(solution))


# Example usage:
if __name__ == "__main__":
    # Replace the path below with the actual location of your .cnf file.
    #filename = "C:\\Users\\hokie\\OneDrive - purdue.edu\\2025 Spring\\ECE 51216\\Project\\uf50-218\\uf50-05.cnf"
    filename = "C:\\Users\\hokie\\OneDrive - purdue.edu\\2025 Spring\\ECE 51216\\Project\\UUF50.218.1000\\uuf50-05.cnf"
    #filename = "C:\\Users\\hokie\\OneDrive - purdue.edu\\2025 Spring\\ECE 51216\\Project\\UF250.1065.100\\uf250-01.cnf"
    #filename = "C:\\Users\\hokie\\OneDrive - purdue.edu\\2025 Spring\\ECE 51216\\Project\\UUF250.1065.100\\uuf250-01.cnf"
    solve_sat(filename)
