import logging
from collections import deque
from input_parser import input_parser
from utils import validate_sat_solution


class CDCLSATSolver:
    def __init__(self, clauses, num_vars):
        self.num_vars = num_vars
        self.clauses = clauses
        self.assignment = {}  # Maps variable -> truth value
        self.trail = []  # List of assigned literals
        self.queue = deque()  # Propagation queue
        self.decision_levels = []  # List of decision level start indices
        self.implication = {}  # Maps literal -> reason clause

    def assign(self, literal):
        var = abs(literal)
        value = literal > 0
        if var in self.assignment:
            if self.assignment[var] != value:
                logging.debug(f"Conflict detected: variable {var} already assigned {self.assignment[var]}, trying to assign {value}")
                return False
            return True
        self.assignment[var] = value
        self.trail.append(literal)
        self.queue.append(literal)
        return True

    def backtrack(self):
        if not self.decision_levels:
            return
        last_decision_index = self.decision_levels.pop()
        while len(self.trail) > last_decision_index:
            literal = self.trail.pop()
            var = abs(literal)
            del self.assignment[var]
        self.queue.clear()  # Clear the propagation queue

    def propagate(self, literal):
        logging.debug(f"Propagating literal: {literal}")
        new_clauses = []
        conflict_clause = None

        for clause in self.clauses:
            if literal in clause:
                new_clauses.append(clause)
                continue
            new_clause = [l for l in clause if l != -literal]
            if len(new_clause) == 0:
                conflict_clause = clause
                break
            elif len(new_clause) == 1:
                unit_literal = new_clause[0]
                if not self.assign(unit_literal):
                    conflict_clause = clause
                    break
            else:
                new_clauses.append(new_clause)

        if conflict_clause:
            logging.debug(f"Conflict detected during propagation: {conflict_clause}")
            return conflict_clause

        self.clauses = new_clauses
        return None

    def unit_propagation(self):
        while self.queue:
            literal = self.queue.popleft()
            logging.debug(f"Unit propagating literal: {literal}")
            conflict_clause = self.propagate(literal)
            if conflict_clause:
                logging.debug(f"Conflict during unit propagation: {conflict_clause}")
                return conflict_clause
        return None

    def analyze_conflict(self, conflict_clause):
        logging.debug(f"Analyzing conflict for clause: {conflict_clause}")
        return [-lit for lit in conflict_clause]

    def branch(self):
        for var in range(1, self.num_vars + 1):
            if var not in self.assignment:
                self.decision_levels.append(len(self.trail))
                self.assign(var)
                logging.debug(f"Branching on variable: {var}")
                return True
        return False

    def cdcl(self):
        while True:
            logging.debug(f"Current clauses: {self.clauses}")
            logging.debug(f"Current assignment: {self.assignment}")
            logging.debug(f"Current trail: {self.trail}")

            # (1) Success check: If no clauses remain, the formula is SAT.
            if not self.clauses:
                logging.info("SATISFIABLE: All clauses satisfied.")
                return self.assignment

            # (2) Conflict check: If any clause is empty, UNSAT.
            if any(len(clause) == 0 for clause in self.clauses):
                logging.warning("UNSATISFIABLE: Found an empty clause.")
                return None

            # (3) Unit propagation
            conflict_clause = self.unit_propagation()
            if conflict_clause:
                logging.debug(f"Conflict detected with clause: {conflict_clause}")
                # Analyze conflict and backtrack
                learned_clause = self.analyze_conflict(conflict_clause)
                if learned_clause is None:
                    logging.warning("UNSATISFIABLE: Conflict analysis returned no learned clause.")
                    return None
                self.clauses.append(learned_clause)
                self.backtrack()

                # Propagate the learned clause
                self.queue.append(learned_clause[0])  # Add the first literal of the learned clause to the queue
                continue

            # (4) Branching
            if not self.branch():
                logging.warning("UNSATISFIABLE: No branching options available.")
                return None


def solve_sat_cdcl(filename):
    """
    Combines the input parser and the CDCL solver.
    Reads the CNF from the DIMACS file, runs the CDCL algorithm, and prints the results.
    """
    clauses, num_variables, _ = input_parser(filename)
    solver = CDCLSATSolver(clauses, num_variables)
    solution = solver.cdcl()
    if solution is None:
        logging.error("UNSAT result returned by the solver.")
        print("UNSAT")
        return 0
    else:
        logging.info(f"SAT result returned by the solver: {solution}")
        print("SAT:", solution)
        solution_list = []
        for var in range(1, num_variables + 1):
            val = 1 if solver.assignment.get(var, False) else 0
            solution_list.append(var if val else -var)
        
        if validate_sat_solution(clauses, solution_list):
            logging.info("SAT Solution is valid.")
            return 1
        else:
            logging.error("SAT Solution is invalid.")
            return -1

