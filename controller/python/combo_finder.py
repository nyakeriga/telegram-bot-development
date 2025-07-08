"""
combo_finder.py

Module to find valid 3-dice combinations whose sum matches a list of target values.
Designed for precision and fault tolerance.
"""

from typing import List, Tuple
from itertools import combinations

def find_valid_combinations(dice_values: List[int], target_sums: List[int]) -> List[Tuple[int, int, int]]:
    """
    Find all unique 3-dice combinations whose sum is in the target_sums list.

    Args:
        dice_values (List[int]): The list of dice values (e.g., [2, 3, 5, 6, 1, 4])
        target_sums (List[int]): The target sums to match (e.g., [11, 13, 15])

    Returns:
        List[Tuple[int, int, int]]: A list of valid 3-dice combinations.
    """

    if len(dice_values) < 3:
        return []  # Not enough dice to form any combination

    valid_combos = []

    for combo in combinations(dice_values, 3):
        if sum(combo) in target_sums:
            valid_combos.append(combo)

    # Remove duplicates (same values, different order)
    unique_combos = list(set(tuple(sorted(c)) for c in valid_combos))

    return sorted(unique_combos)

def find_first_valid_combination(
    dice_values: List[int], target_sums: List[int]
) -> Tuple[int, int, int] | None:
    """
    Return the first valid 3-dice combo whose sum matches target_sums (or None if none found).

    Args:
        dice_values (List[int]): Dice results
        target_sums (List[int]): Valid sum targets

    Returns:
        Tuple[int, int, int] | None: First valid 3-dice combination or None
    """
    if len(dice_values) < 3:
        return None

    for combo in combinations(dice_values, 3):
        if sum(combo) in target_sums:
            return tuple(sorted(combo))

    return None

# For testing purposes (safe to import)
if __name__ == "__main__":
    dice = [1, 4, 6, 3, 2, 5]
    targets = [10, 12, 15]
    print("Valid combos:", find_valid_combinations(dice, targets))
    print("First valid combo:", find_first_valid_combination(dice, targets))
