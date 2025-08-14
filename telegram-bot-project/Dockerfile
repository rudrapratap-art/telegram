FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# If your project files live in repo subfolder "telegram-bot-project", copy from there:
COPY telegram-bot-project/requirements.txt   # <-- adjust path if needed
RUN pip install --no-cache-dir -r requirements.txt

COPY telegram-bot-project/src/ /app/src/           # <-- adjust path if needed
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

CMD ["python", "src/bot.py"]
