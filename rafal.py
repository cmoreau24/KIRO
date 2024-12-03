
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
    return C

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

def batch_size_cost(C):
    for constraint in constraints :
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
                    if t2<=len(L)-2 :
                        if L[t2+1]in vehicles:
                                var3 = False
                    if var1 and var2 and var3:
                        C += y[t2-t]

            
    return C
                

                #C += c_r*(max(0,S-Mr))**2

    #return C



import numpy as np
def paint_shop(sequence:list,delta = 3):
    #sequence est une liste de listes contenant [véhicule(i),bool] où
    #  bool = true si véhicule(i) bicolor ; false sinon
    n = len(sequence) #nbre vehicules
    new_sequence = [[] for _ in range(n)]
    D1 = {} #dictionnaire des véhicules bicolores
    D2 = {} #dico des véhicules mono couleur
    for i in range(1,n+1):
        L = sequence[i-1]
        if L[1]: #si bicolor
            D1[i] = L
        else :
            D2[i] = L
    print(D1,D2)

    keys1 = []
    for i in D1 :
      keys1.append(i)
    keys2 = []
    for i in D2 :
      keys2.append(i)
    

    for i in keys1[::-1] :
      
      k = min(i+delta-1,n)
      while new_sequence[k-1] != [] :
        k -= 1
      
      new_sequence[k-1].append( D1[i] )
      
    for v in new_sequence[::-1] :
      if v == [] :
        num, v_ = D2.popitem()
        v.append(v_)
        
    print(new_sequence)



#paint_shop( [['v1',True], ['v2',False], ['v3',True] ,['v4',False], ['v5',False], ['v6',False], ['v7',False], ['v8',True], ['v9',True], ['v10',False]]  )

            
          




       


