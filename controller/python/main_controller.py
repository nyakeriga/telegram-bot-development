import asyncio
import json
import os
import random
from pyrogram import Client
from pyrogram.errors import FloodWait
from combo_finder import find_valid_combinations

# === Hardcoded PhantomRoll App Details ===
API_ID = 24238991
API_HASH = "d5e8a9523c901ae20c36208effd9909f"
SESSION_NAME = "phantomroll_session"
SESSION_PATH = os.path.expanduser(f"~/phantomroll/session/{SESSION_NAME}")

# === Configuration Parameters ===
TARGET_SUMS = [11, 13, 15]  # Pre-set target sum combinations
DICE_EMOJI = "🎲"
ROLL_COUNT = 6
DELAY_BETWEEN = [0.35, 0.65]  # Range in seconds
VERBOSE = True
STEALTH = True

# === Initialize Pyrogram App ===
app = Client(SESSION_PATH, api_id=API_ID, api_hash=API_HASH)

async def roll_dice(chat: str):
    """
    Sends multiple dice messages to a specified Telegram chat.

    Args:
        chat (str): Target Telegram chat username or ID.

    Returns:
        list: List of tuples (message_id, dice_value)
    """
    sent_messages = []

    async with app:
        for _ in range(ROLL_COUNT):
            try:
                msg = await app.send_dice(chat, emoji=DICE_EMOJI)
                val = msg.dice.value if msg.dice else None
                sent_messages.append((msg.message_id, val))
                if VERBOSE:
                    print(f"[🎲] Sent: msg_id={msg.message_id}, value={val}")
                await asyncio.sleep(random.uniform(*DELAY_BETWEEN))

            except FloodWait as e:
                print(f"[!] Flood wait triggered: sleeping for {e.value}s")
                await asyncio.sleep(e.value)

    return sent_messages

async def process_dice(chat: str):
    """
    Orchestrates the full dice-rolling and deletion logic.

    Steps:
    1. Rolls dice and collects their values.
    2. Finds valid sum combinations from those values.
    3. Marks non-matching messages for deletion (stealth or verbose mode).
    """
    messages = await roll_dice(chat)
    values = [v for (_, v) in messages if v is not None]
    valid_combos = find_valid_combinations(values, TARGET_SUMS)

    if VERBOSE:
        print(f"[✔] Values: {values}")
        print(f"[🎯] Valid combos: {valid_combos}")

    if not valid_combos:
        print("[x] No valid sum combos found.")
        return

    # Extract message IDs for matching combos
    valid_ids = set()
    used_indices = set()

    for combo in valid_combos:
        combo_indices = []
        for v in combo:
            for i, val in enumerate(values):
                if val == v and i not in used_indices:
                    combo_indices.append(i)
                    used_indices.add(i)
                    break
        for idx in combo_indices:
            valid_ids.add(messages[idx][0])

    to_delete = [(msg_id, val) for (msg_id, val) in messages if msg_id not in valid_ids]

    if VERBOSE:
        print(f"[🧹] Will delete {len(to_delete)} messages (stealth={STEALTH})")

    # === Actual Deletion Phase ===
    for msg_id, val in to_delete:
        if STEALTH:
            print(f"[🔒] [STEALTH] Suppressing msg_id={msg_id}, val={val}")
            # Future: call cpp_bridge.delete_msg(msg_id)
        else:
            print(f"[!] Marked for deletion: msg_id={msg_id}, value={val}")
            # await app.delete_messages(chat, msg_id) — optional fallback

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="PhantomRoll Dice Controller")
    parser.add_argument("--chat", required=True, help="Target chat username or ID")
    parser.add_argument("--sums", help="Comma-separated target sums (e.g. 11,13,15)")
    parser.add_argument("--stealth", action="store_true", help="Enable stealth deletion")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    args = parser.parse_args()

    # Dynamic CLI overrides
    if args.sums:
        TARGET_SUMS[:] = [int(s.strip()) for s in args.sums.split(",") if s.strip().isdigit()]
    if args.stealth:
        STEALTH = True
    if args.verbose:
        VERBOSE = True

    asyncio.run(process_dice(args.chat))
