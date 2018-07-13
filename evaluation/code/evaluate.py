#!/usr/bin/python3.6

import argparse
import json
import numpy as np
import subprocess
import time

class Comparison:
    def __init__(self,instance_info,answer,time_in_seconds):
        self.check_k = answer["k"] == instance_info["k"]
        self.diff_k = abs(answer["k"] - instance_info["k"])
        self.check_p = answer["p"] == len(instance_info["P"])
        self.diff_p = abs(answer["p"] - len(instance_info["P"]))
        instance_P = set([tuple(entry) for entry in instance_info["P"]])
        answer_P = set([tuple(entry) for entry in answer["P"]])
        self.set_diff_P_missing = str(instance_P.difference(answer_P))
        self.set_diff_P_extra = str(answer_P.difference(instance_P))
        self.time_in_seconds = time_in_seconds
        if "other" in answer:
            self.other = str(answer["other"])
        else:
            self.other = ""
    
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
        res += "\n"
        res += "Other: "+self.other
        return res
    
def load_instance(instance_dir,instance="small_1.json"):
    instance_path = instance_dir+"/"+instance
    instance_info = json.load(open(instance_path))
    return instance_info

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("script", help="path to a script or executable that accepts one argument and that is a CSV formatted D matrix")
    parser.add_argument("--test_level", default="easy", help="easy, medium, or hard")
    parser.add_argument("--depth", default="0.1", help="0.1:0.1:1.0")
    parser.add_argument("--seed", default="0", help="random seed for selecting the test set")
    parser.add_argument("--config", default="config.json", help="program configuration file")
    parser.add_argument("--output",default=None, help="output the results to this JSON file")
    parser.add_argument("--num_timing_tests",default=1, type=int, help="the number of timing tests to run and report")

    args = parser.parse_args()

    config = json.load(open(args.config))
 
    evaluations = {}
    for instance in config[args.test_level]:
        evaluations[instance] = []
        instance_path = config["instance_directory"]+"/"+instance
        instance_info = json.load(open(instance_path))
        cmd_array = [args.script, instance_path]
        print("Running: " + " ".join(cmd_array))
        for i in range(args.num_timing_tests):
            print("Iteration",i)
            start_time = time.time()
            result = subprocess.run(cmd_array, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            end_time = time.time()
            time_in_seconds = end_time - start_time
            try:
                answer = json.loads(result.stdout)
                evaluations[instance].append(Comparison(instance_info,answer,time_in_seconds))
            except:
                print('ERROR on',instance)
                print("STDOUT:")
                print(result.stdout.decode())
                print("STDERR:")
                print(result.stderr.decode())
                
    if args.output:
        prepare_for_output = {}
        for key,values in evaluations.items():
            prepare_for_output[key] = []
            for value in values:
                prepare_for_output[key].append(value.__dict__)
        open(args.output,"w").write(json.dumps(prepare_for_output))

    # Now output pretty results
    avg_k_diff = 0
    avg_p_diff = 0
    avg_time_in_seconds = 0
    print("Summary of results:")
    for key,value in evaluations.items():
        print("\n")
        print(key)
        avg_k_diff_iter = 0
        avg_p_diff_iter = 0
        avg_time_in_seconds_iter = 0
        for value in values:
            print("\t"+"\n\t".join(str(value).split("\n")))
            avg_k_diff_iter += value.diff_k
            avg_p_diff_iter += value.diff_p
            avg_time_in_seconds_iter += value.time_in_seconds
        avg_k_diff_iter = avg_k_diff_iter*1./len(values)
        avg_p_diff_iter = avg_p_diff_iter*1./len(values)
        avg_time_in_seconds_iter = avg_time_in_seconds_iter*1./len(values)
        avg_k_diff += avg_k_diff_iter
        avg_p_diff += avg_p_diff_iter
        avg_time_in_seconds += avg_time_in_seconds_iter
        print("Iteration average difference in k:",avg_k_diff_iter)
        print("Iteration average difference in p:",avg_p_diff_iter)
        print("Iteration average time in seconds:",avg_time_in_seconds_iter)
    
    avg_k_diff = avg_k_diff*1./len(evaluations)
    avg_p_diff = avg_p_diff*1./len(evaluations)
    avg_time_in_seconds = avg_time_in_seconds*1./len(evaluations)
    print("Overall average difference in k:",avg_k_diff)
    print("Overall average difference in p:",avg_p_diff)
    print("Overall average time in seconds:",avg_time_in_seconds)
