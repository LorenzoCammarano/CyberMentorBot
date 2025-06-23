# 🤖 CyberMentorBot

**CyberMentorBot** è un chatbot Telegram innovativo basato su **LLaMA 3** che ti aiuta a identificare e contrastare tentativi di phishing e truffe online.  
Sfrutta la potenza di un modello LLM avanzato (tramite **Groq**) per analizzare messaggi sospetti e fornire consigli pratici per migliorare la tua sicurezza informatica.

---

## 🚀 Funzionalità Principali

- **Valutazione di Messaggi Sospetti**  
  Analizza in tempo reale i messaggi che ricevi per individuare segnali di phishing o truffa.

- **Suggerimenti per Evitare Truffe Online**  
  Offre consigli educativi personalizzati per riconoscere ed evitare le minacce più comuni.

- **Risposte Generate da llama3-8b-8192 (via Groq)**  
  Utilizza un modello linguistico all'avanguardia per risposte accurate e pertinenti.

- **Webhook su HTTPS (SSL con Let's Encrypt)**  
  Garantisce una comunicazione sicura e cifrata tra Telegram e il bot.

- **Deploy tramite Docker**  
  Semplifica l'installazione e la gestione del bot in ambienti produttivi.

---

## 📸 Esempio di Interazione

👤 **Utente**:  
*Ciao, hai vinto un iPhone! Clicca qui per riceverlo: http://fakesite.ru*

🤖 **CyberMentorBot**:  
⚠️ Questo messaggio presenta caratteristiche comuni di phishing. **Non cliccare sul link!**

---

## ⚙️ Guida all'Installazione

### 1. Clona il Repository

```bash
git clone https://github.com/tuo-username/CyberMentorBot.git
cd CyberMentorBot
```

### 2. Configura il File .env
Crea un file .env nella directory principale del progetto con le seguenti variabili (sostituisci i valori segnaposto):

```bash
TELEGRAM_TOKEN=<tuo_token_telegram>
GROQ_API_KEY=<la_tua_chiave_groq>
GROQ_MODEL= llama3-8b-8192
WEBHOOK_URL=<https://tuo-dominio.it>
PORT=8443
CERT_PATH=</etc/letsencrypt/live/tuo-dominio.it/fullchain.pem>
KEY_PATH=</etc/letsencrypt/live/tuo-dominio.it/privkey.pem>
```

### 3. Costruisci l’Immagine Docker

```bash
docker build -t cybermentorbot .
```

### 4. Avvia il Bot con Docker
Assicurati che la porta 443 sia libera (ferma Apache/Nginx se necessario):

```bash

sudo systemctl stop apache2 # o nginx
```
### Avvia il bot:

```bash
docker run -d \
  --name cybermentorbot \
  -p 443:8443 \
  --env-file .env \
  -v /etc/letsencrypt:/etc/letsencrypt:ro \
  cybermentor_bot
```
## 🔒 Certificato SSL
Per abilitare il webhook di Telegram è necessaria una connessione HTTPS.

Installa e configura Certbot per ottenere un certificato SSL gratuito con Let's Encrypt:

```bash
sudo apt install certbot
sudo certbot certonly --standalone -d tuo-dominio.it
```

## 🧠 Modello AI
CyberMentorBot utilizza il modello llama3-70b-8192 fornito tramite le Groq API.
Ogni messaggio viene analizzato in tempo reale tramite un prompt ingegnerizzato per identificare phishing, truffe e altre minacce comuni.

## 🧪 Test
Per testare il bot, invia dalla tua chat Telegram messaggi sospetti come:

```bash
Hai vinto un premio! Clicca qui: http://badlink.ru
Il bot analizzerà il contenuto e ti fornirà una risposta dettagliata.
```

## ▶️​ Se vuoi testare il mio bot → [CyberMentorBot](https://t.me/Your_CyberMentor_Bot)

## ✨ Autore
### 🔗 Lorenzo Cammarano → [info.lorenzocammarano.me](https://info.lorenzocammarano.me)
