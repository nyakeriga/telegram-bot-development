import json
import os

config = {
    "api_id": 24238991,
    "api_hash": "d5e8a9523c901ae20c36208effd9909f",
    "use_test_dc": False,
    "database_directory": "tdlib-db",
    "use_message_database": False,
    "use_secret_chats": False,
    "system_language_code": "en",
    "device_model": "PhantomDevice",
    "system_version": "1.0",
    "application_version": "0.1",
    "delete_delay_ms": 100
}

# Use absolute path based on script location
output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../core/cplusplus/config/tdlib_config.json"))
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(config, f, indent=4)

print(f"[OK] Configuration written to {output_path}")
