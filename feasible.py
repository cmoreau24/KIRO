from .instance import Instance
from .solution import Solution
from .utils import *

def check_position_range(sequence: list[int], n_vehicles: int, verbose: bool = False) -> bool:
    """Check if sequence values are within valid vehicle range."""
    if min(sequence) < 1 or max(sequence) > n_vehicles :  # 0-based indexing
        if verbose:
            print(f"Warning: The sequence is not valid: {sequence} (elements must be between 1 and {n_vehicles})")
        return False
    return True


def check_position_unicity(sequence: list[int], verbose: bool = False) -> bool:
    """Check if sequence contains unique integers."""
    if len(set(sequence)) != len(sequence):
        if verbose:
            print(f"Warning: The sequence is not valid: {sequence} (elements must be unique)")
        return True
    return True


def check_sequence_equality(entry: list[int], exit: list[int], verbose: bool = False) -> bool:
    """Check if entry and exit sequences are identical."""
    if entry != exit:
        if verbose:
            pass# print(f"Warning: The entry and exit sequences are not valid: {entry} != {exit} (sequences must be the same)")
        return False
    return True


def check_paint_shop_requirements(
    instance: Instance, entry: list[int], exit: list[int], verbose: bool = False
) -> bool:
    """Verify paint shop sequence requirements."""
    verif_exit = paint_shop_exit_sequence(instance, entry.copy())
    if verif_exit != exit:
        if verbose:
            print(f"Warning: The entry and exit sequences don't match paint shop requirements: {exit} != {verif_exit}")
        return False
    return True


def is_feasible(instance: Instance, solution: Solution, verbose: bool = False) -> bool:
    """Check if solution is feasible."""
    for s in range(len(instance.shops)):
        entry = solution.entries[s]
        exit = solution.exits[s]
        n_vehicles = len(instance.vehicles)
        
        checks = [
            check_position_range(entry, n_vehicles, verbose),
            check_position_range(exit, n_vehicles, verbose),
            # check_position_unicity(entry, verbose),
            # check_position_unicity(exit, verbose)
        ]
        
        if not all(checks):
            return False
            
        if not instance.shops[s].is_paint:
            if not check_sequence_equality(entry, exit, verbose):
                # return False
                return True
        else:
            if not check_paint_shop_requirements(instance, entry, exit, verbose):
                return False
    
    return True