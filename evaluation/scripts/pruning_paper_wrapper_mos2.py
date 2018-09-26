#!/usr/bin/python3.6
import sys
import json
import numpy as np
import math

problem_instance_file = sys.argv[1]

D = np.genfromtxt (problem_instance_file, delimiter=",")

# Now compute our solution
import pyrankability

k,P,skipped = pyrankability.pruning_paper.find_P(D,4,100,bilp_method="mos2")#,prune_history_dir="/dev/shm/test/")
print(pyrankability.common.as_json(k,P,{"skipped":skipped,"percent_skipped": skipped*100./math.factorial(D.shape[0])}))
