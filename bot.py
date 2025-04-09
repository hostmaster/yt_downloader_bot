import logging
import os
import subprocess

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Load environment variables
load_dotenv()

# Disable httpx and httpcore logging completely
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Create downloads directory if it doesn't exist
os.makedirs("downloads", exist_ok=True)

# Get allowed user IDs from environment variable
ALLOWED_USER_IDS = [
    int(user_id.strip())
    for user_id in os.getenv("ALLOWED_USER_IDS", "").split(",")
    if user_id.strip()
]

# YouTube URL pattern
YOUTUBE_URL_PATTERN = r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+"


def is_user_allowed(user_id: int) -> bool:
    """Check if the user is allowed to use the bot."""
    return user_id in ALLOWED_USER_IDS


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    if not is_user_allowed(update.effective_user.id):
        await update.message.reply_text(
            "Sorry, you are not authorized to use this bot."
        )
        return

    await update.message.reply_text(
        "Hi! Send me a YouTube URL and I will download it for you."
    )


async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Download the video from the provided YouTube URL."""
    if not is_user_allowed(update.effective_user.id):
        await update.message.reply_text(
            "Sorry, you are not authorized to use this bot."
        )
        return

    url = update.message.text
    chat_id = update.message.chat_id

    # Send initial message
    message = await update.message.reply_text("Downloading video...")

    try:
        # Download video using yt-dlp command
        output_path = os.path.join("downloads", "%(title)s.%(ext)s")
        cmd = ["yt-dlp", "-o", output_path, url]

        # Execute the command
        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            raise Exception(f"yt-dlp error: {stderr}")

        # Find the downloaded file
        files = os.listdir("downloads")
        if not files:
            raise Exception("No files were downloaded")

        # Get the most recently downloaded file
        latest_file = max(
            files, key=lambda x: os.path.getctime(os.path.join("downloads", x))
        )
        file_path = os.path.join("downloads", latest_file)

        # Send the video file
        await update.message.reply_video(
            video=open(file_path, "rb"), supports_streaming=True
        )

        # Clean up
        os.remove(file_path)
        await message.edit_text("Video downloaded successfully!")

    except Exception as e:
        logging.error(f"Error downloading video: {e}")
        await message.edit_text("Sorry, there was an error downloading the video.")


def main():
    """Start the bot."""
    # Create the Application and pass it your bot's token
    application = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(filters.Regex(YOUTUBE_URL_PATTERN), download_video)
    )

    # Start the Bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
