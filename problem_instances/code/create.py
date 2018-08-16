#!/bin/python3.6

import numpy as np
import random

def create_strong_dom_graph(n):
    return np.triu(np.ones((n,n)), 1)

def create_fully_connected_graph(n):
    D = np.ones((n,n))
    for i in range(n):
        D[i,i] = 0
    return D

def flip_k(D,k):
    c = 0
    swapped = []
    while c < k:
        i = random.randint(0, D.shape[0]-1)
        j = random.randint(0, D.shape[1]-1)
        if i == j:
            continue
        if (i,j) in swapped:
            continue
        swapped.append((i,j))
        if D[i,j] == 0:
            D[i,j] = 1
        else:
            D[i,j] = 0
        c += 1
    
if __name__ == '__main__':
    random.seed(0)
    n_k_tuples = [(10,0),(10,2),(10,5),
                  (15,0),(15,5),(15,10),
                  (25,0),(25,5),(25,10),(25,20)]
    for n,k in n_k_tuples:
        print('(n,k)=',(n,k))
        D = create_strong_dom_graph(n)
        flip_k(D,k)
        np.savetxt("../instances/graphs/D_strong_dom_"+str(n)+"_flip_"+str(k)+".csv",D,delimiter=",",fmt="%d")
        
        D = create_fully_connected_graph(n)
        flip_k(D,k)
        np.savetxt("../instances/graphs/D_fully_connected_"+str(n)+"_flip_"+str(k)+".csv",D,delimiter=",",fmt="%d")
