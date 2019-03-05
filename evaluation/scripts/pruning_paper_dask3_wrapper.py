#!/usr/bin/python3.6
import sys
import json
import numpy as np
import math

problem_instance_file = sys.argv[1]

# Now compute our solution
import pyrankability

k,p,P = pyrankability.pruning_paper_dask3.find_P(problem_instance_file,4,100,bilp_method="orig",client=client)

print(pyrankability.common.as_json(k,P,{}))
