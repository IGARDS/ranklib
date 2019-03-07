#!/usr/bin/python3.6
import sys
import json
import numpy as np
import math

problem_instance_file = sys.argv[1]

D = np.genfromtxt (problem_instance_file, delimiter=",")

# Now compute our solution
import pyrankability

Dtilde,output= pyrankability.improve.greedy(D,1)

print(json.dumps("Dtilde": Dtilde, "output": output))
