FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# copy requirements and install (project is in telegram-bot-project/)
COPY telegram-bot-project/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# copy source
COPY telegram-bot-project/src/ /app/src/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

CMD ["python", "src/bot.py"]
