import numpy as np
import json
from pathlib import Path
from .instance import Instance
from .shop import shop_cost, delay_cost

class Solution:
    def __init__(self, entries: np.ndarray, exits: np.ndarray):
        self.entries = entries
        self.exits = exits
    
    def __str__(self):
        return f"Solution(entries=\n{self.entries}\nexits=\n{self.exits}\n)"


def compute_cost(instance: Instance, solution: Solution, verbose: bool = False) -> float:
    total_cost = 0.0
    if verbose:
        print("Computing solution cost")
    
    for s, shop in enumerate(instance.shops):
        if verbose:
            print(f"\nShop {shop.name}")
        
        # Extract the column for the current shop
        sequence = [row[s] for row in solution.entries]
        if verbose:
            print(f"Sequence {sequence} inside the shop")
        total_cost += shop_cost(shop, sequence, verbose=verbose)
        
        # Extract the column for the exits
        sequence = [row[s] for row in solution.exits]
        if verbose:
            print(f"Sequence {sequence} at exit of the shop")
        
        # Handle delay cost for the next shop
        if s < len(instance.shops) - 1:
            next_sequence = [row[s + 1] for row in solution.entries]
            if verbose:
                print(f"Sequence {next_sequence} inside the next shop")
            delay_cost_val = delay_cost(shop, sequence, next_sequence)
            if verbose:
                print(f"Delay cost: {delay_cost_val}")
            total_cost += delay_cost_val
    
    if verbose:
        print(f"\nTotal cost: {total_cost}")
    return total_cost

# def compute_cost(instance: Instance, solution: Solution, verbose: bool = False) -> float:
#     total_cost = 0.0
#     if verbose:
#         print("Computing solution cost")
    
#     for s, shop in enumerate(instance.shops):
#         if verbose:
#             print(f"\nShop {shop.name}")
        
#         sequence = solution.entries[:, s]
#         if verbose:
#             print(f"Sequence {sequence} inside the shop")
#         total_cost += shop_cost(shop, sequence, verbose=verbose)
        
#         sequence = solution.exits[:, s]
#         if verbose:
#             print(f"Sequence {sequence} at exit of the shop")
        
#         if s < len(instance.shops) - 1:
#             next_sequence = solution.entries[:, s + 1]
#             if verbose:
#                 print(f"Sequence {next_sequence} inside the next shop")
#             delay_cost_val = delay_cost(shop, sequence, next_sequence)
#             if verbose:
#                 print(f"Delay cost: {delay_cost_val}")
#             total_cost += delay_cost_val
    
#     if verbose:
#         print(f"\nTotal cost: {total_cost}")
#     return total_cost


def read_solution(instance: Instance, solution_file: str) -> Solution:
    with open(solution_file) as f:
        sol_dict = json.load(f)
    
    solution = zero_solution(instance)
    
    for s, shop in enumerate(instance.shops):
        solution.entries[:, s] = sol_dict[shop.name]["entry"]
        solution.exits[:, s] = sol_dict[shop.name]["exit"]
    
    return solution


def write_solution(instance: Instance, solution: Solution):
    sol_dict = {}
    for s, shop in enumerate(instance.shops):
        # Extract the column for the entries and exits
        entry_column = [row[s] for row in solution.entries]
        exit_column = [row[s] for row in solution.exits]

        sol_dict[shop.name] = {
            "entry": entry_column,
            "exit": exit_column
        }
    
    # Save the solution to a JSON file
    output_path = Path("solutions") / f"{instance.name}_sol.json"
    with open(output_path, "w") as f:
        json.dump(sol_dict, f)



def zero_solution(instance: Instance) -> Solution:
    n_vehicles = len(instance.vehicles)
    n_shops = len(instance.shops)
    return Solution(
        np.zeros((n_vehicles, n_shops), dtype=int),
        np.zeros((n_vehicles, n_shops), dtype=int)
    )