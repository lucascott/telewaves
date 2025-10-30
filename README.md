# TeleWaves - Telegram media downloader

A simple service that monitors your personal Telegram messages for media files and automatically downloads them to a local directory. TeleWaves acts as your personal Telegram user account, giving it access to all messages sent to you, including from music bots and friends.

## ✨ Features

- 🎯 **Smart Chat Filtering**: Configure which chats/users to monitor
- 📁 **Format filtering**: Supports filtering for specific file extensions
- 🔄 **Session Persistence**: Authenticate once, works forever

## 🚀 Quick Start

### 1. Get Telegram API Credentials

1. Visit [https://my.telegram.org/apps](https://my.telegram.org/apps)
2. Log in with your phone number
3. Create a new application (choose your preferred name):
   - **App title**: TeleWaves
   - **Short name**: telewaves
4. Copy your **API ID** and **API Hash**

### 3. First Run Authentication
On first run, TeleWaves will prompt you to authenticate. Therefore, the recommended approach is to run the container interactively

```shell
docker run --rm -v ./data:/data -e TELEGRAM_API_ID=CHANGE_ME -e TELEGRAM_API_HASH=CHANGE_ME -it ghcr.io/lucascott/telewaves
```

After authentication, your session is saved in the volume destination and you won't need to authenticate again.

### Run with Docker Compose

Copy the [`compose.yaml`](./compose.yaml), update the relevant parameters and run:
```shell
docker compose up -d
```

## 🎯 Chat Filtering

TeleWaves supports filtering which chats to monitor. This is useful if you only want to download files from specific bots or users.
By default, all chats are monitored.

### Filter Format:
- **Usernames**: `@username` or `username` (case-insensitive)
- **Chat IDs**: `12345678` (numeric chat ID)
- **Multiple**: Comma-separated values

For example:
```shell
export CHAT_FILTER="@some_bot,12345678,@friend_username"
```

## ⚙️ Configuration

TeleWaves is configured via environment variables:

| Variable            | Required | Default    | Description                                   |
|---------------------|----------|------------|-----------------------------------------------|
| `TELEGRAM_API_ID`   | ✅        | -          | Telegram API ID from my.telegram.org/apps     |
| `TELEGRAM_API_HASH` | ✅        | -          | Telegram API hash from my.telegram.org/apps   |
| `DOWNLOAD_DIR`      | ❌        | `/library` | Directory to save downloaded audio files      |
| `DATA_DIR`          | ❌        | `/data`    | Directory for application data and sessions   |
| `SESSION_NAME`      | ❌        | `session`  | Name for Telegram session file                |
| `CHAT_FILTER`       | ❌        | `""`       | Comma-separated chat IDs/usernames to monitor |

## 🔒 Security & Privacy

- **User Impersonation**: Acts as your personal Telegram account
- **Local Processing**: All processing happens on your machine/server
- **Session Encryption**: Session files are encrypted by Telegram's client library
- **No Data Transmission**: No data sent to external servers

## 📄 License

This project is provided as-is for educational and personal use. Always respect copyright laws and Telegram's Terms of Service when downloading content.

## ⚠️ Legal Disclaimer

TeleWaves acts as your personal Telegram user account. Use responsibly and in compliance with:
- Telegram's Terms of Service
- Copyright laws and intellectual property rights
- Local regulations regarding content downloading

Only download content you have permission to access. The authors are not responsible for any misuse of this software.
