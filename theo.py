from numpy import random
import pandas as pd
import json
import numpy as np


with open('tiny.json', 'r') as file:
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
    index_entry=parametre_permut_0
    index_exit = []
    L_exit = []
    two_tone_temp = []
    two_tone_temp_time = np.array([])
    two_tone_temp_index=[]
    
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





parametre_permut_0=np.array(list(vehicles.keys()))-1
parametre_permut_1=([i for i in range(1,len(list(vehicles.values()))+1)])

new_sequence=[]
for i in parametre_permut_1:
    new_sequence.append(vehicles[i])
after_paint=paint_order(parametre_permut_0,new_sequence,parameters['two_tone_delta'])[2]

new_sequence=['two-tone', 'regular', 'two-tone','regular','regular','regular','regular','two-tone','two-tone','regular']
print(new_sequence)
print(paint_order(parametre_permut_0,new_sequence,3)[2])

parametre_permut_2=after_paint


#print(parametre_permut_2)

def main(parametre_permut_0,parametre_permut_1, parametre_permut_2):
    cost=parameters['resequencing_cost']
    C = 0
    for i in range(len(parametre_permut_0)):
        C+= cost*np.maximum(0, parametre_permut_0[i] - lag["body"] - parametre_permut_1[i])

    new_sequence=[]
    for i in parametre_permut_1:
        new_sequence.append(vehicles[parametre_permut_0[i-1]+1])
    after_paint=paint_order(new_sequence,parameters['two_tone_delta'])[2]
    
    for i in range(len(after_paint)) :
        C+= cost*np.maximum(0,  after_paint[i] - lag['paint'] - parametre_permut_2[i])

    L_body=parametre_permut_0
    L_paint=parametre_permut_1
    L_assembly=parametre_permut_2
    C=lot_change_cost(C,L_body,L_paint,L_assembly)
    C=rolling_window_cost(C,L_body,L_paint,L_assembly)
    C=batch_size_cost(C,L_body,L_paint,L_assembly)

    return C,np.array(after_paint)+1, np.array(parametre_permut_0)+1


print(main(parametre_permut_0,parametre_permut_1, parametre_permut_2))



#print(paint_order(list(vehicles.values()),parameters['two_tone_delta']))
#print(vehicles)

