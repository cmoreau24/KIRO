from numpy import random

import json
import numpy as np


with open('medium_1.json', 'r') as file:
    data = json.load(file)

vehicles = {}
for i in range(len(data["vehicles"])):
    vehicles[i+1] = data["vehicles"][i]["type"]

constraints = []
for i in range(len(data["constraints"])):
    constraints.append(data["constraints"][i])

lag = {}
for i in range(len(data["shops"])):
    lag[data["shops"][i]["name"]] = data["shops"][i]["resequencing_lag"]


parameters = data["parameters"]
#print(constraints)

def lot_change_cost(C,L_body,L_paint,L_assembly):
    for constraint in constraints :
        if constraint['shop']=="body":
            L=L_body
        elif constraint['shop']=="paint":
            L=L_paint
        else:
            L=L_assembly
        if constraint["type"] == "lot_change": #pour chaque lot l
            D = {}
            c_l = constraint["cost"]
            for t in range(len(L)):#pour chaque véhicule
                v = L[t]
                list = []
                for p in constraint["partition"]:
                    if v in p:
                        list = p
                D[t] = list
            for t in range(len(L)-1):
                if D[t] != D[t+1]:
                    if D[t] != []:
                        C += c_l
    return C

def rolling_window_cost(C,L_body,L_paint,L_assembly):
    for constraint in constraints :
        if constraint['shop']=="body":
            L=L_body
        elif constraint['shop']=="paint":
            L=L_paint
        else:
            L=L_assembly
        if constraint["type"] == "rolling_window": 
            w_r = constraint["window_size"]
            c_r = constraint["cost"]
            Mr = constraint["max_vehicles"]
            for t in range(len(L)-w_r+1):
                S = 0
                for t2 in range(t,t+w_r):
                    if L[t2] in constraint["vehicles"]:
                        S += 1

                C += c_r*(max(0,S-Mr))**2

    return C

def paint_order(parametre_permut_0,L,delta):
    L_entry = L
    L_exit = []
    
    index_entry=parametre_permut_0
    index_exit = []

    two_tone_temp = []
    two_tone_temp_index=[]
    two_tone_temp_time = np.array([])

    
    for i in range(len(L_entry)):
        if len(two_tone_temp_time)>0:
            for k in range(len(two_tone_temp_time)):
                if two_tone_temp_time[0]>=delta-1:

                    L_exit.append(two_tone_temp[0])
                    index_exit.append(two_tone_temp_index[0])
                    two_tone_temp=two_tone_temp[1:]
                    two_tone_temp_time=two_tone_temp_time[1:]
                    two_tone_temp_index=two_tone_temp_index[1:]

        if L[i] == "two-tone":
            two_tone_temp.append(L_entry[i])
            two_tone_temp_time = np.append(two_tone_temp_time,0)
            two_tone_temp_index.append(index_entry[i])
        
        else:
            L_exit.append(L_entry[i])
            index_exit.append(index_entry[i])
            two_tone_temp_time+=1

    L_exit=L_exit+two_tone_temp
    index_exit=index_exit+two_tone_temp_index

    return L_entry, L_exit, index_exit


def batch_size_cost(C,L_body,L_paint,L_assembly):
    for constraint in constraints :
        if constraint['shop']=="body":
            L=L_body
        elif constraint['shop']=="paint":
            L=L_paint
        else:
            L=L_assembly
        if constraint["type"] == "batch_size": 
            vehicles = constraint["vehicles"]
            m_b = constraint["min_vehicles"]
            M_b = constraint["max_vehicles"]
            c_b = constraint["cost"]
            y = [c_b*max(0,m_b-k,k-M_b)**2 for k in range (len(L))]
            for t in range(len(L)-1):
                for t2 in range(t,len(L)):
                    var1 = True
                    if t>1:
                        if L[t-1]  in vehicles:
                            var1 = False
                    var2 = True
                    for t3 in range(t,t2+1):
                        if not L[t3] in vehicles:
                            var2 = False
                    var3 = True
                    if t2<=len(L)-2:
                        if L[t2+1]in vehicles:
                                var3 = False
                    if var1 and var2 and var3:
                        C += y[t2-t]
           
    return C

