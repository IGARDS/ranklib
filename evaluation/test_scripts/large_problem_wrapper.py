#!/usr/bin/python3.6
import sys
import json
import numpy as np

problem_instance_file = sys.argv[1]

D = np.genfromtxt (problem_instance_file, delimiter=",")

# Now compute our solution
import pyrankability

large_problem_solver = pyrankability.approximate.LargeProblemSolver(D)
large_problem_solver.find_P(print_flag=True)
solution = large_problem_solver.to_json()

print(json.dumps(solution))
