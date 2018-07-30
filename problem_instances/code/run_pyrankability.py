#!/usr/bin/python3.6

"""
Right now this is hard coded to assume an unweighted graph.
"""

import numpy as np
from dask.distributed import Client

import argparse

import pyrankability

import json

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("D", help="path to a CSV formatted D matrix")
    parser.add_argument("output", help="path to output json file")

    args = parser.parse_args()
    
    client = None # Client("127.0.0.1:8786")

    #D = np.loadtxt("../ranklib/problem_instances/instances/D_NCAA.csv",delimiter=",")
    #D = np.loadtxt("../ranklib/problem_instances/instances/D_strong_dom_25.csv",delimiter=",")
    #D = np.loadtxt("../ranklib/problem_instances/instances/D_strong_dom_25_flip_20.csv",delimiter=",")
    D = np.loadtxt(args.D,delimiter=",")
    
    rec_search = pyrankability.RecusiveKBoundedSearch(D,max_depth=10,target_search_space_at_leaf=1000,leave_out=4)
    rec_search.find_P(client)
    
    f = open(args.output,'w')
    res = rec_search.to_json()
    res["D"] = D.astype(int).tolist()
    f.write(json.dumps(res))
    f.close()
