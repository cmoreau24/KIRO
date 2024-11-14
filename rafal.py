
import numpy as np
from numpy import random
import pandas as pd
import json

L = [random.randint(1,5) for i in range(random.randint(10))]
print(L)

with open('tiny.json', 'r') as file:
    data = json.load(file)

#for key, value in data.items():
#    print(f"{key}: {value}")


#
# print(data["vehicles"])

vehicles = {}
for i in range(len(data["vehicles"])):
    vehicles[i] = data["vehicles"][i]["type"]

#print(vehicles)


constraints = {}
for i in range(len(data["constraints"])):
    constraints[i] = data["constraints"][i]

#print(constraints)


def lot_change_cost(C):
    for constraint in constraints :
        if constraint["type"] == "lot_change": #pour chaque lot l
            D = {}
            c_l = constraint["cost"]
            for t in range(len(L)-1):#pour chaque véhicule
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

def rolling_window_cost(C):
    for constraint in constraints :
        if constraint["type"] == "rolling_window": 
            w_r = constraint["window_size"]
            c_r = constraint["cost"]
            Mr = constraint["max_vehicles"]
            for t in range(len(L)-w_r+2):
                S = 0
                for t2 in range(t,t+w_r):
                    if L[t2] in constraint["vehicles"]:
                        S += 1

                C += c_r*(max(0,S-Mr))**2

    return C







            
          




       


