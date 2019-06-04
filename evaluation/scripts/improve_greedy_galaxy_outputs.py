#!/usr/bin/python3.6
import sys
import json
import numpy as np
import math
import subprocess

rankability_script = sys.argv[1]
problem_instance_file = sys.argv[2]
output_json_file = sys.argv[3]
output_Dtilde = sys.argv[4]
output_output = sys.argv[5]

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
    exit(1)

open(output_json_file,"w").write(str(output_json))

open(output_Dtilde,"w").write(str(output_json["Dtilde"]))

open(output_output,"w").write(str(output_json["output"]))

#open("P.csv","w").write(str(output_json["P"]))
#np.savetxt(output_output,output_json["output"],delimiter=",",fmt='%d')

print(output_json["output"])
