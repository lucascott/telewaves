"""
TeleWaves Constants Module

Defines default values and environment variable names used throughout the application.
"""

from enum import StrEnum


class Defaults(StrEnum):
    """Default configuration values for TeleWaves service."""

    chat_filter = ""
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
