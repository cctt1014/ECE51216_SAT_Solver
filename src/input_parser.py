def input_parser(filename):
    """    this function takes file path of DIMACS CNF file(.cnf format) and parses it returning clauses(list), number of variables and number of clauses
    DIMACS format has 3 type of lines:
      comment line: starts with "c" which are ignored
      problem line: starts with "p", for example, "p cnf 3 4", item3 and item4 is the number of variables and clauses
      clause lines: consisting of integer literals, each clause is ends with a 0 ex) 1 -2 0 
    """
    
    num_variables= 0              
    num_clauses=0                
    clauses=[]                   
    current_clause=[]  #temporary list to accumulate literals for the current clause
    
    # opens the .cnf file specified by variable 'filename', in read mode ('r'), the with statement acts as a context manager
    with open(filename, 'r') as f:
        #process each line in the file
        for line in f:
            line=line.strip()  # .strip() removes whitespace in the beginning and end 
            
            #skip empty lines
            if not line:
                continue
            

            #skip comment lines
            if line.startswith('c') or line.startswith('%'): #added '%' to skip the line, there is % at the end of the .cnf file
                continue


            #process the problem specification line
            if line.startswith('p'):
                parts=line.split()
                # expecting the line to be of the form: "p cnf <num_variables> <num_clauses>"
                if len(parts)>=4:
                    try:
                        num_variables=int(parts[2])
                        num_clauses=int(parts[3])
                    except ValueError:
                        raise ValueError("Invalid number format in problem line")
                else:
                    raise ValueError("Problem line is missing required information")
                continue  #move to next line
            

            #process clause lines
            tokens=line.split()  # split the line into tokens (each token is a literal)
            for token in tokens:
                try:
                    literal = int(token)
                except ValueError:
                    raise ValueError(f"Invalid literal encountered: {token}")
                
                if literal==0:  #end of a clause, clause line ends with 0
                    if current_clause:
                        clauses.append(current_clause)
                        current_clause=[]  #reset the temporary list for the next clause
                else:
                    current_clause.append(literal) #add the literal to the current clause
    
    #if file did not end with a 0, add it
    if current_clause:
        clauses.append(current_clause)
        
    return clauses, num_variables, num_clauses

# uncomment to test 
#if __name__ == "__main__":
#     cnf, n_vars, n_clauses = input_parser("C:\\Users\\kim4802\\OneDrive - purdue.edu\\2025 Spring\\ECE 51216\\Project\\uf50-218\\uf50-01.cnf") #this should be the path to your cnf file
#     print("Parsed Clauses:", cnf)
#     print("Number of Variables:", n_vars)
#     print("Number of Clauses:", n_clauses)
