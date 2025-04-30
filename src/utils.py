import logging

def validate_sat_solution(clauses, assignment):
    """
    Validates the solution of a SAT problem.
    
    Args:
        clauses (list): List of clauses in CNF format.
        assignment (list): List of assigned literals.
        
    Returns:
        bool: True if the assignment satisfies all clauses, False otherwise.
    """
    logging.debug(f"Validating assignment: {assignment} against clauses: {clauses}")
    
    # Create a set for fast lookup of assigned literals
    assigned_set = set(assignment)
    
    # Check each clause
    is_valid = True
    for clause in clauses:
        # Check if the clause is satisfied by the current assignment
        if not any(literal in assigned_set for literal in clause):
            logging.debug(f"Clause {clause} is not satisfied by the assignment {assignment}.")
            is_valid = False  # Clause is not satisfied
    
    return is_valid  # All clauses are satisfied