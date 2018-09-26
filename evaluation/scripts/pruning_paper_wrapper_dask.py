#!/usr/bin/python3.6
import sys
import json
import numpy as np
import math
from dask.distributed import Client
import shutil

problem_instance_file = sys.argv[1]

D = np.genfromtxt (problem_instance_file, delimiter=",")
shutil.copyfile(problem_instance_file, '/dev/shm/D.csv')  

# Now compute our solution
import pyrankability

import argparse

import pyrankability

client = Client("127.0.0.1:8786")

k,P,skipped = pyrankability.pruning_paper_dask.find_P("/dev/shm/D.csv",4,100,
                                                      bilp_method="orig",prune_history=True,check_and_recurse=False,client=client)
print(pyrankability.common.as_json(k,P,{"skipped":skipped,"percent_skipped": skipped*100./math.factorial(D.shape[0])}))
