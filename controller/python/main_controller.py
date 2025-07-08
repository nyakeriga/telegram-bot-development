import asyncio
import json
import os
from pyrogram import Client
from combo_finder import find_valid_combinations  # We'll build this next
# from pyro_client import send_dice, delete_message  # Temporarily disabled

# Load config
with open(os.path.expanduser('~/phantomroll/config/settings.json')) as f:
    settings = json.load(f)

with open(os.path.expanduser('~/phantomroll/config/sums_config.yaml')) as f:
    import yaml
    sum_config = yaml.safe_load(f)

# Pyrogram session details
API_ID = settings["api_id"]
API_HASH = settings["api_hash"]
SESSION_NAME = settings.get("session_name", "phantomroll_session")
SESSION_PATH = os.path.expanduser(f'~/phantomroll/phantomroll/controller/python/{SESSION_NAME}')

# Target group and sum combinations
TARGET_CHAT = settings.get("target_chat", "@targetgroup")
TARGET_SUMS = sum_config.get("target_sums", [11, 13, 15])

# Placeholder for dice values
rolled_values = []

# Pyrogram client
app = Client(SESSION_PATH, api_id=API_ID, api_hash=API_HASH)


async def simulate_dice_rolls():
    print(f"[+] Pretending to roll dice in {TARGET_CHAT} for sums {TARGET_SUMS}...")
    # Commented out actual sending for now
    for i in range(6):  # Simulate 6 dice
        # msg = await send_dice(TARGET_CHAT)
        # value = msg.dice.value if msg.dice else 1
        value = 1 + i % 6  # Simulated value for now
        rolled_values.append(value)
        print(f"[x] Fake rolled: {value}")
        await asyncio.sleep(0.1)

    print(f"[=] All values: {rolled_values}")
    combos = find_valid_combinations(rolled_values, TARGET_SUMS)
    if combos:
        print(f"[✓] Found valid combos: {combos}")
        # Here we would delete unmatched messages (disabled for now)
    else:
        print("[!] No matching combinations found.")


if __name__ == "__main__":
    asyncio.run(simulate_dice_rolls())
