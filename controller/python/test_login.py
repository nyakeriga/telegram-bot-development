# test_login.py

from pyrogram import Client

api_id = 24238991
api_hash = "d5e8a9523c901ae20c36208effd9909f"

# This will persist the session to phantomroll_session.session
with Client("phantomroll_session", api_id=api_id, api_hash=api_hash) as app:
    print("✅ Logged in successfully!")


