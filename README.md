# Pulse — Python Automation Bot

A daily summary bot that runs itself every morning via GitHub Actions. Built for Zero2Dev Session 03.

## What it does

Pulse fetches live weather and a motivational quote, formats them into a clean summary, and saves it as a downloadable file — all automatically at 8 AM IST every day.

## Project structure

```
folio/
├── bot.py                    # Main Pulse bot
├── requirements.txt          # Dependencies
├── projects.json             # Auto-generated from GitHub API
├── supplementary/
│   ├── weather_alert.py      # Task 1: OpenWeatherMap alert
│   ├── news_digest.py        # Task 2: Morning news email
│   └── update_projects.py    # Task 3: GitHub repos → portfolio
└── .github/workflows/
    ├── daily.yml             # Runs Pulse at 8 AM IST
    ├── weather_alert.yml     # Runs weather check at 8 AM IST
    ├── news_digest.yml       # Runs news digest at 7 AM IST
    └── update_projects.yml   # Runs on every push to main
```

## Running locally

```bash
pip install -r requirements.txt
python bot.py
```

## GitHub Secrets needed

| Secret | Used by |
|--------|---------|
| `OWM_API_KEY` | Weather alert (OpenWeatherMap) |
| `EMAIL_SENDER` | All email tasks |
| `EMAIL_PASSWORD` | All email tasks (Gmail App Password) |
| `EMAIL_RECEIVER` | All email tasks |
| `GITHUB_USERNAME` | Update projects task |

## Case study

**Problem:** Wanted a daily briefing without doing anything manually each morning.

**Approach:** A Python bot with four functions pulling two free APIs, scheduled on GitHub Actions.

**Craft:** Graceful try/except on every API call, secrets handled the right way, downloadable artifact.

**Outcome:** Runs autonomously at 8 AM IST, every day, for free.
