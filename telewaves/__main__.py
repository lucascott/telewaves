"""
TeleWaves - Telegram Audio File Monitor

Entry point for the TeleWaves service. Loads configuration from environment
variables and starts the Telegram monitoring service.

Usage:
    python -m telewaves

Environment Variables:
    TELEGRAM_API_ID: Your Telegram API ID from my.telegram.org/apps
    TELEGRAM_API_HASH: Your Telegram API hash from my.telegram.org/apps
    DOWNLOAD_DIR: Directory to save downloaded audio files (default: /library)
    DATA_DIR: Directory for application data (default: /data)
    SESSION_NAME: Name for Telegram session file (default: session)
    CHAT_FILTER: Comma-separated list of chat IDs/usernames to monitor (optional)
"""

import asyncio
import logging

from telewaves.configuration import load_configuration
from telewaves.service import TeleWaves

_logger = logging.getLogger(__name__)


async def main():
    """
    Main entry point for TeleWaves service.

    Loads configuration and starts the TeleWaves service.
    """
    config = load_configuration()
    await TeleWaves(
        config.telegram_api_id,
        config.telegram_api_hash,
        config.session_dir,
        config.download_dir,
        config.chat_filter,
        config.extensions_filter,
    ).run()


if __name__ == "__main__":
    asyncio.run(main())
