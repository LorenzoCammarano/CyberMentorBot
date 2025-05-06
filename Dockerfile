# Usa un'immagine Python leggera
FROM python:3.13-slim

# Imposta variabili d'ambiente per evitare prompt interattivi e problemi con encoding
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Crea e imposta la directory di lavoro
WORKDIR /app/bot

# Copia i requirements e installa le dipendenze
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copia l'intero contenuto del progetto
COPY . /app/

# Espone la porta per Flask
EXPOSE 9443

# Avvia l'applicazione dal modulo corretto
CMD ["python", "main.py"]
