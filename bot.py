#!/usr/bin/env python3
"""Telegram reminder bot — schedule reminders via chat."""
import os
import json
import asyncio
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

REMINDERS_FILE = "reminders.json"

def load_reminders() -> list:
    if os.path.exists(REMINDERS_FILE):
        with open(REMINDERS_FILE) as f:
            return json.load(f)
    return []

def save_reminders(reminders: list):
    with open(REMINDERS_FILE, "w") as f:
        json.dump(reminders, f, indent=2, default=str)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Reminder Bot\n\n"
        "Commands:\n"
        "/remind <minutes> <message> — Set a reminder\n"
        "/list — List active reminders\n"
        "/cancel <id> — Cancel a reminder"
    )

async def remind(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /remind <minutes> <message>")
        return
    
    try:
        minutes = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Minutes must be a number")
        return
    
    message = " ".join(context.args[1:])
    remind_at = datetime.now() + timedelta(minutes=minutes)
    
    reminders = load_reminders()
    reminder = {
        "id": len(reminders) + 1,
        "chat_id": update.message.chat_id,
        "message": message,
        "remind_at": remind_at.isoformat(),
        "created": datetime.now().isoformat(),
    }
    reminders.append(reminder)
    save_reminders(reminders)
    
    await update.message.reply_text(
        f"Reminder #{reminder['id']} set for {minutes} minutes: {message}"
    )

async def list_reminders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reminders = load_reminders()
    chat_reminders = [r for r in reminders if r["chat_id"] == update.message.chat_id]
    
    if not chat_reminders:
        await update.message.reply_text("No active reminders")
        return
    
    lines = []
    for r in chat_reminders:
        lines.append(f"#{r['id']}: {r['message']} (at {r['remind_at']})")
    
    await update.message.reply_text("Active reminders:\n" + "\n".join(lines))

def main():
    token = os.environ.get("TELEGRAM_TOKEN")
    if not token:
        print("Error: TELEGRAM_TOKEN not set")
        return
    
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("remind", remind))
    app.add_handler(CommandHandler("list", list_reminders))
    
    print("Bot started")
    app.run_polling()

if __name__ == "__main__":
    main()
