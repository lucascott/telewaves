"""
TeleWaves - Telegram Audio File Monitor

A powerful Python service that monitors your personal Telegram messages
for audio files and automatically downloads them to a local directory.

TeleWaves acts as your personal Telegram user account, giving it access
to all messages sent to you, including from music bots and friends.
"""

import logging
import os

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

from telewaves.configuration import Configuration, load_configuration
from telewaves.service import TeleWaves

__all__ = ["TeleWaves", "Configuration", "load_configuration"]
