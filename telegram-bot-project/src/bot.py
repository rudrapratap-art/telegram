import os
import sys
import subprocess
import logging
import requests
import threading
import http.server
import socketserver
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Config
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
COOKIES_FILE = "cookies.txt"
YT_DLP_TIMEOUT = int(os.getenv("YT_DLP_TIMEOUT", "60"))
HEALTH_PORT = int(os.getenv("PORT", "8080"))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if not BOT_TOKEN:
    raise SystemExit("Set TELEGRAM_BOT_TOKEN environment variable")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📥 Send me an Instagram reel link and I’ll get you the download link.")

async def download_instagram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()
    if not text or "instagram.com" not in text:
        await update.message.reply_text("❌ Please send a valid Instagram link.")
        return

    url = text.split()[0]
    await update.message.reply_text("⏳ Fetching download link... please wait.")

    try:
        cmd = [sys.executable, "-m", "yt_dlp"]
        if os.path.isfile(COOKIES_FILE):
            cmd += ["--cookies", COOKIES_FILE]
        cmd += ["-g", "-f", "mp4", url]

        logger.info("Running: %s", " ".join(cmd))
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=YT_DLP_TIMEOUT)

        if result.returncode != 0:
            stderr = (result.stderr or "").strip()
            logger.error("yt-dlp failed: %s", stderr)
            await update.message.reply_text(
                f"❌ yt-dlp error:\n{stderr or 'Unknown error'}\n\nTip: if the reel is private, add a cookies.txt file (do NOT commit it)."
            )
            return

        lines = [ln.strip() for ln in (result.stdout or "").splitlines() if ln.strip()]
        if not lines:
            await update.message.reply_text("❌ yt-dlp returned no link.")
            return

        download_link = lines[0]
        await update.message.reply_text(f"✅ Download Link:\n{download_link}")

    except subprocess.TimeoutExpired:
        logger.exception("yt-dlp timeout")
        await update.message.reply_text("❌ Error: Timed out while fetching the link.")
    except Exception as e:
        logger.exception("Unexpected error")
        await update.message.reply_text(f"❌ Unexpected error: {e}")

# Health endpoint so Render web service detects a bound port
def _start_health_server():
    class _Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path in ("/", "/health"):
                self.send_response(200)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(b"OK")
            else:
                self.send_response(404)
                self.end_headers()
        def log_message(self, format, *args):
            return

    try:
        socketserver.TCPServer.allow_reuse_address = True
        with socketserver.TCPServer(("", HEALTH_PORT), _Handler) as httpd:
            logger.info("Health server listening on port %s", HEALTH_PORT)
            httpd.serve_forever()
    except Exception:
        logger.exception("Health server failed to start")

if __name__ == "__main__":
    # start health server thread so Render detects an open port
    t = threading.Thread(target=_start_health_server, daemon=True)
    t.start()

    # remove any existing webhook so polling can start without conflict
    try:
        requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook", timeout=10)
    except Exception:
        logger.exception("Failed to delete webhook (continuing)")

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_instagram))

    logger.info("🚀 Bot is running...")
    app.run_polling()
