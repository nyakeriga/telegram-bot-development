from telethon import TelegramClient
from telethon.errors import FloodWaitError
from telethon.tl.functions.messages import SendDiceRequest
import asyncio
import json
import os
import random

# Load credentials
with open(os.path.expanduser('~/phantomroll/config/settings.json')) as f:
    config = json.load(f)

API_ID = config['api_id']
API_HASH = config['api_hash']
SESSION_PATH = os.path.expanduser('~/phantomroll/session/phantomroll.session')

client = TelegramClient(SESSION_PATH, API_ID, API_HASH)

# Store sent dice messages
# Format: (message_id, raw_text, dice_value, emoji)
sent_dice = []

async def send_dice(chat_id: str, emoji: str = "🎲"):
    """
    Sends a dice emoji via raw SendDiceRequest for guaranteed dice.value.
    """
    # Send the dice through the MTProto function
    updates = await client.invoke(SendDiceRequest(
        peer=chat_id,
        emoji=emoji,
        random_id=random.randint(-2**63, 2**63 - 1)
    ))

    # The last update contains the message; extract it robustly
    if hasattr(updates, 'updates') and updates.updates:
        last = updates.updates[-1]
        m = getattr(last, 'message', None)
    else:
        # Fallback: fetch the most recent message
        msgs = await client.get_messages(chat_id, limit=1)
        m = msgs[0] if msgs else None

    value = getattr(getattr(m, "dice", None), "value", None) if m else None
    sent_dice.append((m.id if m else None, getattr(m, "raw_text", None), value, emoji))
    return m

async def delete_message(chat_id: str, message_id: int):
    try:
        await client.delete_messages(chat_id, message_id)
        await asyncio.sleep(random.uniform(0.05, 0.12))  # Stealthy human-like delay
    except FloodWaitError as e:
        print(f"[WARN] FloodWait triggered. Sleeping for {e.seconds} seconds...")
        await asyncio.sleep(e.seconds)
    except Exception as e:
        print(f"[ERROR] Deletion failed for message {message_id}: {e}")

async def delete_messages_fast(chat_id: str, message_ids: list[int]):
    for msg_id in message_ids:
        await delete_message(chat_id, msg_id)

async def main():
    await client.start()
    print("[+] Connected to Telegram!")

    chat = input("Enter target chat username or ID: ").strip()

    for _ in range(6):
        msg = await send_dice(chat, "🎲")
        val = msg.dice.value if msg and msg.dice else "❌"
        print(f"[SENT] ID: {msg.id if msg else 'N/A'}, Value: {val}")

    delete = input("Delete all messages? (y/n): ").strip().lower()
    if delete == "y":
        await delete_messages_fast(chat, [msg_id for msg_id, *_ in sent_dice if msg_id])
        print("[+] All messages deleted stealthily.")

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
