import pandas as pd
import numpy as np
import copy
import os

from dask.distributed import Client
from scipy.stats import zscore

from sklearn.externals import joblib

from sklearn.feature_selection import VarianceThreshold

import pyltr

import sys
sys.path.insert(0,"/local/rankability_toolbox")

PATH_TO_RANKLIB='/local/ranklib'

import pyrankability

load_model = True

metric = pyltr.metrics.KendallTau()

if load_model == False:
    with open('MQ2008-list/Fold1/train.txt') as trainfile, \
            open('MQ2008-list/Fold1/vali.txt') as valifile, \
            open('MQ2008-list/Fold1/test.txt') as evalfile:
        TX, Ty, Tqids, Tdids = pyltr.data.letor.read_dataset(trainfile)
        VX, Vy, Vqids, Vdids = pyltr.data.letor.read_dataset(valifile)
        EX, Ey, Eqids, Edids = pyltr.data.letor.read_dataset(evalfile)

    def subset_max_rank(X,y,qids,dids,max_rank = 10):
        keep_inxs = np.where(y<=max_rank)[0]
        X = X[keep_inxs,:]
        y = y[keep_inxs]
        qids = qids[keep_inxs]
        dids = dids[keep_inxs]
        return X,y,qids,dids

    TX10,Ty10,Tqids10,Tdids10 = subset_max_rank(TX,Ty,Tqids,Tdids)
    VX10,Vy10,Vqids10,Vdids10 = subset_max_rank(VX,Vy,Vqids,Vdids)
    EX10,Ey10,Eqids10,Edids10 = subset_max_rank(EX,Ey,Eqids,Edids)

    # Only needed if you want to perform validation (early stopping & trimming)
    monitor = pyltr.models.monitors.ValidationMonitor(
        VX10, Vy10, Vqids10, metric=metric, stop_after=250)

    model = pyltr.models.LambdaMART(
        metric=metric,
        n_estimators=1000,
        learning_rate=0.01,
        max_features=0.5,
        query_subsample=0.5,
        max_leaf_nodes=10,
        min_samples_leaf=64,
        verbose=1
    )

    model.fit(TX10, Ty10, Tqids10, monitor=monitor)
    
    joblib.dump(model,"model.joblib.z")
    
    def predict_process(model,metric,X,y,qids,dids):
        pred = model.predict(X)
        unique_qids = np.unique(qids)
        inxs_qid = {}
        rank_pred_qid = {}
        metric_mean_random_qid = {}
        metric_mean_qid = {}
        for qid in unique_qids:
            inxs_qid[qid] = np.where(qids == qid)[0]
            pred_qid = pred[inxs_qid[qid]]
            inxs_argsort = np.argsort(pred_qid)
            rank_pred_qid[qid] = np.zeros((len(inxs_qid[qid]),),dtype=int)
            rank_pred_qid[qid][inxs_argsort] = np.arange(rank_pred_qid[qid].shape[0],dtype=int)+1
            metric_mean_random_qid[qid] = metric.calc_mean_random(qids[inxs_qid[qid]], y[inxs_qid[qid]])
            metric_mean_qid[qid] = metric.calc_mean(qids[inxs_qid[qid]], y[inxs_qid[qid]], pred_qid)
        return rank_pred_qid, metric_mean_random_qid,metric_mean_qid

    rank_pred_qid,metric_mean_random_qid,metric_mean_qid = predict_process(model,metric,EX10,Ey10,Eqids10,Edids10)

    unique_qids = list(rank_pred_qid.keys())
    results_df = pd.DataFrame({"qid": unique_qids,"metric_mean":[metric_mean_qid[k] for k in unique_qids],"metric_mean_random":[metric_mean_random_qid[k] for k in unique_qids]})

    results_df.to_csv("results_df.csv",index=False)

    np.savetxt('X.csv',EX10,"%.4f",delimiter=",")
    np.savetxt('qids.csv',Eqids10,'%s',delimiter=',')
else:
    print('Loading saved model')
    model = joblib.load("model.joblib.z")
    
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

client = Client("127.0.0.1:8786")

ks = []
#Ps = []
ps = []
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
    np.savetxt("/dev/shm/D.csv",D,"%d",delimiter=",")
    k,P = pyrankability.pruning_paper_dask2.find_P("/dev/shm/D.csv",4,100,bilp_method="orig",prune_history=False,client=client)
    ks.append(k)
    #Ps.append(P)
    ps.append(len(P))
    if i % 10 == 0:
        print(i*1./results_df.shape[0])
    i += 1
    
results_df['k'] = ks
results_df['p'] = ps

results_df.to_csv("results_df_2.csv",index=False)