# YouTube Video Downloader Telegram Bot

A Telegram bot that downloads YouTube videos and sends them back to users.

## Features

- Downloads YouTube videos using yt-dlp
- Sends the downloaded video back to the user
- Supports both youtube.com and youtu.be links
- Automatic cleanup of downloaded files
- User access control
- Docker support with persistent volumes
- Task automation with Taskfile

## Setup

### Local Setup

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your configuration:
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   ALLOWED_USER_IDS=123456789,987654321
   ```

### Docker Setup

1. Build and run using Docker Compose:
   ```bash
   docker-compose up -d
   ```

2. Or pull and run the latest image from GitHub Container Registry:
   ```bash
   docker pull ghcr.io/your-username/yt_downloader_bot:latest
   docker run -d \
     --name youtube-downloader-bot \
     --env-file .env \
     -v youtube-downloader-downloads:/app/downloads \
     ghcr.io/your-username/yt_downloader_bot:latest
   ```

### Taskfile Automation

This project uses [Taskfile](https://taskfile.dev/) for automation. Install Taskfile first:

```bash
# macOS
brew install go-task/tap/go-task

# Linux
sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b /usr/local/bin
```

Available tasks:
```bash
task --list-all
```

Common tasks:
```bash
# Build the Docker image locally
task build

# Run the container locally
task run

# Push the image to GitHub Container Registry
task push

# Manage Docker Compose services
task compose -- up -d    # Start services
task compose -- down     # Stop services
task compose -- logs     # View logs
task compose -- ps       # List services

# Clean up Docker resources (including volumes)
task clean

# Run the complete workflow (build, push, and start)
task all
```

To use the push task, set these environment variables:
```bash
export GITHUB_USERNAME=your-username
export GITHUB_TOKEN=your-github-token
export GITHUB_REPOSITORY=your-username/yt_downloader_bot
```

## Usage

1. Start the bot:
   ```bash
   # Development
   python bot.py
   # or
   docker-compose up -d
   # or
   task compose -- up -d
   ```

2. In Telegram, send the `/start` command to the bot
3. Send any YouTube video link to the bot
4. The bot will download the video and send it back to you

## Notes

- The bot downloads videos in the best available quality
- Downloaded files are automatically deleted after being sent
- Make sure you have enough disk space for video downloads
- Only users listed in ALLOWED_USER_IDS can use the bot
- Downloads are stored in a Docker volume named `youtube-downloader-downloads`

## Docker Image

The Docker image is automatically built and pushed to GitHub Container Registry on every push to the main branch.

To use the image:
1. Pull the latest version:
   ```bash
   docker pull ghcr.io/your-username/yt_downloader_bot:latest
   ```

2. Or use a specific version:
   ```bash
   docker pull ghcr.io/your-username/yt_downloader_bot:sha-xxxxxxx
   ```

## Development

### Building the Docker Image

```bash
# Using Docker directly
docker build -t yt_downloader_bot .

# Using Taskfile
task build
```

### Running Tests

```bash
# Using Docker Compose directly
docker-compose up -d

# Using Taskfile
task compose -- up -d
```

### Managing Docker Volumes

To manage the downloads volume:
```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect youtube-downloader-downloads

# Remove volume
docker volume rm youtube-downloader-downloads
```

## License

MIT