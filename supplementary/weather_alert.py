# weather_alert.py
# Fetches weather from OpenWeatherMap for your city.
# If temperature > 35C or rain is predicted, sends an email alert.
# Runs via GitHub Actions on a schedule.

import requests
import smtplib
import os
from email.mime.text import MIMEText
from datetime import datetime

CITY = "Thiruvananthapuram"

def get_weather():
    """Fetch current weather data from OpenWeatherMap."""
    api_key = os.environ.get("OWM_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={api_key}&units=metric"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Could not fetch weather: {e}")
        return None

def check_alert(data):
    """Check if temp > 35C or rain is in the forecast."""
    if not data:
        return False, "Weather data unavailable"

    temp = data["main"]["temp"]
    description = data["weather"][0]["description"].lower()
    city_name = data["name"]

    alert_reasons = []

    if temp > 35:
        alert_reasons.append(f"High temperature: {temp:.1f}°C")

    if "rain" in description or "drizzle" in description or "thunderstorm" in description:
        alert_reasons.append(f"Rain predicted: {description}")

    if alert_reasons:
        message = f"Weather Alert for {city_name}!\n\n"
        message += "\n".join(alert_reasons)
        message += f"\n\nChecked at: {datetime.now().strftime('%I:%M %p, %d %B %Y')}"
        return True, message

    return False, f"All clear in {city_name}. Temp: {temp:.1f}°C, {description}"

def send_email(subject, body):
    """Send an email alert using Gmail SMTP."""
    sender = os.environ.get("EMAIL_SENDER")
    password = os.environ.get("EMAIL_PASSWORD")  # Gmail App Password
    receiver = os.environ.get("EMAIL_RECEIVER")

    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = receiver

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)

        print("Alert email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def run():
    """Main function - fetch weather, check conditions, alert if needed."""
    print(f"Checking weather for {CITY}...")

    data = get_weather()
    should_alert, message = check_alert(data)

    print(message)

    if should_alert:
        send_email("⚠️ Weather Alert - Pulse Bot", message)
    else:
        print("No alert needed.")

if __name__ == "__main__":
    run()
