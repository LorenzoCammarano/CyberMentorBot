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
OVH_API_URL = os.getenv("OVH_API_URL")  # URL dell'API OVH (definito nel file .env)
OVH_API_KEY = os.getenv("OVH_API_KEY")  # La tua chiave API OVH (definito nel file .env)

if not TOKEN or not WEBHOOK_URL or not OVH_API_URL or not OVH_API_KEY:
    raise EnvironmentError("BOT_TOKEN, WEBHOOK_URL, OVH_API_URL o OVH_API_KEY mancante nel file .env")

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

        # Analisi del testo tramite l'API OVH
        result = analizza_testo_utente_con_ovh(text)
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

# ─────── ANALISI TESTO CON API OVH ────────────────────────

def analizza_testo_utente_con_ovh(testo):
    # Esegui una richiesta POST all'API OVH per l'analisi del testo
    payload = {
        'text': testo,  # Passa il testo dell'utente
        'api_key': OVH_API_KEY  # La chiave dell'API OVH
    }

    headers = {
        'Content-Type': 'application/json',  # Definisci il tipo di contenuto come JSON
    }

    # Richiesta POST all'API di OVH
    response = requests.post(OVH_API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        result = response.json()
        rischio = result.get("rischio", "basso")
        commento = result.get("commento", "✅ Nessun rischio rilevato.")
    else:
        rischio = "errore"
        commento = "⚠️ Errore durante l'analisi del testo."

    return {
        "rischio": rischio,
        "commento": commento
    }

# ─────── AVVIO ──────────────────────────────────────────

if __name__ == "__main__":
    set_webhook()
    context = (
        "/etc/letsencrypt/live/info.lorenzocammarano.me/fullchain.pem",
        "/etc/letsencrypt/live/info.lorenzocammarano.me/privkey.pem",
    )
    app.run(host="0.0.0.0", port=9443, ssl_context=context)

