<<<<<<< HEAD
from numpy import random
import pandas as pd
import json

L = [random.randint(1,5) for i in range(random.randint(10))]
print(L)

with open('tiny.json', 'r') as file:
    data = json.load(file)



vehicles = {}
for i in range(len(data["vehicles"])):
    vehicles[i] = data["vehicles"][i]["type"]

#print(vehicles)


constraints = {}
for i in range(len(data["constraints"])):
    constraints[i] = data["constraints"][i]

#print(constraints)


def women_be_shopping(L):
    cout=0
    for shop in constraints:
        if shop["shop"] == "paint":
            L_entry = L
            L_exit = []
            for i in range(len(L_entry)):
                if L_entry[i]
                    L_exit.append()
        
=======
import numpy as np


def permutations(L1,L2,L3, N):
    L_prime = L
    while n < N:
        p = np.random.random()
        if p < 0.8:
            random_swap(L1)
            random_swap(L2)
            random_swap(L3)
            if cost_resequencing(L1,L2,L3) < cost_resequencing(L):
                L = L_prime
    return L

def random_swap(L):
    i = np.random.randint(len(L))
    j = np.random.randint(len(L))
    L[i], L[j] = L[j], L[i]

def permutations(N):
>>>>>>> theo
