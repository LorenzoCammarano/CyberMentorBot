#!/usr/bin/env python

import os
import logging
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# ─────── SETUP ──────────────────────────────────────────

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not TOKEN or not WEBHOOK_URL or not GROQ_API_KEY:
    raise EnvironmentError("Variabili d'ambiente BOT_TOKEN, WEBHOOK_URL o GROQ_API_KEY mancanti")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# ─────── FUNZIONE DI ANALISI AI ─────────────────────────

def analizza_testo_con_groq(testo):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {
                "role": "system",
                "content": (
                    "Sei un esperto di sicurezza informatica. Valuta il messaggio utente "
                    "e spiega se può essere una truffa, phishing, o contenere rischi."
                )
            },
            {
                "role": "user",
                "content": testo
            }
        ],
        "temperature": 0.7
    }

    try:
        r = requests.post(url, headers=headers, json=data)
        r.raise_for_status()
        content = r.json()["choices"][0]["message"]["content"].strip()
        return content
    except Exception as e:
        logger.error(f"Errore richiesta Groq: {e}")
        return "⚠️ Errore durante la generazione della risposta."

# ─────── HANDLER TELEGRAM ──────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_html(
        rf"👋 Ciao {user.mention_html()}! Inviami un messaggio sospetto e ti dirò se può essere rischioso."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Inviami un messaggio (es. email sospetta o link) e ti dirò se c'è qualcosa di strano."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat_id = update.message.chat.id
    logger.info(f"Messaggio da chat_id={chat_id}: {text}")

    result = analizza_testo_con_groq(text)
    logger.info(f"Risposta AI: {result}")

    response = f"Messaggio ricevuto:\n{text}\n\n🧠 Risposta AI:\n{result}"
    await context.bot.send_message(chat_id=chat_id, text=response)

# ─────── AVVIO APPLICAZIONE ────────────────────────────

if __name__ == "__main__":
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_webhook(
        listen="0.0.0.0",
        port=8443,
        webhook_url=WEBHOOK_URL,
        cert="/path/to/your/fullchain.pem",
        key="/path/to/your/privkey.pem"
    )
