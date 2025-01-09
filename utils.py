from .shop import Shop
from .vehicle import Vehicle
from .instance import Instance
from .solution import Solution
from copy import deepcopy

# Apply the two-tone permutation defined by two_tone_delta for the vehicle at position idx in the sequence
def two_tone_permute(sequence, idx, two_tone_delta, verbose=False):
    vehicle_delta = min(two_tone_delta, len(sequence) - idx)
    # If there is no delta to apply, return
    if vehicle_delta == 0:
        return
    
    # Otherwise, apply the permutation
    if verbose:
        print(f"\t{sequence[idx:idx + vehicle_delta]} became ", end="")
    
    two_tone_id = sequence[idx]
    sequence[idx:idx + vehicle_delta - 1] = sequence[idx + 1:idx + vehicle_delta]
    sequence[idx + vehicle_delta - 1] = two_tone_id
    
    if verbose:
        print("ok")
        print(sequence[idx:idx + vehicle_delta])


# Compute the paint shop exit sequence given the entry sequence
def paint_shop_exit_sequence(instance, sequence, verbose=False):
    EXIT = deepcopy(sequence)
    
    if verbose:
        print(f"Before permute:\n{EXIT}")

    # Boolean list to keep track of vehicles on which to apply perturbation
    apply_permute = [v.is_two_tone for v in instance.vehicles]
    
    if verbose:
        vehicles_to_permute = [v_id for v_id in sequence if apply_permute[v_id]]
        print(f"Vehicles to permute: {vehicles_to_permute}\n")

    idx = 0
    while any(apply_permute):
        # If the current vehicle is two-tone and has not yet been permuted, apply the permutation
        v_id = EXIT[idx]
        # print(v_id)
        # print(EXIT)
        # print(apply_permute)
        if apply_permute[v_id - 1]:
            if verbose:
                print(f"\nIdx {idx}: Permuting vehicle {v_id}")
            two_tone_permute(EXIT, idx, instance.two_tone_delta, verbose=verbose)

            # Mark the vehicle as permuted
            apply_permute[v_id - 1] = False

            if verbose:
                print(f"\tUpdated exit sequence:")
                print(f"\t{EXIT}\n")
        else:
            if instance.vehicles[v_id - 1].is_two_tone:
                if verbose:
                    print(f"Idx {idx}: Two-tone vehicle {v_id} has already been permuted")
            else:
                if verbose:
                    print(f"Idx {idx}: Vehicle {v_id} is not a two-tone vehicle")

            idx += 1

    return EXIT

# Construct an admissible solution with the entries
def create_solution(instance, entries):
    # Transpose the entries matrix
    transposed = [list(row) for row in zip(*entries)]
    entries = transposed

    if len(entries) != len(instance.vehicles) or len(entries[0]) != len(instance.shops):
        raise ValueError(
            f"entries must be a {len(instance.vehicles)} x {len(instance.shops)} matrix"
        )

    # Initialize the solution
    exits = [[0] * len(instance.shops) for _ in range(len(instance.vehicles))]

    for s in range(len(instance.shops)):
        # The exit sequence depends on the type of shop
        if instance.shops[s].is_paint:
            column = [row[s] for row in entries]
            exit_sequence = paint_shop_exit_sequence(instance, column)
            for i in range(len(exit_sequence)):
                exits[i][s] = exit_sequence[i]
        else:
            for i, row in enumerate(entries):
                exits[i][s] = row[s]
    # # on retranspose
    # transposed = [list(row) for row in zip(*entries)]
    # entries = transposed
    # transposed_exit = [list(row) for row in zip(*exits)]
    # exits = transposed_exit
    # print(Solution, "solution a la sortie de create")
    return Solution(entries, exits)


# def create_solution(instance, entries):
#     # print(entries)
#     transposed = [list(row) for row in zip(*entries)]
#     # print(transposed)
#     entries = transposed
#     # print(entries)

#     if len(entries) != len(instance.vehicles) or len(entries[0]) != len(instance.shops):
#         raise ValueError(
#             f"entries must be a {len(instance.vehicles)} x {len(instance.shops)} matrix"
#         )

