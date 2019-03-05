#!/usr/bin/python3.6
import sys
import json
import numpy as np
import math

problem_instance_file = sys.argv[1]

D = np.genfromtxt (problem_instance_file, delimiter=",")

# Now compute our solution
import pyrankability

search = pyrankability.exact.ExhaustiveSearch(D)
search.find_P()

print(pyrankability.common.as_json(search.k,search.P,{}))
