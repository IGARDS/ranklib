import subprocess
import json

d="../../problem_instances/instances/graphs/2018-09-24_14-50-34/"
files = subprocess.check_output(["ls",d]).decode().split("\n")
fields = []
for f in files:
	if ".json" in f and "find_k" in f and "_10_flip_0_0" in f:
		fields += ['"'+f+'"']
		#print(f)
		#json.loads(open(d+f).read())

print(",".join(fields))
