import logging
from input_parser import input_parser
from utils import validate_sat_solution

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
    logging.debug(f"Current assignment: {assignment}")
    logging.debug(f"Current clauses: {clauses}")
    
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
    logging.debug(f"Trying literal {chosen_literal} as True")
    result = dpll(propagate(clauses, chosen_literal), assignment + [chosen_literal])
    if result is not None:
        return result
    
    # [Backtracking] <chosen_literal = False>: if result = None is returned, backtrack to the other branch, try setting the chosen literal to False.
    logging.debug(f"Backtracking on literal {chosen_literal} as False")
    result = dpll(propagate(clauses, -chosen_literal), assignment + [-chosen_literal])
    return result


def solve_sat_dpll(filename):
    """
    Combines the input parser and the DPLL solver.
    Reads the CNF from the DIMACS file, runs the DPLL algorithm,
    and prints the results.
    """
    clauses, num_variables, num_clauses = input_parser(filename)
    #print("Parsed Clauses:", clauses)
    logging.info(f"Number of Variables: {num_variables}")
    logging.info(f"Number of Clauses: {num_clauses}")
    
    solution = dpll(clauses, [])
    if solution is None:
        print("RESULT:UNSAT")
        return 0
    else:
        print("RESULT:SAT")
        
        # Convert the list of assigned literals into a dictionary for clarity.
        print("ASSIGNMENT:", end="")
        for literal in solution:
            val = 1 if literal > 0 else 0
            print(f"{abs(literal)}={val}", end=" ")
        print("")
        return 1
    
        # Uncomment the following lines to validate the solution
        # solution_is_valid = validate_sat_solution(clauses, solution)
        # if solution_is_valid:
        #     logging.info("The solution is valid.")
        #     return 1
        # else:
        #     logging.error("The solution is invalid.")
        #     return -1


# Example usage:
if __name__ == "__main__":
    # Replace the path below with the actual location of your .cnf file.
    #filename = "C:\\Users\\hokie\\OneDrive - purdue.edu\\2025 Spring\\ECE 51216\\Project\\uf50-218\\uf50-05.cnf"
    filename = "C:\\Users\\hokie\\OneDrive - purdue.edu\\2025 Spring\\ECE 51216\\Project\\UUF50.218.1000\\uuf50-05.cnf"
    #filename = "C:\\Users\\hokie\\OneDrive - purdue.edu\\2025 Spring\\ECE 51216\\Project\\UF250.1065.100\\uf250-01.cnf"
    #filename = "C:\\Users\\hokie\\OneDrive - purdue.edu\\2025 Spring\\ECE 51216\\Project\\UUF250.1065.100\\uuf250-01.cnf"
    solve_sat_dpll(filename)
