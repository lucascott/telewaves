# TeleWaves - Telegram media downloader

A simple service that monitors your personal Telegram messages for media files and automatically downloads them to a local directory. TeleWaves acts as your personal Telegram user account, giving it access to all messages sent to you, including from music bots and friends.

## ✨ Features

- **Chat Filtering**: Configure which chats/users to monitor
- **Extension Filtering**: Filter downloads by file extensions with presets (audio, video, image, document, archive) or custom extension lists
- **Session Persistence**: Authenticate once, works forever

## 🚀 Quick Start

### Get Telegram API Credentials

1. Visit [https://my.telegram.org/apps](https://my.telegram.org/apps)
2. Log in with your phone number
3. Create a new application (choose your preferred name):
   - **App title**: TeleWaves
   - **Short name**: telewaves
4. Copy your **API ID** and **API Hash**

### First Run Authentication
On first run, TeleWaves will prompt you to authenticate. Therefore, the recommended approach is to run the container interactively

```shell
docker run --rm -v ./data:/data -e TELEGRAM_API_ID=CHANGE_ME -e TELEGRAM_API_HASH=CHANGE_ME -it ghcr.io/lucascott/telewaves:main
```

After authenticating, your session is saved in the volume destination and you won't need to authenticate again.

### Run with Docker Compose

Copy the [`compose.yaml`](./compose.yaml), update the relevant parameters and run:
```shell
docker compose up -d
```

## 🎯 Chat Filtering

TeleWaves supports filtering which chats to monitor. This is useful if you only want to download files from specific bots or users.
By default, all chats are monitored.

### Filter Format
- **Usernames**: `@username` or `username` (case-insensitive)
- **Chat IDs**: `12345678` (numeric chat ID)
- **Multiple**: Comma-separated values

For example:
```shell
export CHAT_FILTER="@some_bot,12345678,@friend_username"
```

## 📁 Extension Filtering

TeleWaves supports filtering downloads by file extensions to only save the media types you want. 
By default, all media files are downloaded. Use a combination of predefined collections and/or explicit extensions to
have a fine-grained extensions filter.

The predefined collections of file extensions are (source: [`constants.py`](./telewaves/constants.py)):

- **`audio`**: `.mp3`, `.flac`, `.m4a`, `.ogg`, `.wav`, `.aac`, `.wma`, `.aiff`, `.ape`
- **`video`**: `.mp4`, `.avi`, `.mkv`, `.mov`, `.wmv`, `.flv`, `.webm`, `.m4v`
- **`image`**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.webp`, `.svg`
- **`document`**: `.pdf`, `.doc`, `.docx`, `.txt`, `.rtf`, `.odt`, `.pages`
- **`archive`**: `.zip`, `.rar`, `.7z`, `.tar`, `.gz`, `.bz2`, `.xz`

For example:
```shell
export EXTENSIONS_FILTER="audio,.pdf,.zip"
```

## ⚙️ Configuration

TeleWaves is configured via environment variables:

| Variable            | Default    | Description                                                        |
|---------------------|------------|--------------------------------------------------------------------|
| `TELEGRAM_API_ID`   | Required   | Telegram API ID from my.telegram.org/apps                          |
| `TELEGRAM_API_HASH` | Required   | Telegram API hash from my.telegram.org/apps                        |
| `DOWNLOAD_DIR`      | `/library` | Directory to save downloaded media files                           |
| `DATA_DIR`          | `/data`    | Directory for application data and sessions                        |
| `SESSION_NAME`      | `session`  | Name for Telegram session file                                     |
| `CHAT_FILTER`       | `""`       | Comma-separated chat IDs/usernames to monitor                      |
| `EXTENSIONS_FILTER` | `""`       | Comma-separated extensions/presets (e.g., "audio,video,.zip,.pdf") |

## 🔒 Security & Privacy

- **User Impersonation**: Acts as your personal Telegram account
- **No Data Collection**: No telemetry or data collection

## 📄 License

This project is provided as-is for educational and personal use. Always respect copyright laws and Telegram's Terms of Service when downloading content.

## ⚠️ Legal Disclaimer

TeleWaves acts as your personal Telegram user account. Use responsibly and in compliance with:
- Telegram's Terms of Service
- Copyright laws and intellectual property rights
- Local regulations regarding content downloading

Only download content you have permission to access. I'm not responsible for any misuse of this software.
