#!/usr/bin/python3.6
import sys
sys.path.append('/home/rankability/rankability_toolbox_private')
import json
import numpy as np

problem_instance_file = sys.argv[1]

instance_info = json.load(open(problem_instance_file))
D = np.array(instance_info["D"])

# Now compute our solution
import pyrankability

solution = {}
rec_search = pyrankability.RecusiveKBoundedSearch(D,max_depth=3,target_search_space_at_leaf=1000,leave_out=4)
rec_search.find_P()
solution = rec_search.to_json()

print(json.dumps(solution))
