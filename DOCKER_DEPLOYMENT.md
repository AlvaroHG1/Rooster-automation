# Docker Deployment Guide

## Voordelen van Docker

- ✅ **Portable**: Werkt op elke VM (Linux/Windows/Mac)
- ✅ **Geïsoleerd**: Geen conflicten met andere software
- ✅ **Auto-restart**: Container herstart automatisch na crash/reboot
- ✅ **Reproducible**: Altijd dezelfde environment
- ✅ **Easy updates**: `docker-compose pull && docker-compose up -d`

## Quick Start

### 1. Installeer Docker

**Linux (Ubuntu/Debian):**

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

**Windows/Mac:**
Download Docker Desktop van https://www.docker.com/products/docker-desktop

### 2. Clone Repository

```bash
git clone <repository-url>
cd rooster_automation
```

### 3. Configureer Environment

```bash
cp .env.example .env
nano .env  # Of gebruik je favoriete editor
```

Vul in:

```env
ROI_EMAIL=jouw_email
ROI_PASSWORD=jouw_wachtwoord

GMAIL_ADDRESS=jouw_email
GMAIL_APP_PASSWORD=jouw_gmail_app_password

# Wordt automatisch /app/shared in container
SHARED_FOLDER_PATH=/app/shared

TRIGGER_EMAIL_SENDER=noreply@staff.nl
```

### 3b. Gmail IMAP Setup

De app gebruikt Gmail via IMAP. Je hebt dus geen extra OAuth-bestanden nodig.

1. Zet 2-factor authentication aan op je Google account
2. Genereer een Gmail app password
3. Zet IMAP aan in Gmail settings
4. Vul dat app password in bij `GMAIL_APP_PASSWORD`
5. `./config` bevat alleen app-config zoals `config.yaml`

### 4. Start Container

```bash
docker-compose up -d
```

### 5. Bekijk Logs

```bash
docker-compose logs -f
```

