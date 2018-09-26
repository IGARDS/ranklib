#!/usr/bin/python3.6
import sys
import json
import numpy as np

problem_instance_file = sys.argv[1]

instance_info = json.load(open(problem_instance_file))
D = np.array(instance_info["D"])

# Now compute our solution
import pyrankability

search = pyrankability.MOSSearch(D)
search.prepare_iterators()
search.find_P()
solution = search.to_json()

print(json.dumps(solution))
