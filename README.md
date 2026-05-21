# Telegram Reminder Bot

A simple Telegram bot for scheduling reminders.

## Features
- `/remind <minutes> <message>` — Set a reminder
- `/list` — View active reminders
- `/cancel <id>` — Cancel a reminder
- Persists reminders to JSON file

## Setup
1. Create bot via @BotFather
2. Set `TELEGRAM_TOKEN` environment variable
3. `pip install -r requirements.txt`
4. `python bot.py`

## Stack
- Python 3.10+
- python-telegram-bot v20
