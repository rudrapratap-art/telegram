# Instagram Reel downloader Telegram bot

Deploy: GitHub → Render (Docker)

Requirements
- Python 3.11
- TELEGRAM_BOT_TOKEN set as env var in Render

Quick local
1. Create venv, install deps:
   .\.venv\Scripts\Activate.ps1
   .\.venv\Scripts\pip install -r requirements.txt

2. Run:
   .\.venv\Scripts\python.exe src\bot.py

Deploy to Render (summary)
- Push repo to GitHub.
- Create a Render service (Docker).
- Set TELEGRAM_BOT_TOKEN in Render's environment settings.
- Deploy.