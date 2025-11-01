"""
TeleWaves Configuration Module

Handles loading and parsing of configuration from environment variables,
including API credentials, directory paths, and chat filtering settings.
"""

import logging
import os
import sys
from dataclasses import dataclass
from pathlib import Path

from telewaves.constants import Defaults, EnvironmentVariables

_logger = logging.getLogger(__name__)


@dataclass
class Configuration:
    """
    Configuration container for TeleWaves service settings.

    Attributes:
        telegram_api_id (int): Telegram API ID from my.telegram.org/apps
        telegram_api_hash (str): Telegram API hash from my.telegram.org/apps
        download_dir (Path): Directory where audio files will be saved
        data_dir (Path): Base directory for application data
        session_dir (Path): Path to Telegram session file
        chat_filter (set[str]): Set of chat IDs/usernames to monitor
    """

    telegram_api_id: int
    telegram_api_hash: str
    download_dir: Path
    data_dir: Path
    session_dir: Path
    chat_filter: set[str]
    extensions_filter: set[str]


def _parse_comma_separated_entities(string_collection: str) -> set[str]:
    """
    Parse a comma-separated string of chat identifiers into a normalized set.

    Args:
        string_collection (str): Comma-separated string of entities

    Returns:
        set[str]: Set of normalized, lowercase chat identifiers
    """
    if not string_collection:
        return set()
    entities = string_collection.split(",")
    return {entity.strip().lower() for entity in entities if entity.strip()}


def load_configuration() -> Configuration:
    """
    Load TeleWaves configuration from environment variables with fallback to defaults.

    Reads configuration values from environment variables, validates them,
    and creates necessary directories. Exits the program if required
    configuration (API credentials) is missing or invalid.

    Returns:
        Configuration: Populated configuration object

    Raises:
        SystemExit: If required API credentials are missing or invalid
    """
    # Get API credentials from secrets or environment
    api_id_str = os.getenv(EnvironmentVariables.TELEGRAM_API_ID)
    api_hash = os.getenv(EnvironmentVariables.TELEGRAM_API_HASH)

    if not api_id_str or not api_hash:
        _logger.error("Telegram API credentials not found!")
        _logger.error(
            f"Please provide {EnvironmentVariables.TELEGRAM_API_ID} and {EnvironmentVariables.TELEGRAM_API_HASH} environment variables."
        )
        _logger.error("Get these from https://my.telegram.org/apps")
        sys.exit(1)

    try:
        api_id = int(api_id_str)
    except ValueError:
        _logger.error(f"{EnvironmentVariables.TELEGRAM_API_ID} must be a valid integer")
        sys.exit(1)

    chat_filter = os.getenv(EnvironmentVariables.CHAT_FILTER, Defaults.chat_filter)
    extensions_filter = os.getenv(
        EnvironmentVariables.EXTENSIONS_FILTER, Defaults.extensions_filter
    )

    data_dir = Path(os.getenv(EnvironmentVariables.DATA_DIR, Defaults.data_dir))
    data_dir.mkdir(parents=True, exist_ok=True)
    session_dir = data_dir / os.getenv(
        EnvironmentVariables.SESSION_NAME, Defaults.session_name
    )

    download_dir = Path(
        os.getenv(EnvironmentVariables.DOWNLOAD_DIR, Defaults.download_dir)
    )
    download_dir.mkdir(parents=True, exist_ok=True)

    return Configuration(
        telegram_api_id=api_id,
        telegram_api_hash=api_hash,
        download_dir=download_dir,
        data_dir=data_dir,
        session_dir=session_dir,
        chat_filter=_parse_comma_separated_entities(chat_filter),
        extensions_filter=_parse_comma_separated_entities(extensions_filter),
    )
