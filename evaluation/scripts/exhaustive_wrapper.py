#!/usr/bin/python3.6
import sys
import json
import numpy as np
import math

problem_instance_file = sys.argv[1]

D = np.genfromtxt (problem_instance_file, delimiter=",")

# Now compute our solution
import pyrankability

search = pyrankability.exact.ExhaustiveSearch(D.shape[0])
search.leave_out = 4
search.prepare_iterators()
search.find_P(D,2)

print(pyrankability.common.as_json(search.k,search.P,{}))
