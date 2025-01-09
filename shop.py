import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Any
from .batchSize import BatchSize, batch_size_cost
from .lotChange import LotChange, lot_change_cost
from .rollingWindow import RollingWindow, rolling_window_cost

@dataclass
class Shop:
    name: str
    is_paint: bool
    resequencing_lag: int
    resequencing_cost: float
    batch_sizes: List[BatchSize] = field(default_factory=list)
    lot_changes: List[LotChange] = field(default_factory=list)
    rolling_windows: List[RollingWindow] = field(default_factory=list)

    def __str__(self):
        return (
            f"Shop(name = {self.name},\n"
            f"\tis_paint = {self.is_paint},\n"
            f"\tresequencing_lag = {self.resequencing_lag},\n"
            f"\tresequencing_cost = {self.resequencing_cost},\n"
            f"\tbatch_sizes ({len(self.batch_sizes)}) = [{','.join(str(b) for b in self.batch_sizes)}],\n"
            f"\tlot_changes ({len(self.lot_changes)}) = [{','.join(str(l) for l in self.lot_changes)}],\n"
            f"\trolling_windows ({len(self.rolling_windows)}) = [{','.join(str(r) for r in self.rolling_windows)}])"
        )


def shop_cost(shop: Shop, sequence: List[int], verbose: bool = False) -> float:
    shop_cost = 0.0
    lot_change_total = sum(lot_change_cost(lc, sequence) for lc in shop.lot_changes)
    if verbose:
        print(f"Lot change costs: {lot_change_total}")
    shop_cost += lot_change_total
    
    rolling_window_total = sum(rolling_window_cost(rw, sequence) for rw in shop.rolling_windows)
    if verbose:
        print(f"Rolling window costs: {rolling_window_total}")
    shop_cost += rolling_window_total
    
    batch_size_total = sum(batch_size_cost(bs, sequence) for bs in shop.batch_sizes)
    if verbose:
        print(f"Batch size costs: {batch_size_total}")
    shop_cost += batch_size_total
    
    if verbose:
        print(f"Shop cost: {shop_cost}")
    return shop_cost


def delay_cost(shop: Shop, sequence: List[int], next_sequence: List[int]) -> float:
    delay_cost = 0.0
    for exit_pos, v_id in enumerate(sequence, 1):
        # Check if v_id exists in next_sequence
        # print(next_sequence, v_id)
        if v_id not in next_sequence:
            print(f"Warning: Vehicle {v_id} not found in the next sequence.")
            # print(next_sequence)
            continue  # Skip or handle this case as needed

        # Get the position of v_id in next_sequence
        next_entry_pos = next_sequence.index(v_id) + 1

        # Calculate the delay
        delay = max(0, exit_pos - next_entry_pos - shop.resequencing_lag)

        # Accumulate delay cost
        delay_cost += shop.resequencing_cost * delay

    return delay_cost

# def delay_cost(shop: Shop, sequence: List[int], next_sequence: List[int]) -> float:
#     delay_cost = 0.0
#     for exit_pos, v_id in enumerate(sequence, 1):
#         next_entry_pos = np.where(next_sequence == v_id)[0][0] + 1
#         # next_entry_pos = next_sequence.index(v_id) + 1
#         delay = max(0, exit_pos - next_entry_pos - shop.resequencing_lag)
#         delay_cost += shop.resequencing_cost * delay
#     return delay_cost