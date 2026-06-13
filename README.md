# \# Pulse - Daily Summary Bot

# 

# A Python bot that fetches live weather and a motivational quote every morning and saves it as a summary file. Runs automatically at 8 AM IST via GitHub Actions.

# 

# \## How it works

# \- Fetches weather from wttr.in

# \- Fetches a random quote from ZenQuotes

# \- Saves everything into daily\_summary.txt

# \- Runs on its own every day using GitHub Actions cron

# 

# \## How to run locally

# pip install requests

# python bot.py

# 

# \## Supplementary tasks

# \- weather\_alert.py — checks OpenWeatherMap, sends email if temp > 35C or rain

# \- news\_digest.py — scrapes 3 news sites and sends an HTML email every morning

# \- update\_projects.py — fetches GitHub repos and generates projects.json for portfolio

