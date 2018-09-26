#!/usr/bin/python3.6

import sys
sys.path.append("/home/rankability/")

import json

solution = json.load(open("out"))

import ranklib

graph_path = "/home/rankability/ranklib/problem_instances/instances/graphs/2018-08-24_14-51-35/D_strong_dom_50_flip_0.csv"

instance_path = ranklib.common.save_instance(graph_path,solution["P"],solution["k"],other=solution["other"])

print("Solution saved to",instance_path)