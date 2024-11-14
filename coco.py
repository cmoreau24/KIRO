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
