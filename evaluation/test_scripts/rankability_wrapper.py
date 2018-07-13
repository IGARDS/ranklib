#!/usr/bin/python3.6
import sys
sys.path.append('/home/rankability/')
import json
import numpy as np

from rankability_toolbox.exhaustive.rankability import *

problem_instance_file = sys.argv[1]

instance_info = json.load(open(problem_instance_file))
D = np.array(instance_info["D"])

solution = {}
k,p,P = exhaustive_index_1(D)
solution["k"] = k
solution["p"] = p
solution["P"] = P

print(json.dumps(solution))
