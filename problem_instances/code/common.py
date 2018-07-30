import json
import numpy as np

def load_instance(path,as_numpy=True,starting_index=0):
    
    instance = json.loads(open(path).read())
    
    if as_numpy:
        instance["D"] = np.array(instance["D"])
    
    instance["P"] = np.array(instance["P"],dtype=int)
    
    shift = np.min(instance["P"]) - starting_index
    
    instance["P"] = instance["P"] - shift
    
    if not as_numpy:
        instance["P"] = instance["P"].aslist()
        
    return instance
    
    
    
    
    