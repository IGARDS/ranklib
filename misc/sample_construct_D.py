import pandas as pd
import numpy as np
import copy
import os

from scipy.stats import zscore

from sklearn.feature_selection import VarianceThreshold

results_df = pd.read_csv("results_df.csv")
EX10 = np.genfromtxt('X.csv',delimiter=',')
Eqids10 = np.genfromtxt('qids.csv',delimiter=',')

def get_X(X,qids,qid):
    inxs = np.where(qids == qid)[0]
    return X[inxs,:]

def construct_D1(Xqid,frac=0.3):
    n = Xqid.shape[0]
    m = Xqid.shape[1]
    D = np.zeros((n,n),dtype=int)
    C = np.zeros((n,n),dtype=int)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            C[i,j] = len(np.where(Xqid[i,:] > Xqid[j,:])[0])
    D[C > m*frac] = 1
    return D,C

metrics = []
i = 0
for qid in results_df["qid"]:
    Xqid = get_X(EX10,Eqids10,qid)
    # Note: There is some weird numerical precision thing that makes me do this twice
    var_thres = VarianceThreshold()
    var_thres.fit(Xqid)
    trans = var_thres.transform(Xqid)
    var_thres2 = VarianceThreshold()
    var_thres2.fit(trans)
    Xqid_norm = zscore(var_thres2.transform(trans),axis=0)
    D,C = construct_D1(Xqid_norm,frac=0.4)
    metric = 0.0 # put your metric here run on D
    metrics.append(metric)
    if i % 10 == 0:
        print(i*1./results_df.shape[0])
    i += 1
    
results_df['metric'] = metrics

# Here are the type of commands I used to test for correlation
from scipy.stats import kendalltau
print(kendalltau(results_df["metric"],results_df["metric_mean"]))
