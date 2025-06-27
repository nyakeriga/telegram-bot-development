# combo_finder.py

from typing import List, Tuple
import itertools


def find_valid_combinations(target_sums: List[int]) -> List[Tuple[int, int, int]]:
    """
    Generate all 3-dice combinations (1-6) whose sum matches any in the target_sums list.

    Args:
        target_sums (List[int]): List of valid sums (e.g., [11, 13, 15])

    Returns:
        List[Tuple[int, int, int]]: List of matching dice triplets
    """
    valid_combinations = []
    all_rolls = itertools.product(range(1, 7), repeat=3)

    for combo in all_rolls:
        if sum(combo) in target_sums:
            valid_combinations.append(combo)

    return valid_combinations


# For debugging or standalone testing
if __name__ == "__main__":
    test_sums = [11, 13, 15]
    matches = find_valid_combinations(test_sums)
    print(f"[+] Found {len(matches)} valid combinations:")
    for combo in matches:
        print(f"  🎲 {combo} => {sum(combo)}")
