#!/usr/bin/python3.6

import argparse
import json
import numpy as np
import subprocess

def compare_answer(instance_info,answer):
    evaluation = {}
    evaluation["check_k"] = answer["k"] == instance_info["k"]
    print(instance_info["P"])
    print(len(instance_info["P"]))
    evaluation["check_p"] = answer["p"] == len(instance_info["P"])
    return evaluation

parser = argparse.ArgumentParser()
parser.add_argument("script", help="path to a script or executable that accepts one argument and that is a CSV formatted D matrix")
parser.add_argument("-t","--test_level", default="easy", help="easy, medium, or hard")
parser.add_argument("-d","--depth", default="0.1", help="0.1:0.1:1.0")
parser.add_argument("-s","--seed", default="0", help="random seed for selecting the test set")
parser.add_argument("-c","--config", default="config.json", help="program configuration file")

args = parser.parse_args()

config = json.load(open(args.config))

for instance in config[args.test_level]:
    instance_path = config["instance_directory"]+"/"+instance
    instance_info = json.load(open(instance_path))
    cmd_array = [args.script, instance_path]
    result = subprocess.run(cmd_array, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    answer = json.loads(result.stdout)
    evaluation = compare_answer(instance_info,answer)
    print(evaluation)
