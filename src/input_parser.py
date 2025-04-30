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

# uncomment to test 
#if __name__ == "__main__":
#     cnf, n_vars, n_clauses = input_parser("C:\\Users\\kim4802\\OneDrive - purdue.edu\\2025 Spring\\ECE 51216\\Project\\uf50-218\\uf50-01.cnf") #this should be the path to your cnf file
#     print("Parsed Clauses:", cnf)
#     print("Number of Variables:", n_vars)
#     print("Number of Clauses:", n_clauses)
