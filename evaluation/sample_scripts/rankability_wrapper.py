#!/usr/bin/python3.6
import sys
sys.path.append('/home/rankability/')
import json

from rankability_toolbox.exhaustive.rankability import *

problem_instance_file = sys.argv[1]

instance_info = json.load(open(problem_instance_file))
D = np.array(instance_info["D"])

solution = {}
k,p,P = exhaustive(D)
solution["k"] = int(k)
solution["p"] = int(p)
solution["P"] = np.array2string(P).replace('\n', '').replace(" ",",")

#print(solution)
print(json.dumps(solution))
