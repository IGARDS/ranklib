#!/usr/bin/python3.6

import argparse
import json
import numpy as np
import subprocess

class Comparison:
    def __init__(self,instance_info,answer):
        self.check_k = answer["k"] == instance_info["k"]
        self.diff_k = abs(answer["k"] - instance_info["k"])
        self.check_p = answer["p"] == len(instance_info["P"])
        self.diff_p = abs(answer["p"] - len(instance_info["P"]))
        instance_P = set([tuple(entry) for entry in instance_info["P"]])
        answer_P = set([tuple(entry) for entry in answer["P"]])
        self.set_diff_P_missing = str(instance_P.difference(answer_P))
        self.set_diff_P_extra = str(answer_P.difference(instance_P))
    
    def __str__(self):
        res = "Check k: "+str(self.check_k)
        res += "\n"
        res = "Difference k: "+str(self.diff_k)
        res += "\n"
        res += "Check p: "+str(self.check_p)
        res += "\n"
        res += "Difference p: "+str(self.diff_p)
        res += "\n"
        res += "Set difference P missing: "+str(self.set_diff_P_missing)
        res += "\n"
        res += "Set difference P extra: "+str(self.set_diff_P_extra)
        return res
    
def load_instance(instance_dir,instance="small_1.json"):
    instance_path = instance_dir+"/"+instance
    instance_info = json.load(open(instance_path))
    return instance_info

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("script", help="path to a script or executable that accepts one argument and that is a CSV formatted D matrix")
    parser.add_argument("-t","--test_level", default="easy", help="easy, medium, or hard")
    parser.add_argument("-d","--depth", default="0.1", help="0.1:0.1:1.0")
    parser.add_argument("-s","--seed", default="0", help="random seed for selecting the test set")
    parser.add_argument("-c","--config", default="config.json", help="program configuration file")
    parser.add_argument("-o","--output",default=None, help="output the results to this JSON file")

    args = parser.parse_args()

    config = json.load(open(args.config))

    evaluations = {}
    for instance in config[args.test_level]:
        instance_path = config["instance_directory"]+"/"+instance
        instance_info = json.load(open(instance_path))
        cmd_array = [args.script, instance_path]
        #print(" ".join(cmd_array))
        result = subprocess.run(cmd_array, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #print(result.stdout,result.stderr)
        try:
            answer = json.loads(result.stdout)
            evaluations[instance] = Comparison(instance_info,answer)
        except:
            print('ERROR on',instance)
            #print(result.stdout)
            #print(result.stderr)
    if args.output:
        prepare_for_output = {}
        for key,value in evaluations.items():
            prepare_for_output[key] = value.__dict__
        open(args.output,"w").write(json.dumps(prepare_for_output))

    # Now output pretty results
    avg_k_diff = 0
    avg_p_diff = 0
    for key,value in evaluations.items():
        print(key)
        print("\t"+"\n\t".join(str(value).split("\n")))
        avg_k_diff += value.diff_k
        avg_p_diff += value.diff_p

    avg_k_diff = avg_k_diff*1./len(evaluations)
    avg_p_diff = avg_p_diff*1./len(evaluations)
    print("Average difference in k:",avg_k_diff)
    print("Average difference in p:",avg_p_diff)
