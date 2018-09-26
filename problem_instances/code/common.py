import json
import numpy as np

np.set_printoptions(threshold=np.nan)

def load_instance(path,as_numpy=True,starting_index=0):
    
    instance = json.loads(open(path).read())
    
    if as_numpy:
        instance["D"] = np.array(instance["D"],dtype=int)
    
    instance["P"] = np.array(instance["P"],dtype=int)
    
    shift = np.min(instance["P"]) - starting_index
    
    instance["P"] = instance["P"] - shift
    
    if not as_numpy:
        instance["P"] = instance["P"].aslist()
        
    return instance

def save_instance(graph_path,P,k,other={}):
    if type(P) != list:
        P = P.tolist()
    if ".csv" not in graph_path:
        raise Exception("graph_path must end with .csv")
    D = np.genfromtxt (graph_path, delimiter=",").astype(int).tolist()
    instance_path = graph_path.replace(".csv",".json")
    if "ranklib" in graph_path:
        fields = graph_path.replace("//","/").split("/")
        ix = fields.index("ranklib")
        graph_path = "/".join(fields[ix:])
    else:
        raise Exception("graph_path must include ranklib folder in the path")
    k = int(k)
    p = len(P)
    indent = "    "
    instance_as_string = "{\n"
    instance_as_string += indent + json.dumps({"k": k}).replace("{","").replace("}","")+",\n"
    instance_as_string += indent + json.dumps({"p": p}).replace("{","").replace("}","")+",\n"
    instance_as_string += indent + '"P": \n'
    P_as_string = np.array2string(np.array(P,dtype=int),separator=",",max_line_width=np.Inf).replace("[","[\n",1)
    lines = P_as_string.split("\n")
    for i,line in enumerate(lines):
        add_indent = indent+indent
        if i > 0:
            add_indent += indent
        instance_as_string += add_indent + line + "\n"
    instance_as_string = instance_as_string[:-2] + "],\n"
    instance_as_string += indent + '"D": \n'
    D_as_string = np.array2string(np.array(D,dtype=int),separator=",",max_line_width=np.Inf).replace("[","[\n",1)
    lines = D_as_string.split("\n")
    for i,line in enumerate(lines):
        add_indent = indent+indent
        if i > 0:
            add_indent += indent
        if i == 1:
            add_indent += " "
        instance_as_string += add_indent + line + "\n"
    instance_as_string = instance_as_string[:-2] + "],\n"
    instance_as_string += indent + json.dumps({"other": other})[1:-1]+"\n"
    instance_as_string += "}"
    
    open(instance_path,"w").write(instance_as_string)
    
    return instance_path
    
    
    
    
    