def main(parametre_permut_0,parametre_permut_1, parametre_permut_2):
    cost=parameters['resequencing_cost']
    C = 0
    for i in range(len(parametre_permut_0)):
        C+= cost*np.maximum(0, parametre_permut_0[i] - lag["body"] - parametre_permut_1[i])

    new_sequence=[]
    for i in parametre_permut_1:
        new_sequence.append(vehicles[parametre_permut_0[i-1]+1])
    after_paint=paint_order(parametre_permut_0,new_sequence,parameters['two_tone_delta'])[2]
    
    for i in range(len(after_paint)) :
        C+= cost*np.maximum(0,  after_paint[i] - lag['paint'] - parametre_permut_2[i])

    L_body=parametre_permut_0
    L_paint=parametre_permut_1
    L_assembly=parametre_permut_2
    C=lot_change_cost(C,L_body,L_paint,L_assembly)
    C=rolling_window_cost(C,L_body,L_paint,L_assembly)
    C=batch_size_cost(C,L_body,L_paint,L_assembly)

    return C,np.array(after_paint)+1, np.array(parametre_permut_0)+1



parametre_permut_0=np.array(list(vehicles.keys()))-1
parametre_permut_1=([i for i in range(1,len(list(vehicles.values()))+1)])

new_sequence=[]
for i in parametre_permut_1:
    new_sequence.append(vehicles[i])
after_paint=paint_order(parametre_permut_0,new_sequence,parameters['two_tone_delta'])[2]



parametre_permut_2=after_paint

#print(parametre_permut_2)



def permutations(L1,L2,L3, N, swap):
    graph = []
    L1p=L1.copy()
    L2p=L2.copy()
    L3p =L3.copy()
    C=main(L1,L2,L3)[0]
    n=0
    while n < N:
        L1=swap(L1p)  # les listes divergent !
        L2=swap(L2p)
        L3=swap(L3p)
        C_temp=main(L1,L2,L3)[0]
        print(C_temp)
        graph.append(C_temp)
        if  C_temp <= C:
            L1p,L2p,L3p = L1,L2,L3
            C=C_temp
        n+=1
    return L1p,L2p,main(L1p,L2p,L3p)[1],L3p,C, graph

def random_swap(L):
    i = np.random.randint(len(L))
    j = np.random.randint(len(L))
    T=L.copy()
    T[i], T[j] = T[j], T[i]
    return T



print(main(parametre_permut_0,parametre_permut_1, parametre_permut_2)[0])

#print(permutations(parametre_permut_0,parametre_permut_1, parametre_permut_2,1000, random_swap))

#print(paint_order(list(vehicles.values()),parameters['two_tone_delta']))
#print(vehicles)


def close_swap(L):
    i = np.random.randint(len(L)-1)
    T=L.copy()
    T[i], T[i+1] = T[i+1], T[i]
    return T


def section_swap(L):
    m = np.random.randint()

#print(permutations(parametre_permut_0,parametre_permut_1, parametre_permut_2,10000, close_swap))

#1064300

def we_cooked_him(L1, L2, L3, alpha, T0, Tfin, N):
    graph = []
    L1p=L1.copy()
    L2p=L2.copy()
    L3p =L3.copy()
    C=main(L1,L2,L3)[0]

    L1_=close_swap(L1p)
    L2_=close_swap(L2p)
    L3_=close_swap(L3p)
    C_ = main(L1_, L2_, L3_)[0]

    if C < C_:
        L1opt = L1p
        L2opt = L2p
        L3opt = L3p
        C_opt = C
        C_test = C_
        L1_test = L1_
        L2_test = L2_
        L3_test = L3_


    else:
        L1opt = L1_
        L2opt = L2_
        L3opt = L3_
        C_opt = C_
        C_test = C
        L1_test = L1p
        L2_test = L2p
        L3_test = L3p

    T = T0
    while T < Tfin:
        if C_test < C_opt:
            L1opt = L1_test
            L2opt = L2_test
            L3opt = L3_test
            C_opt = C_test
            C_test = C_opt
            L1_test = L1opt
            L2_test = L2opt
            L3_test = L3opt
   
        p = np.exp(-(C_test - C_opt)/T)
        for n in range(N):
            if np.random.random() < p:
                L1=close_swap(L1opt)  # les listes divergent !
                L2=close_swap(L2opt)
                L3=close_swap(L3opt)
                C_temp=main(L1,L2,L3)[0]
                if  C_temp <= C_opt:
                    L1opt,L2opt,L3opt = L1,L2,L3
                    C_opt=C_temp
            else:
                L1=close_swap(L1_test)  # les listes divergent !
                L2=close_swap(L2_test)
                L3=close_swap(L3_test)
                C_temp=main(L1,L2,L3)[0]
                if  C_temp <= C_test:
                    L1_test,L2_test,L3_test = L1,L2,L3
                    C_test=C_temp
            graph.append(C_temp)
        T*=alpha

    if C_test < C_opt:
        L1opt = L1_test
        L2opt = L2_test
        L3opt = L3_test           
        C_opt = C_test
        C_test = C_opt
        L1_test = L1opt
        L2_test = L2opt
        L3_test = L3opt

    return L1opt,L2opt,main(L1opt,L2opt,L3opt)[1],L3opt,C_opt, graph
        


