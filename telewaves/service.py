"""
TeleWaves Service Module

Core service implementation for monitoring Telegram messages and downloading audio files.
Provides the main TeleWaves class that handles user authentication, message processing,
and audio file detection and download.
"""

import logging
from pathlib import Path

from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaDocument

from telewaves.constants import EXTENSION_PRESETS, _Presets

logger = logging.getLogger(__name__)


class TeleWaves:
    """
    Main service class for monitoring Telegram messages and downloading media files.

    This service acts as your personal Telegram user account to monitor all incoming
    messages for media files, automatically downloading them to a specified directory
    based on configurable extension filtering. Supports chat filtering to monitor
    only specific users or channels.

    Attributes:
        download_dir (Path): Directory where media files will be saved
        chat_filter (set[str] | None): Set of chat IDs/usernames to monitor (None = all chats)
        allowed_extensions (set[str]): Set of allowed file extensions for download
        client (TelegramClient): Telethon client for Telegram API interactions
    """

    def __init__(
        self,
        telegram_api_id: int,
        telegram_api_hash: str,
        session_dir: Path,
        download_dir: Path,
        chat_filter: set[str] | None = None,
        extensions_filter: set[str | _Presets] | None = None,
    ):
        """
        Initialize the TeleWaves service.

        Args:
            telegram_api_id (int): Telegram API ID from my.telegram.org/apps
            telegram_api_hash (str): Telegram API hash from my.telegram.org/apps
            session_dir (Path): Directory to store Telegram session files
            download_dir (Path): Directory to save downloaded media files
            chat_filter (set[str] | None): Set of chat IDs/usernames to monitor.
                                         If None, monitors all chats.
            extensions_filter (set[str] | None): File extensions to download.
                                                    Can be a set of extensions (e.g., {'.mp3', '.flac'}), or a
                                                    a preset name (e.g., 'audio'), or None for all media.

        Raises:
            FileNotFoundError: If download_dir doesn't exist or session_dir parent doesn't exist
            ValueError: If extension_filter preset is not recognized
        """
        self.download_dir = Path(download_dir)
        self.chat_filter = chat_filter

        if not self.download_dir.is_dir():
            raise FileNotFoundError(
                f"Download directory does not exist: {self.download_dir}"
            )
        if not session_dir.parent.is_dir():
            raise FileNotFoundError(
                f"Parent directory for session data does not exist: {session_dir.parent}"
            )

        if self.chat_filter:
            logger.info(f"Chat filter enabled for: {', '.join(self.chat_filter)}")
        else:
            logger.info("No chat filter - monitoring all chats")

        # Set up extension filtering
        self.allowed_extensions = set()
        if not extensions_filter:
            # Default behavior: download all media types
            logger.info(
                "No extension in extensions filter - downloading all media types"
            )
        else:
            for ext in extensions_filter:
                if extensions := EXTENSION_PRESETS.get(ext):
                    logger.debug(f"Extension preset found: {ext}")
                    self.allowed_extensions.update(extensions)
                else:
                    self.allowed_extensions.add(ext)
            logger.info(f"Selected extensions: {', '.join(self.allowed_extensions)}")

        self.client = TelegramClient(session_dir, telegram_api_id, telegram_api_hash)

    def _should_process_chat(self, chat_id: int, user_info: str | None = None) -> bool:
        """
        Check if we should process messages from this chat based on the chat filter.

        Args:
            chat_id (int): Telegram chat ID
            user_info (str | None): Username or user ID string (e.g., "@username" or "12345")

        Returns:
            bool: True if the chat should be processed, False otherwise
        """
        if not self.chat_filter:
            return True  # No filter means process all chats

        # Check chat ID
        if str(chat_id) in self.chat_filter:
            return True

        # Check based on user info (username or user ID)
        if user_info:
            user_info = user_info.lower()
            if (
                user_info in self.chat_filter
                or f"@{user_info.lower()}" in self.chat_filter
            ):
                return True
        return False

    def _should_download_file(self, file_path: Path) -> bool:
        """
        Check if a file should be downloaded based on the extensions filtering configuration.

        Args:
            file_path (Path): Path to the file to check

        Returns:
            bool: True if the file should be downloaded, False otherwise
        """
        if not self.allowed_extensions:
            # No extension filtering - download all media
            return True

        return file_path.suffix.lower() in self.allowed_extensions

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize filename for safe storage on the filesystem.

        Removes problematic characters and ensures the filename is safe to use
        across different operating systems.

        Args:
            filename (str): Original filename to sanitize

        Returns:
            str: Sanitized filename safe for filesystem storage
        """
        # Remove or replace problematic characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, "_")

        # Remove leading/trailing whitespace and dots
        filename = filename.strip(" .")

        # Ensure filename is not empty
        if not filename:
            filename = "untitled"

        return filename

    async def download_media_file(
        self, message, media, original_filename: str
    ) -> Path | None:
        """
        Download a media file from a Telegram message to the local filesystem.

        Handles filename sanitization, collision avoidance, and error handling
        during the download process.

        Args:
            message: Telegram message object containing the media
            media: Media object from the message
            original_filename (str): Original filename of the media file

        Returns:
            Path | None: Path to the downloaded file if successful, None if failed
        """
        # Sanitize filename
        safe_filename = self.sanitize_filename(original_filename)

        file_path = self.download_dir / safe_filename

        # Avoid overwriting existing files
        counter = 1
        original_path = file_path
        while file_path.exists():
            stem = original_path.stem
            suffix = original_path.suffix
            file_path = self.download_dir / f"{stem}_{counter}{suffix}"
            counter += 1

        logger.info(f"Downloading file to: {file_path}")

        try:
            # Download file using Telethon
            downloaded_path = await message.download_media(file=str(file_path))
            if downloaded_path:
                logger.info(f"Successfully downloaded: {file_path}")
                return Path(downloaded_path)
            else:
                logger.error(f"Failed to download file: {original_filename}")
                return None
        except Exception as e:
            logger.error(f"Failed to download file {original_filename}: {e}")
            return None

    @staticmethod
    def _user_info(user) -> str | None:
        """
        Get a string representation of the user for logging and filtering.

        Args:
            user: Telegram user object

        Returns:
            str | None: String representation (@username or user_id) or None if user is None
        """
        if not user:
            return None

        if hasattr(user, "username") and (username := user.username):
            return f"@{username}"
        else:
            return user.id

    async def process_message(self, event: events.NewMessage.Event):
        """
        Process incoming Telegram messages to detect and download media files.

        This method is called for every new message received by the Telegram client.
        It checks if the message contains media, applies chat filtering, and downloads
        any media files that match the configured extension filter.

        Args:
            event (events.NewMessage.Event): Telegram new message event
        """
        message = event.message

        if not message or not message.media:
            return

        chat_id = message.chat_id
        sender_info = self._user_info(await message.get_sender())

        # Check if we should process this chat
        if not self._should_process_chat(chat_id, sender_info):
            logger.debug(
                f"Skipping message from {sender_info} in chat {chat_id} (filtered out)"
            )
            return

        logger.info(f"Processing message from {sender_info} in chat {chat_id}")

        media = message.media
        filename = None
        should_download = False

        # Check different types of media
        if isinstance(media, MessageMediaDocument):
            # Document (could be audio file, voice message, video, etc.)
            document = media.document
            filename = next(
                (
                    attr.file_name
                    for attr in document.attributes
                    if hasattr(attr, "file_name") and attr.file_name
                ),
                None,
            )

            if not filename:
                filename = f"document_{document.id}"
                # Try to get extension from mime_type
                if document.mime_type:
                    mime_to_ext = {
                        "audio/mpeg": ".mp3",
                        "audio/mp4": ".m4a",
                        "audio/flac": ".flac",
                        "audio/ogg": ".ogg",
                        "audio/wav": ".wav",
                        "video/mp4": ".mp4",
                    }
                    ext = mime_to_ext.get(document.mime_type, "")
                    if ext:
                        filename += ext

            # Check if file should be downloaded based on extension filtering
            if filename:
                if self._should_download_file(Path(filename)):
                    logger.info(
                        f"Found matching file: {filename} (MIME: {document.mime_type})"
                    )
                    try:
                        # Download the file
                        downloaded_path = await self.download_media_file(
                            message, media, filename
                        )

                        if downloaded_path and downloaded_path.exists():
                            # Verify it matches our extension filter
                            if self._should_download_file(downloaded_path):
                                logger.info(
                                    f"Successfully processed media file: {downloaded_path}"
                                )

                                # Optional: Log file size
                                file_size = downloaded_path.stat().st_size
                                size_mb = file_size / (1024 * 1024)
                                logger.info(f"File size: {size_mb:.2f} MB")

                            else:
                                logger.warning(
                                    f"Downloaded file does not match extension filter: {downloaded_path}"
                                )
                                # Optionally remove filtered files
                                downloaded_path.unlink(missing_ok=True)
                                logger.info(f"Removed filtered file: {downloaded_path}")
                        else:
                            logger.error(
                                f"Failed to download or file doesn't exist: {filename}"
                            )
                    except Exception as e:
                        logger.error(f"Failed to process audio file {filename}: {e}")
                else:
                    logger.debug(
                        f"Document {filename} does not match extension filter (MIME: {document.mime_type})"
                    )

    async def run(self):
        """
        Start the TeleWaves service and begin monitoring Telegram messages.

        This method initializes the Telegram client, handles authentication,
        sets up message event handlers, and keeps the service running until
        manually stopped or disconnected. Downloads media files based on the
        configured extensions filtering.

        Raises:
            EOFError: When authentication is interrupted in non-interactive mode
            Exception: Various Telegram client or authentication errors
        """
        logger.info("Starting TeleWaves service...")
        logger.info(f"Download directory: {self.download_dir}")

        try:
            # Start the client (this will prompt for authentication if needed)
            logger.info(
                "Starting Telegram client... (you may be prompted for authentication)"
            )
            await self.client.start()

            # Get user info
            me = await self.client.get_me()
            logger.info(
                f"Logged in as: {me.first_name} {me.last_name or ''} ({('@' + me.username) or 'no username handle'})"
            )

            # Add event handler for new messages with media
            @self.client.on(events.NewMessage)
            async def handler(event):
                await self.process_message(event)

            logger.info("Monitoring your Telegram messages for media files...")

            # Keep the client running
            await self.client.run_until_disconnected()

        except EOFError:
            logger.error(
                "Authentication interrupted (EOF). Please run in an interactive terminal for first-time setup."
            )
        except Exception as e:
            logger.error(f"Failed to start Telegram client: {e}")
            if "phone" in str(e).lower() or "auth" in str(e).lower():
                logger.error(
                    "This may be an authentication issue. Please ensure you have valid API credentials."
                )
            raise
        finally:
            await self.client.disconnect()
