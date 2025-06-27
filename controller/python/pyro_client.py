import asyncio
import json
import os
import random
from pyrogram import Client
from pyrogram.types import Message
from phantomroll.controller.python.pyro_client import app


# Load settings
with open(os.path.expanduser('~/phantomroll/config/settings.json')) as f:
    cfg = json.load(f)

API_ID = cfg['api_id']
API_HASH = cfg['api_hash']
SESSION_NAME = cfg.get('session_name', 'phantomroll_session')

# Build full session path
SESSION_PATH = os.path.expanduser(f'~/phantomroll/phantomroll/controller/python/{SESSION_NAME}')

# Pyrogram client
app = Client(
    SESSION_PATH,
    api_id=API_ID,
    api_hash=API_HASH
)

sent_dice = []

async def send_dice(chat_id: str, emoji: str = "🎲") -> Message:
    async with app:
        msg = await app.send_dice(chat_id, emoji)
        value = msg.dice.value if msg.dice else None
        sent_dice.append((chat_id, msg.message_id, value, emoji))
        return msg

async def delete_message(chat_id: str, message_id: int):
    async with app:
        await app.delete_messages(chat_id, message_id)
    await asyncio.sleep(random.uniform(0.05, 0.12))
