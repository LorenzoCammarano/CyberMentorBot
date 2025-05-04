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

if not TOKEN or not WEBHOOK_URL:
    raise EnvironmentError("BOT_TOKEN o WEBHOOK_URL mancante nel file .env")

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

        # Placeholder per analisi IA (es. rischio phishing)
        result = analizza_testo_utente(text)
        response = f"Messaggio ricevuto: {text}\n🧠 Rilevamento: {result['commento']}"

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
        rf"Ciao {user.mention_html()}! Sono CyberMentor 🤖\nInviami un messaggio e ti dirò se è sicuro!",
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Scrivimi un messaggio sospetto e ti dirò se fidarti o meno.")

# ─────── ANALISI TESTO (IA MOCK) ────────────────────────

def analizza_testo_utente(testo):
    # TODO: sostituire con chiamata API OVH
    parole_sospette = ["clicca", "password", "vinto", "conferma", "pagamento"]
    rischio = any(word in testo.lower() for word in parole_sospette)

    return {
        "rischio": "alto" if rischio else "basso",
        "commento": "⚠️ Attenzione: potenziale rischio." if rischio else "✅ Nessun rischio rilevato."
    }

# ─────── AVVIO ──────────────────────────────────────────

if __name__ == "__main__":
    set_webhook()
    context = ('/certs/cert.pem', '/certs/key.pem')  # Percorso nel container
    app.run(host="0.0.0.0", port=443, ssl_context=context)

