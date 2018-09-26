#!/usr/bin/python3.6
import sys
import json
import numpy as np
import tempfile
import subprocess
import argparse
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument("python_script", help="Script to run. It must take a path to a csv formatted D matrix")
parser.add_argument("problem_instance_file", help="Path to csv formatted D matrix or a json file")
parser.add_argument("--timeout",default=600, type=int, help="seconds to allow a test to run")

args = parser.parse_args()

python_script = args.python_script
problem_instance_file = args.problem_instance_file

if "json" in problem_instance_file:
	instance_info = json.load(open(problem_instance_file))
	if "D" not in instance_info:
		ix = problem_instance_file.index(".csv")
		D_file = problem_instance_file[:ix]+".csv"
		D = np.genfromtxt (D_file, delimiter=",")
	else:
		D = np.array(instance_info["D"])
else:
	D = np.genfromtxt (problem_instance_file, delimiter=",")

f = tempfile.NamedTemporaryFile(delete=False)
np.savetxt(f.name, D, delimiter=",")

timeout=args.timeout

stdout_f = tempfile.NamedTemporaryFile(delete=True)
stderr_f = tempfile.NamedTemporaryFile(delete=True)
finished = False
try:
	subprocess.run([python_script, f.name],stdout=open(stdout_f.name,"w"),stderr=open(stderr_f.name,"w"),timeout=timeout)
	finished = True
except:
	pass

if finished:
    print(open(stdout_f.name).read()) 
else:
    print(open(stdout_f.name).read()) 
    #solution = {}
    #with open(stdout_f.name) as f:
    #    for line in f:
    #        if "prune" in line:
    #            prune_perm = [3,5,6,7]
                
print("STDERR:")
print(open(stderr_f.name).read())
