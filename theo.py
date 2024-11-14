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


def women_be_shopping(L):
    for shop in constraints:
        if shop["shop"] == "paint":
            L_entry = L
            L_exit = []
            for i in range(len(L_entry)):
                if L_entry[i] 
                    L_exit.append()