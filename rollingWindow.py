from typing import List, Dict
from itertools import islice

class RollingWindow:
    def __init__(self, id: int, cost: float, window_size: int, max_vehicles: int, vehicles: List[int]):
        self.id = id
        self.cost = cost
        self.window_size = window_size
        self.max_vehicles = max_vehicles
        self.vehicles = vehicles

    @staticmethod
    def from_dict(constraint_dict: Dict[str, any]):
        return RollingWindow(
            id=constraint_dict["id"],
            cost=constraint_dict["cost"],
            window_size=constraint_dict["window_size"],
            max_vehicles=constraint_dict["max_vehicles"],
            vehicles=constraint_dict["vehicles"],
        )

    def __repr__(self):
        return (f"RollingWindow(id={self.id}, cost={self.cost}, window_size={self.window_size}, "
                f"max_vehicles={self.max_vehicles}, vehicles={self.vehicles})")

def partition(sequence: List[int], window_size: int, step: int):
    """
    Generate sliding windows (sublists) from the sequence.
    """
    return (sequence[i:i + window_size] for i in range(0, len(sequence) - window_size + 1, step))

def rolling_window_cost(rolling_window: RollingWindow, sequence: List[int]) -> float:
    cost = 0.0
    # For each window in the sequence
    for window_sequence in partition(sequence, rolling_window.window_size, 1):
        # Counting the number of vehicles concerned by the constraint in the window
        vehicles_in_window = sum(1 for v in window_sequence if v in rolling_window.vehicles)
        # Computing if this is too much
        over_vehicles = max(0, vehicles_in_window - rolling_window.max_vehicles)
        # Adding the cost
        cost += rolling_window.cost * (over_vehicles ** 2)
    return cost
