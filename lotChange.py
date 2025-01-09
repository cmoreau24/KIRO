from typing import List, Dict

class LotChange:
    def __init__(self, id: int, cost: float, partition: List[List[int]]):
        self.id = id
        self.cost = cost
        self.partition = partition

    def __repr__(self):
        return f"LotChange(id={self.id}, cost={self.cost}, partition={self.partition})"

    @classmethod
    def from_dict(cls, constraint_dict: Dict[str, any]):
        return cls(
            constraint_dict["id"],
            constraint_dict["cost"],
            constraint_dict["partition"],
        )


def lot_change_cost(lot_change: LotChange, sequence: List[int]) -> float:
    cost = 0.0
    for v_idx in range(len(sequence) - 1):
        v = sequence[v_idx]
        current_lot = next((lot for lot in lot_change.partition if v in lot), None)
        next_v = sequence[v_idx + 1]
        next_lot = next((lot for lot in lot_change.partition if next_v in lot), None)
        if current_lot != next_lot:
            cost += lot_change.cost
    return cost
