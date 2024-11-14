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



def paint_order(L,delta):
    L_entry = L
    index_entry=[i for i in range(len(L_entry))]
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






parametre_permut_1=[i for i in range(1,len(list(vehicles.values()))+1)]

new_sequence=[]
for i in parametre_permut_1:
    new_sequence.append(vehicles[i])
after_paint=paint_order(new_sequence,parameters['two_tone_delta'])[2]
parametre_permut_2=after_paint



def cost_resequencing(parametre_permut_1, parametre_permut_2):
    cost=parameters['resequencing_cost']
    C = 0
    for i in range(len(list(vehicles.keys()))):
        C+= cost*np.maximum(0, list(vehicles.keys())[i] - lag["body"] - parametre_permut_1[i])

    new_sequence=[]
    for i in parametre_permut_1:
        new_sequence.append(vehicles[i])
    after_paint=paint_order(new_sequence,parameters['two_tone_delta'])[2]
    
    for i in range(len(after_paint)) :
        C+= cost*np.maximum(0,  after_paint[i] - lag['paint'] - parametre_permut_2[i])
    return C 


print(cost_resequencing(parametre_permut_1, parametre_permut_2))



#print(paint_order(list(vehicles.values()),parameters['two_tone_delta']))
#print(vehicles)

