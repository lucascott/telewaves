"""
TeleWaves Constants Module

Defines default values and environment variable names used throughout the application.
"""

from enum import StrEnum
from typing import Literal


class Defaults(StrEnum):
    """Default configuration values for TeleWaves service."""

    chat_filter = ""
    extensions_filter = ""
    session_name = "telegram"
    data_dir = "/data"
    download_dir = "/library"


class EnvironmentVariables(StrEnum):
    """Environment variable names used for configuration."""

    TELEGRAM_API_ID = "TELEGRAM_API_ID"
    TELEGRAM_API_HASH = "TELEGRAM_API_HASH"
    DOWNLOAD_DIR = "DOWNLOAD_DIR"
    DATA_DIR = "DATA_DIR"
    SESSION_NAME = "SESSION_NAME"
    CHAT_FILTER = "CHAT_FILTER"
    EXTENSIONS_FILTER = "EXTENSIONS_FILTER"


# Predefined extension presets
Presets = Literal["audio", "video", "image", "document", "archive"]
EXTENSION_PRESETS = {
    "audio": {".mp3", ".flac", ".m4a", ".ogg", ".wav", ".aac", ".wma", ".aiff", ".ape"},
    "video": {".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".m4v"},
    "image": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp", ".svg"},
    "document": {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".pages"},
    "archive": {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"},
}
