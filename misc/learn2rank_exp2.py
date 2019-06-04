import pandas as pd
import numpy as np
import copy
import os
import joblib

import sys
sys.path.insert(0,"/local/rankability_toolbox")

PATH_TO_RANKLIB='/local/ranklib'

import pyrankability

import pyltr

from dask.distributed import Client

client = Client("127.0.0.1:8786")

with open('MQ2007/Fold1/train.txt') as trainfile, \
        open('MQ2007/Fold1/vali.txt') as valifile, \
        open('MQ2007/Fold1/test.txt') as evalfile:
    TX, Ty, Tqids, Tdids = pyltr.data.letor.read_dataset(trainfile)
    VX, Vy, Vqid, Vdids = pyltr.data.letor.read_dataset(valifile)
    EX, Ey, Eqids, Edids = pyltr.data.letor.read_dataset(evalfile)
    
Tdocids = [did.split()[2] for did in Tdids] 

max_n = 100
results = {}
for qi, qid in enumerate(np.unique(Tqids)):
    inxs = np.where(Tqids == qid)[0]
    docids = np.array(Tdocids)[inxs]
    if len(docids) > max_n:
        print(qid,"size is >",max_n)
        continue
    print(len(docids),"number of documents for qid %d",qid)
    D = np.zeros((len(docids),len(docids)),dtype=int)
    for i in range(len(docids)):
        inxs_i = inxs[i]
        for j in range(i+1,len(docids)):
            inxs_j = inxs[j]
            if Ty[inxs_i] == Ty[inxs_j] and Ty[inxs_j] > 0:
                D[j,i] = 1
                D[i,j] = 1
                #D[i,j] = Ty[i]*1./Ty[j]
                #D[j,i] = Ty[j]*1./Ty[i]
            elif Ty[inxs_i] > Ty[inxs_j]:
                D[i,j] = 1
                #D[i,j] = Ty[i]
            elif Ty[inxs_j] > Ty[inxs_i]:
                D[j,i] = 1
                #D[j,i] = Ty[j]
    #np.round(10*D).astype(int)
    
    #np.savetxt("/dev/shm/D.csv", D, delimiter=",")
    
    try:
        k = pyrankability.pruning_paper.find_k(D,bilp_method="orig")
        #k,p,P = pyrankability.pruning_paper_dask3.find_P("/dev/shm/D.csv",4,100,bilp_method="orig",client=client)

        results[qid] = {}
        results[qid]["D"] = D
        results[qid]["k"] = k
        #results[qid]["p"] = p
        #results[qid]["P"] = P
        #print(output)
    except:
        print("Error on qid",qid)
    #if qi > 2:
    #    break
    
joblib.dump(results,"results_exp.joblib.z")