#     # Initialize the solution
#     exits = [[0] * len(instance.shops) for _ in range(len(instance.vehicles))]
#     print(exits)
#     for s in range(len(instance.shops)):
#         # The exit sequence depends on the type of shop
#         if instance.shops[s].is_paint:
#             exits[:, s] = paint_shop_exit_sequence(instance, [row[s] for row in entries])
#         else:
#             for row in entries:
#                 print(row)
#             print(exits[:, s])
#             exits[:, s] = [row[s] for row in entries]

#     return Solution(entries, exits)

# from typing import List

# from .shop import Shop
# from .vehicle import Vehicle
# from .instance import Instance
# from .solution import Solution


# def two_tone_permute(sequence: List[int], idx: int, two_tone_delta: int, verbose: bool = False) -> None:
#     """Apply two-tone permutation at position idx with given delta."""
#     vehicle_delta = min(two_tone_delta, len(sequence) - idx)
#     if vehicle_delta == 0:
#         return
    
#     if verbose:
#         print(f"\t{sequence[idx:(idx + vehicle_delta + 1)]} became ", end="")
    
#     two_tone_id = sequence[idx]
#     sequence[idx:idx + vehicle_delta] = sequence[idx + 1:idx + vehicle_delta + 1]
#     sequence[idx + vehicle_delta] = two_tone_id
    
#     if verbose:
#         print(f"{sequence[idx:(idx + vehicle_delta + 1)]}")


# def paint_shop_exit_sequence(instance: Instance, sequence: List[int], verbose: bool = False) -> List[int]:
#     """Compute paint shop exit sequence given entry sequence."""
#     exit_seq = sequence.copy()
    
#     if verbose:
#         print(f"Before permute:\n{exit_seq}")
    
#     apply_permute = [v.is_two_tone for v in instance.vehicles]
    
#     if verbose:
#         print(f"Vehicles to permute: {[vid for vid, flag in enumerate(apply_permute) if flag]}\n")
    
#     idx = 0
#     while any(apply_permute):
#         v_id = exit_seq[idx]
#         print(v_id)
#         print(apply_permute)
#         if apply_permute[v_id]:
#             if verbose:
#                 print(f"\nIdx {idx}: Permuting vehicle {v_id}")
#             two_tone_permute(exit_seq, idx, instance.two_tone_delta, verbose)
#             apply_permute[v_id] = False
            
#             if verbose:
#                 print(f"\tUpdated exit sequence:\n\t{exit_seq}\n")
#         else:
#             if verbose:
#                 if instance.vehicles[v_id].two_tone:
#                     print(f"Idx {idx}: Two-tone vehicle {v_id} has already been permuted")
#                 else:
#                     print(f"Idx {idx}: Vehicle {v_id} is not a two-tone vehicle")
#             idx += 1
    
#     return exit_seq


# def create_solution(instance: Instance, entries: List[List[int]]) -> Solution:
#     """Construct solution from entry sequences."""
#     if len(entries) != len(instance.shops) :
#         raise ValueError(f"entries must be a {len(instance.vehicles)} x {len(instance.shops)} matrix")
    
#     exits = []
#     for s in range(len(instance.shops)):
#         if instance.shops[s].is_paint:
#             exits.append(paint_shop_exit_sequence(instance, entries[s]))
#         else:
#             exits.append(entries[s])
    
#     return Solution(entries=entries, exits=exits)


# def test_paint_shop_sequence():
#     """Test the paint shop sequencing logic."""
#     # Test 1: Basic two-tone vehicle sequence
#     vehicles = [Vehicle(True), Vehicle(False), Vehicle(False), Vehicle(True)]
#     shops = [Shop(True)]
#     instance = Instance(vehicles=vehicles, shops=shops, two_tone_delta=2)
#     sequence = [0, 1, 2, 3]  # Python uses 0-based indexing
    
#     result = paint_shop_exit_sequence(instance, sequence)
#     assert result == [1, 2, 0, 3], "Basic two-tone test failed"
    
#     # Test 2: Multiple two-tone vehicles
#     vehicles = [Vehicle(True), Vehicle(True), Vehicle(False), Vehicle(False)]
#     instance = Instance(vehicles=vehicles, shops=shops, two_tone_delta=2)
#     sequence = [0, 1, 2, 3]
    
#     result = paint_shop_exit_sequence(instance, sequence)
#     assert result == [2, 0, 3, 1], "Multiple two-tone test failed"
    
#     print("All tests passed!")

# if __name__ == "__main__":
#     test_paint_shop_sequence()