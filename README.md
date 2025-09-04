<div align="center">
  
# 🤖 CyberMentorBot

</div>

<p align="center">
  <img src="assets/CyberMentorBot.png" alt="CyberMentorBot banner" width="400"/>
</p>

**CyberMentorBot** is an advanced Telegram chatbot designed to help you identify and counter **phishing**, **online scams**, and other **cyber threats**.  
Powered by the **LLaMA 3** model via **Groq API**, it analyzes suspicious messages in real-time and provides clear, safe, and immediate responses.

---

### 🗝️ Key Features

- 🔍 **Real-Time Message Analysis**  
  Detects suspicious content such as deceptive links, fake offers, or fraudulent requests.

- 🛡️ **Personalized Security Advice**  
  Guides you in recognizing common scam patterns with educational explanations.

- 🧠 **AI Powered by LLaMA 3 (Groq)**  
  Uses `llama3-8b-8192` to provide reliable and up-to-date responses.

- 🔐 **Secure Webhook via HTTPS (SSL)**  
  Encrypted communication between Telegram and the bot using a Let's Encrypt certificate.

- 🐳 **Simplified Docker Deployment**  
  Launch the bot in just a few commands, ready for production environments.

---

### ⚙️ Installation Guide

#### 1. Clone the Repository

```bash
git clone https://github.com/your-username/CyberMentorBot.git
cd CyberMentorBot
```

<br>

#### 2. Create the .env File
Create a .env file in the project root with the following configuration:

<br>

```bash
# Telegram Bot Token
BOT_TOKEN=<your_telegram_bot_token>

# LLM Provider API Key (e.g., Groq)
GROQ_API_KEY=<your_groq_api_key>

# Public Webhook URL (HTTPS, accessible by Telegram)
WEBHOOK_URL=<your_public_https_webhook_url>

# SSL certificate paths used inside the container
SSL_CERT_PATH=/path/to/ssl_certificate_inside_container
SSL_KEY_PATH=/path/to/ssl_key_inside_container

# SSL certificate paths on the host system (used by Python bot)
CERT_PATH=<path_to_ssl_certificate_on_host>
KEY_PATH=<path_to_ssl_key_on_host>
```

<br>

---

#### ⚠️ Make sure your domain points to the server and is configured with HTTPS 🔐.

---

<br>

####  3. Build the Docker Image
```bash
docker build -t cybermentorbot .
```

<br>

#### 4. Run the Bot
Ensure port 443 is free (stop Apache/Nginx if necessary):

```bash
sudo systemctl stop apache2 nginx
```

Then start the container:

```bash
docker run -d \
  --name cybermentorbot \
  -p 443:8443 \
  --env-file .env \
  -v /etc/letsencrypt:/etc/letsencrypt:ro \
  cybermentorbot
```

<br>

#### 🔐 SSL Certificates (Let's Encrypt)
A valid HTTPS certificate is required for Telegram webhook.
You can generate one with Certbot:

```bash
sudo apt install certbot
sudo certbot certonly --standalone -d your-domain.com
```

The files will be saved in `/etc/letsencrypt/live/your-domain.com/`

<br>

---

### 🧠 AI Model Details
CyberMentorBot uses the LLaMA 3 model (`llama3-8b-8192`) via Groq API. Each message is processed in real-time with a specialized prompt to identify malicious behaviors such as:

<ul>
  <li>Phishing</li>
  <li>Suspicious links</li>
  <li>Bank fraud</li>
  <li>Scam schemes</li>
</ul>

<br>

---

### 🧪 Bot Testing
You can test the bot directly on Telegram by sending a message like:

<pre> You won a prize! Enter your details here: http://badlink.ru
The bot will analyze the text and respond with an assessment.</pre>

<br>

---

### 🖥️ Available Commands

| **Command**   | **Description**                                    |
|-----------|------------------------------------------------|
| ``` /start ```    | Start a conversation with the bot             |
| ``` /help```     | Show instructions and tips                    |
| ``` <text>```    | Any message will be automatically analyzed   |


<br>

---

### ❇️ Try My Bot ⤵️
🤖 CyberMentorBot 🔗 [Your_CyberMentor_Bot](https://t.me/Your_CyberMentor_Bot)

<br>

---

### 👨‍💻 Author  
🔹Lorenzo Cammarano 🔗 [info.lorenzocammarano.me](https://lorenzocammarano.me/)