""" USING CLOSE SWAP WE GET THE GOD SOlUTION !!! 
        
       Small_1: 942700, (array([ 0,  2,  1,  4,  3,  5,  6,  7,  8,  9, 10, 11, 14, 12, 15, 13, 17,
       18, 16, 20, 24, 22, 23, 19, 28, 26, 21, 27, 25, 29, 31, 32, 30, 36,
       33, 37, 35, 34, 40, 38, 39, 41, 43, 42, 47, 44, 45, 46, 48, 49, 53,
       50, 52, 51]),  [1, 2, 5, 3, 6, 7, 4, 8, 9, 12, 11, 10, 13, 14, 16, 17, 18, 15, 19, 21, 23, 20, 22, 24, 25, 26, 27, 28, 29, 30, 35, 31, 33, 34, 38, 36, 39, 32, 37, 41, 42, 44, 40, 43, 45, 46, 48, 50, 47, 49, 52, 51, 53, 54], [ 1,  2,  5,  6,  7,  9, 10, 11, 12, 15, 18, 19, 23, 24, 20, 27, 22,
       28, 30, 32, 34, 38, 41,  3, 39, 40,  4, 42, 44,  8, 43, 48, 46, 47,
       13, 16, 14, 17, 21, 25, 29, 26, 33, 31, 37, 36, 35, 45, 49, 50, 54,
       51, 53, 52], [0, 3, 1, 4, 6, 8, 14, 10, 9, 11, 18, 15, 19, 20, 21, 26, 22, 27, 34, 29, 33, 35, 38, 2, 37, 39, 5, 42, 41, 7, 43, 47, 49, 46, 17, 16, 12, 13, 23, 24, 28, 25, 30, 31, 36, 32, 40, 48, 45, 52, 50, 51, 53, 44], 942700)"""

def minus_one(L):
    T = []
    for i in range(len(L)-1):
        T.append(L[i]-1)
    return T

list_1 = [ 0,  2,  1,  4,  3,  5,  6,  7,  8,  9, 10, 11, 14, 12, 15, 13, 17,
       18, 16, 20, 24, 22, 23, 19, 28, 26, 21, 27, 25, 29, 31, 32, 30, 36,
       33, 37, 35, 34, 40, 38, 39, 41, 43, 42, 47, 44, 45, 46, 48, 49, 53,
       50, 52, 51]
list_2 = [1, 2, 5, 3, 6, 7, 4, 8, 9, 12, 11, 10, 13, 14, 16, 17, 18, 15, 19, 21, 23, 20, 22, 24, 25, 26, 27, 28, 29, 30, 35, 31, 33, 34, 38, 36, 39, 32, 37, 41, 42, 44, 40, 43, 45, 46, 48, 50, 47, 49, 52, 51, 53, 54]
list_3 = [0, 3, 1, 4, 6, 8, 14, 10, 9, 11, 18, 15, 19, 20, 21, 26, 22, 27, 34, 29, 33, 35, 38, 2, 37, 39, 5, 42, 41, 7, 43, 47, 49, 46, 17, 16, 12, 13, 23, 24, 28, 25, 30, 31, 36, 32, 40, 48, 45, 52, 50, 51, 53, 44]

result = we_cooked_him(parametre_permut_0,parametre_permut_1, parametre_permut_2, 1.1, 100000000000, 200000000000, 100)
print(result)

#result = permutations(parametre_permut_0,parametre_permut_1, parametre_permut_2, 1000, close_swap)
import matplotlib.pyplot as plt
plt.plot(result[-1])
plt.show()