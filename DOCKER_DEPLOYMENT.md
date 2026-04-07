# Docker Deployment Guide

## Recommended Setup

Voor deze app is dit de meest stabiele setup:

- Proxmox VM
- Debian 12 of Ubuntu 24.04
- Docker + Docker Compose plugin
- Deze repo als bind-mounted compose project

Waarom:

- Playwright + Chromium draait voorspelbaar in een normale Docker setup
- minder gezeik dan Docker-in-LXC
- updates en rollback zijn simpel

---

## One-Time Host Setup

### 1. Maak een kleine VM

Prima start:

- 2 vCPU
- 2 GB RAM
- 10-20 GB disk
- timezone op `Europe/Amsterdam`

### 2. Installeer Docker

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker
docker --version
docker compose version
```

### 3. Clone de repo

```bash
cd /opt
sudo git clone https://github.com/AlvaroHG1/rooster_automation.git
sudo chown -R $USER:$USER /opt/rooster_automation
cd /opt/rooster_automation
```

### 4. Zet config en secrets klaar

```bash
cp .env.example .env
mkdir -p logs shared
nano .env
```

Minimaal nodig:

```env
ROI_EMAIL=your_email
ROI_PASSWORD=your_password
GMAIL_ADDRESS=your_gmail@gmail.com
GMAIL_APP_PASSWORD=your_gmail_app_password
TRIGGER_EMAIL_SENDER=noreply@staff.nl
CALDAV_URL=https://caldav.icloud.com
CALDAV_USERNAME=your_apple_id@icloud.com
CALDAV_PASSWORD=your_icloud_app_password
CALDAV_CALENDAR_NAME=Rooster
```

Gmail setup:

1. Zet 2FA aan op je Google account
2. Maak een app password aan
3. Zorg dat IMAP aan staat in Gmail
4. Zet dat wachtwoord in `GMAIL_APP_PASSWORD`

### 5. Eerste deploy

```bash
docker compose build
docker compose up -d
docker compose ps
docker compose logs --tail=100 rooster-automation
```

---

## Normal Update Routine

Dit is de standaard routine als je nieuwe code naar `main` hebt gemerged.

```bash
cd /opt/rooster_automation
git fetch origin
git checkout main
git pull --ff-only origin main
docker compose up -d --build
docker compose ps
docker compose logs --tail=100 rooster-automation
```

Als de app gezond lijkt:

- container staat `Up`
- logs tonen geen auth/browser/crash loop

---

## Safe Update Routine

Als je iets netter wilt werken:

```bash
cd /opt/rooster_automation
cp .env .env.bak
cp config/config.yaml config/config.yaml.bak
git fetch origin
git checkout main
git pull --ff-only origin main
docker compose build --pull
docker compose up -d
docker compose ps
docker compose logs --tail=150 rooster-automation
```

Extra netjes op Proxmox:

- maak eerst een VM snapshot
- update daarna pas de app

---

## Health Checks

Gebruik deze na deploy of update:

```bash
cd /opt/rooster_automation
docker compose ps
docker compose logs --tail=200 rooster-automation
docker inspect --format='{{.State.Status}} {{.State.Restarting}}' rooster-automation
```

Waar je op let:

- geen restart loop
- geen `AUTHENTICATIONFAILED`
- geen Playwright browser startup errors
- geen CalDAV auth errors

---

## Rollback Routine

Als een update kapot is:

```bash
cd /opt/rooster_automation
git log --oneline -5
git checkout <laatste-goede-commit>
docker compose up -d --build
docker compose ps
docker compose logs --tail=150 rooster-automation
```

Daarna fix je `main` later pas. Eerst weer werkend krijgen.

Als je met Proxmox snapshots werkt is dit nog simpeler:

1. stop met prutsen
2. revert de VM snapshot
3. check logs

---

## Day-to-Day Commands

Logs volgen:

```bash
cd /opt/rooster_automation
docker compose logs -f rooster-automation
```

Container herstarten:

```bash
cd /opt/rooster_automation
docker compose restart rooster-automation
```

Container stoppen:

```bash
cd /opt/rooster_automation
docker compose down
```

Opnieuw starten:

```bash
cd /opt/rooster_automation
docker compose up -d
```

---

## Practical Rules

- edit secrets alleen in `.env`
- edit scraper ids alleen in `config/config.yaml`
- deploy alleen vanaf `main`
- gebruik `git pull --ff-only` zodat je VM geen rare merge commits maakt
- maak bij risicovolle updates eerst een Proxmox snapshot
- check na elke update direct de logs

---

## Minimal Routine

Als je gewoon de korte versie wilt:

### Eerste keer

```bash
cd /opt
git clone https://github.com/AlvaroHG1/rooster_automation.git
cd rooster_automation
cp .env.example .env
mkdir -p logs shared
docker compose up -d --build
docker compose logs --tail=100 rooster-automation
```

### Elke update

```bash
cd /opt/rooster_automation
git pull --ff-only origin main
docker compose up -d --build
docker compose logs --tail=100 rooster-automation
```
