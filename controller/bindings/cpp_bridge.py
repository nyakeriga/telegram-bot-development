"""
cpp_bridge.py

This module acts as a bridge between Python and C++,
exposing C++ stealth functions to be used in the main Python controller.
"""

import ctypes
import os
import sys

# Determine the shared library extension based on OS
if sys.platform.startswith("linux"):
    LIB_NAME = "libphantomroll.so"
elif sys.platform == "darwin":
    LIB_NAME = "libphantomroll.dylib"
elif sys.platform == "win32":
    LIB_NAME = "phantomroll.dll"
else:
    raise RuntimeError("Unsupported OS for C++ bridge.")

# Construct absolute path to the compiled C++ shared library
LIB_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    "..", "..", "..",
    "core", "cplusplus", LIB_NAME
))

if not os.path.exists(LIB_PATH):
    raise FileNotFoundError(f"Shared library not found at: {LIB_PATH}")

# Load the C++ shared library
cpp_lib = ctypes.CDLL(LIB_PATH)

# Define the argument and return types of the C++ function
cpp_lib.delete_telegram_message.argtypes = [ctypes.c_int64, ctypes.c_int32]
cpp_lib.delete_telegram_message.restype = ctypes.c_int

def delete_message(chat_id: int, message_id: int) -> bool:
    """
    Deletes a Telegram message using the C++ stealth method.

    Args:
        chat_id (int): The ID of the chat where the message resides.
        message_id (int): The ID of the message to delete.

    Returns:
        bool: True if deletion succeeded, False otherwise.
    """
    result = cpp_lib.delete_telegram_message(chat_id, message_id)
    return result == 0
