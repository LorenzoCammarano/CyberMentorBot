# 🤖 CyberMentorBot

<p align="center">
  <img src="assets/CyberMentorBot.png" alt="CyberMentorBot banner" width="400"/>
</p>


**CyberMentorBot** è un chatbot Telegram avanzato, progettato per aiutarti a identificare e contrastare tentativi di **phishing**, **truffe online**, e altre **minacce informatiche**.  
Grazie alla potenza del modello **LLaMA 3** tramite **Groq API**, analizza in tempo reale i messaggi sospetti che ricevi e ti fornisce risposte chiare, sicure e immediate.

---

## 🚀 Funzionalità Principali

- 🔍 **Analisi dei Messaggi in Tempo Reale**  
  Rileva contenuti sospetti come link ingannevoli, offerte false o richieste fraudolente.

- 🛡️ **Consigli di Sicurezza Personalizzati**  
  Ti guida nel riconoscere schemi comuni di truffa con spiegazioni educative.

- 🧠 **Intelligenza Artificiale via LLaMA 3 (Groq)**  
  Usa `llama3-8b-8192` per offrire risposte affidabili e aggiornate.

- 🔐 **Webhook Sicuro via HTTPS (SSL)**  
  Comunicazione cifrata tra Telegram e il bot con certificato Let's Encrypt.

- 🐳 **Deploy Semplificato con Docker**  
  Avvio del bot in pochi comandi, pronto per ambienti di produzione.

---

## ⚙️ Guida all’Installazione

### 1. Clona il Repository

```bash
git clone https://github.com/tuo-username/CyberMentorBot.git
cd CyberMentorBot
```

### 2. Crea il file .env
Crea un file .env nella root del progetto e configura così:
```bash
# Token del bot Telegram
BOT_TOKEN=<your_telegram_bot_token>

# Chiave API del provider LLM (es. Groq)
GROQ_API_KEY=<your_groq_api_key>

# URL pubblico del webhook (HTTPS, accessibile da Telegram)
WEBHOOK_URL=<your_public_https_webhook_url>

# Percorsi ai certificati SSL usati all'interno del container
SSL_CERT_PATH=/path/to/ssl_certificate_inside_container
SSL_KEY_PATH=/path/to/ssl_key_inside_container

# Percorsi ai certificati SSL sul sistema host (usati dal bot Python)
CERT_PATH=<path_to_ssl_certificate_on_host>
KEY_PATH=<path_to_ssl_key_on_host>
```

### 🔐 Assicurati che il tuo dominio punti al server ed è configurato con HTTPS.

### 3. Costruisci l’Immagine Docker
```bash
docker build -t cybermentorbot .
```

### 5. Avvia il Bot
Assicurati che la porta 443 sia libera (ferma Apache/Nginx se necessario):

```bash
sudo systemctl stop apache2 nginx
```

#### E poi avvia il container:

```bash
docker run -d \
  --name cybermentorbot \
  -p 443:8443 \
  --env-file .env \
  -v /etc/letsencrypt:/etc/letsencrypt:ro \
  cybermentorbot
```

## 🔐 Certificati SSL (Let's Encrypt)
Per far funzionare il webhook di Telegram, è necessario un certificato HTTPS valido.
Puoi generarne uno con Certbot:

```bash
sudo apt install certbot
sudo certbot certonly --standalone -d tuo-dominio.it
```

I file verranno salvati in /etc/letsencrypt/live/tuo-dominio.it/

## 🧠 Dettagli sul Modello AI
CyberMentorBot si basa sul modello LLaMA 3 (llama3-8b-8192), fornito tramite Groq API.
Ogni messaggio inviato viene processato in tempo reale da un prompt specializzato per identificare comportamenti malevoli come:

<ul>
  <li>Phishing</li>
  <li>Link sospetti</li>
  <li>Frodi bancarie</li>
  <li>Schemi di truffa</li>
</ul>

## 🧪 Test del Bot
Puoi testare il bot direttamente da Telegram inviando un messaggio come:

<pre> Hai vinto un premio! Inserisci i tuoi dati qui: http://badlink.ru
Il bot analizzerà il testo e risponderà con una valutazione.</pre>

## 🧰 Comandi Disponibili

<pre> Comando	Descrizione
/start → Inizia la conversazione con il bot
/help → Mostra le istruzioni e suggerimenti
testo → Qualsiasi messaggio verrà analizzato in automatico </pre>

## ▶️ Prova il mio Bot
👉 CyberMentorBot 🔗 [Your_CyberMentor_Bot](https://t.me/Your_CyberMentor_Bot)

## 👨‍💻 Autore  
Lorenzo Cammarano 🔗 [info.lorenzocammarano.me](https://lorenzocammarano.me/)



