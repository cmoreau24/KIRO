import json
from dataclasses import dataclass, field
from typing import List, Dict, Any
from pathlib import Path
from .vehicle import Vehicle
from .batchSize import BatchSize
from .lotChange import LotChange
from .rollingWindow import RollingWindow
from .shop import Shop


@dataclass
class Instance:
    name: str
    two_tone_delta: int
    shops: List[Shop] = field(default_factory=list)
    vehicles: List[Vehicle] = field(default_factory=list)

    def __str__(self):
        return (
            f"Instance(name = {self.name},\n"
            f"two-tone delta = {self.two_tone_delta},\n"
            f"vehicles ({len(self.vehicles)}) = [{','.join(str(v) for v in self.vehicles)}],\n"
            f"shops = [{','.join(str(s) for s in self.shops)}],\n"
            ")"
        )


def read_instance(instance_file: str, verbose: bool = False) -> Instance:
    print(f"Reading solution file {instance_file}")
    
    with open(instance_file) as f:
        instance_dict = json.load(f)

    name = Path(instance_file).stem
    if verbose:
        print(f"Instance name: {name}")

    instance = Instance(
        name=name,
        two_tone_delta=instance_dict["parameters"]["two_tone_delta"]
    )

    if verbose:
        print(f"Instance two-tone delta: {instance.two_tone_delta}")
        print(f"Instance vehicles: {len(instance_dict['vehicles'])}")

    for vehicle_dict in instance_dict["vehicles"]:
        vehicle = Vehicle(
            id=vehicle_dict["id"],
            is_two_tone=vehicle_dict["type"] == "two-tone"
        )
        instance.vehicles.append(vehicle)

    if verbose:
        print(instance.vehicles)
        print(f"Instance shops: {len(instance_dict['shops'])}")

    for shop_dict in instance_dict["shops"]:
        shop = Shop(
            name=shop_dict["name"],
            is_paint=shop_dict["name"] == "paint",
            resequencing_lag=shop_dict["resequencing_lag"],
            resequencing_cost=instance_dict["parameters"]["resequencing_cost"]
        )
        instance.shops.append(shop)

    if verbose:
        print(instance.shops)
        print(f"Instance constraints: {len(instance_dict['constraints'])}")

    for constraint_dict in instance_dict["constraints"]:
        shop_idx = next(i for i, shop in enumerate(instance.shops) 
                       if shop.name == constraint_dict["shop"])
        shop = instance.shops[shop_idx]

        if constraint_dict["type"] == "batch_size":
            batch_size = BatchSize.from_dict(constraint_dict)
            shop.batch_sizes.append(batch_size)

        elif constraint_dict["type"] == "lot_change":
            lot_change = LotChange.from_dict(constraint_dict)
            all_vehicles = sorted([v for partition in lot_change.partition for v in partition])
            unique_vehicles = set(all_vehicles)

            if (len(unique_vehicles) != len(instance.vehicles) or 
                len(all_vehicles) != len(instance.vehicles)):
                
                print(f"length(unique_vehicles): {len(unique_vehicles)}")
                print(f"length(all_vehicles): {len(all_vehicles)}")
                print(f"N vehicles: {len(instance.vehicles)}")
                print(all_vehicles)

                missing_vehicles = []
                for i in range(len(all_vehicles) - 1):
                    if all_vehicles[i] + 1 < all_vehicles[i + 1]:
                        missing_vehicles.extend(range(all_vehicles[i] + 1, all_vehicles[i + 1]))
                print(f"Missing vehicles: {missing_vehicles}")

                duplicated_vehicles = []
                for i in range(len(all_vehicles) - 1):
                    if all_vehicles[i] == all_vehicles[i + 1]:
                        duplicated_vehicles.append(all_vehicles[i])
                print(f"Duplicated vehicles: {duplicated_vehicles}")

                print(f"Warning: Lot change {lot_change.id} is not valid: {lot_change.partition} does not partition vehicles")
            else:
                shop.lot_changes.append(lot_change)

        elif constraint_dict["type"] == "rolling_window":
            rolling_window = RollingWindow.from_dict(constraint_dict)
            if rolling_window.window_size > len(instance.vehicles):
                print(f"Warning: Rolling window {rolling_window.id} is not valid: window size {rolling_window.window_size} is greater than number of vehicles {len(instance.vehicles)}")
            elif len(rolling_window.vehicles) == 0:
                print(f"Warning: Rolling window {rolling_window.id} is not valid: no vehicle in the rolling window")
            shop.rolling_windows.append(rolling_window)

    if verbose:
        print(instance.shops)

    return instance