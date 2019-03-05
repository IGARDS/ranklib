#!/usr/bin/python3.6
import sys
import json
import numpy as np
import math
import subprocess

rankability_script = sys.argv[1]
problem_instance_file = sys.argv[2]
output_json_file = sys.argv[3]
output_k_file = sys.argv[4]
output_P_file = sys.argv[5]

try:
    output = subprocess.check_output([rankability_script,problem_instance_file])
    lines = []
    for line in output.decode("utf-8").split("\n"):
        if "Academic license" in line:
            continue
        lines.append(line)
    output = "\n".join(lines)
    output_json = json.loads(output)
except:
    print(output)
    exit(1)

open(output_json_file,"w").write(str(output_json))

open(output_k_file,"w").write(str(output_json["k"]))

#open("P.csv","w").write(str(output_json["P"]))
np.savetxt(output_P_file,output_json["P"],delimiter=",",fmt='%d')

print("k:",output_json["k"])
print("p:",output_json["p"])
print("P:",output_json["P"])
