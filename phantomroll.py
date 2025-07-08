from telethon import TelegramClient
import asyncio
import time

api_id = 24238991
api_hash = 'd5e8a9523c901ae20c36208effd9909f'
client = TelegramClient('anon', api_id, api_hash)

async def main():
    await client.start()
    target = input("Enter username or group (e.g. @username): ")

    print("Sending 5 dice rolls...")
    messages = []
    for _ in range(5):
        msg = await client.send_message(target, '🎲')
        messages.append(msg)
        time.sleep(0.2)

    await asyncio.sleep(1)

    print("Deleting messages...")
    for msg in messages:
        await client.delete_messages(target, msg)

    print("Done.")

with client:
    client.loop.run_until_complete(main())
