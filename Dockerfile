# Usa immagine Python slim compatibile (3.11)
FROM python:3.11-slim

# Setta la working directory
WORKDIR /app

# Aggiorna apt e installa dipendenze di sistema per SSL e build
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    libssl-dev \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copia i file requirements
COPY requirements.txt .

# Installa i pacchetti Python necessari
RUN pip install --no-cache-dir -r requirements.txt

# Copia il resto del progetto
COPY . .

# Esponi la porta 8443 (per Flask HTTPS)
EXPOSE 8443

# Comando di avvio
CMD ["python", "main.py"]
