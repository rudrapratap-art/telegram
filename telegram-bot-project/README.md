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

Deploy to Render (Docker)

1. Ensure repo on GitHub contains Dockerfile, src/bot.py, requirements.txt.
2. In Render dashboard -> New -> Web Service
   - Connect GitHub repo
   - Environment: Docker
   - Dockerfile path: Dockerfile
3. In Environment settings add SECRET:
   - TELEGRAM_BOT_TOKEN = <your bot token>
4. Deploy. Monitor logs in Render to confirm startup.

Notes:
- Do NOT commit cookies.txt or .env. Use Render secrets for tokens.
- If some reels are private, provide cookies via secure mechanism outside the repo.