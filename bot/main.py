#!/usr/bin/env python

import os
import logging
import requests
from dotenv import load_dotenv
from flask import Flask, request
from telegram import Update, Bot
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
    raise EnvironmentError("BOT_TOKEN, WEBHOOK_URL o GROQ_API_KEY mancante nel file .env")

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=TOKEN)
app = Flask(__name__)

# ─────── ENDPOINT TELEGRAM (WEBHOOK) ───────────────────

@app.route("/", methods=["POST"])
def webhook_handler():
    update = Update.de_json(request.get_json(force=True), bot)

    if update.message:
        text = update.message.text
        chat_id = update.message.chat_id

        # Analisi del testo tramite Groq AI
        result = analizza_testo_con_groq(text)
        response = f"Messaggio ricevuto:\n{text}\n\n🧠 Risposta AI:\n{result}"

        bot.send_message(chat_id=chat_id, text=response)

    return "OK", 200

# ─────── WEBHOOK SETUP ──────────────────────────────────

def set_webhook():
    response = requests.get(f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={WEBHOOK_URL}")
    print("Webhook response:", response.json())

# ─────── COMANDI BOT ────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_html(
        rf"Ciao {user.mention_html()}! Sono CyberMentor 🤖\nScrivimi un messaggio sospetto e ti aiuterò a valutarlo.",
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Inviami un messaggio (es. email sospetta o link) e ti dirò se c'è qualcosa di strano.")

# ─────── AI RISPOSTA CON GROQ ───────────────────────────

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
                "content": "Sei un esperto di sicurezza informatica. Valuta il messaggio utente e spiega se può essere phishing, scam, o se è sicuro."
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
        return r.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        logger.error(f"Errore richiesta Groq: {e}")
        return "⚠️ Errore durante la generazione della risposta."

# ─────── AVVIO ──────────────────────────────────────────

if __name__ == "__main__":
    set_webhook()
    context = (
        "/etc/letsencrypt/live/info.lorenzocammarano.me/fullchain.pem",
        "/etc/letsencrypt/live/info.lorenzocammarano.me/privkey.pem",
    )
    app.run(host="0.0.0.0", port=8443, ssl_context=context)
