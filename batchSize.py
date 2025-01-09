from typing import List, Dict

class BatchSize:
    def __init__(self, id: int, cost: float, min_batch_size: int, max_batch_size: int, vehicles: List[int]):
        self.id = id
        self.cost = cost
        self.min_batch_size = min_batch_size
        self.max_batch_size = max_batch_size
        self.vehicles = vehicles

    def __repr__(self):
        return (f"BatchSize(id={self.id}, cost={self.cost}, min_size={self.min_batch_size}, "
                f"max_size={self.max_batch_size}, vehicles={self.vehicles})")

    @classmethod
    def from_dict(cls, constraint_dict: Dict[str, any]):
        return cls(
            constraint_dict["id"],
            constraint_dict["cost"],
            constraint_dict["min_vehicles"],
            constraint_dict["max_vehicles"],
            constraint_dict["vehicles"],
        )


def is_a_batch(batch_size: BatchSize, sequence: List[int], batch_start_idx: int, batch_end_idx: int) -> bool:
    before_not_in = batch_start_idx == 0 or sequence[batch_start_idx - 1] not in batch_size.vehicles
    inside_in = all(v in batch_size.vehicles for v in sequence[batch_start_idx:batch_end_idx + 1])
    after_not_in = batch_end_idx == len(sequence) - 1 or sequence[batch_end_idx + 1] not in batch_size.vehicles
    return before_not_in and inside_in and after_not_in


def batch_size_cost(batch_size: BatchSize, sequence: List[int]) -> float:
    cost = 0.0
    for batch_start_idx in range(len(sequence)):
        for batch_end_idx in range(batch_start_idx, len(sequence)):
            if is_a_batch(batch_size, sequence, batch_start_idx, batch_end_idx):
                size = batch_end_idx - batch_start_idx + 1
                size_deviation = max(0, size - batch_size.max_batch_size, batch_size.min_batch_size - size)
                cost += batch_size.cost * (size_deviation ** 2)
    return cost
