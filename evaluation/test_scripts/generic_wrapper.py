#!/usr/bin/python3.6
import sys
import json
import numpy as np
import tempfile
import subprocess

python_script = sys.argv[1]
problem_instance_file = sys.argv[2]

if "json" in problem_instance_file:
	instance_info = json.load(open(problem_instance_file))
	D = np.array(instance_info["D"])
else:
	D = np.genfromtxt (problem_instance_file, delimiter=",")

f = tempfile.NamedTemporaryFile(delete=False)
np.savetxt(f.name, D, delimiter=",")

print(subprocess.check_output([python_script, f.name],stderr=subprocess.STDOUT).decode())
