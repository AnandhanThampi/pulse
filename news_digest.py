# news_digest.py
# Scrapes top headlines from 3 news websites.
# Compiles them into a formatted HTML email and sends it.
# Scheduled to run every morning at 7 AM IST via GitHub Actions.

import requests
import smtplib
import os
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

# -- FUNCTION 1: Scrape The Hindu ------------------------------------
def scrape_the_hindu():
    """Get top headlines from The Hindu."""
    headlines = []
    try:
        url = "https://www.thehindu.com/"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # The Hindu uses <h3> tags for article titles with links
        articles = soup.select("h3.title a")[:5]

        for article in articles:
            title = article.get_text(strip=True)
            link = article.get("href", "#")
            if title:
                headlines.append({"title": title, "link": link, "time": "Latest"})

    except Exception as e:
        headlines.append({"title": f"Could not fetch The Hindu ({e})", "link": "#", "time": ""})

    return headlines

# -- FUNCTION 2: Scrape BBC News India --------------------------------
def scrape_bbc():
    """Get top headlines from BBC News India."""
    headlines = []
    try:
        url = "https://feeds.bbci.co.uk/news/india/rss.xml"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "xml")
        items = soup.find_all("item")[:5]

        for item in items:
            title = item.find("title").get_text(strip=True) if item.find("title") else "No title"
            link = item.find("link").get_text(strip=True) if item.find("link") else "#"
            pub_date = item.find("pubDate").get_text(strip=True) if item.find("pubDate") else ""
            headlines.append({"title": title, "link": link, "time": pub_date[:16] if pub_date else "Latest"})

    except Exception as e:
        headlines.append({"title": f"Could not fetch BBC News ({e})", "link": "#", "time": ""})

    return headlines

# -- FUNCTION 3: Scrape Times of India --------------------------------
def scrape_toi():
    """Get top headlines from Times of India RSS feed."""
    headlines = []
    try:
        url = "https://timesofindia.indiatimes.com/rssfeedstopstories.cms"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "xml")
        items = soup.find_all("item")[:5]

        for item in items:
            title = item.find("title").get_text(strip=True) if item.find("title") else "No title"
            link = item.find("link").get_text(strip=True) if item.find("link") else "#"
            pub_date = item.find("pubDate").get_text(strip=True) if item.find("pubDate") else ""
            headlines.append({"title": title, "link": link, "time": pub_date[:16] if pub_date else "Latest"})

    except Exception as e:
        headlines.append({"title": f"Could not fetch Times of India ({e})", "link": "#", "time": ""})

    return headlines

# -- FUNCTION 4: Build the HTML email ---------------------------------
def build_html_email(hindu, bbc, toi):
    """Compile all headlines into a formatted HTML email."""
    today = datetime.now().strftime("%A, %d %B %Y")

    def make_section(source_name, color, articles):
        rows = ""
        for article in articles:
            rows += f"""
            <tr>
                <td style="padding: 10px 0; border-bottom: 1px solid #f0f0f0;">
                    <a href="{article['link']}" style="color: #222; text-decoration: none; font-size: 14px; line-height: 1.5;">
                        {article['title']}
                    </a>
                    <br>
                    <span style="font-size: 11px; color: #888;">{article['time']}</span>
                </td>
            </tr>"""
        return f"""
        <tr>
            <td style="padding: 20px 0 5px;">
                <h2 style="margin: 0; color: {color}; font-size: 16px; border-left: 4px solid {color}; padding-left: 10px;">
                    {source_name}
                </h2>
            </td>
        </tr>
        {rows}"""

    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; color: #333;">

        <table width="100%" cellpadding="0" cellspacing="0">
            <tr>
                <td style="background: #1a1a2e; padding: 24px; text-align: center;">
                    <h1 style="color: white; margin: 0; font-size: 22px;">📰 Morning News Digest</h1>
                    <p style="color: #aaa; margin: 6px 0 0; font-size: 13px;">{today}</p>
                </td>
            </tr>

            <tr>
                <td style="padding: 20px;">
                    <table width="100%" cellpadding="0" cellspacing="0">
                        {make_section("The Hindu", "#e63946", hindu)}
                        {make_section("BBC News India", "#bb0000", bbc)}
                        {make_section("Times of India", "#f77f00", toi)}
                    </table>
                </td>
            </tr>

            <tr>
                <td style="background: #f5f5f5; padding: 16px; text-align: center;">
                    <p style="margin: 0; font-size: 11px; color: #999;">
                        Sent automatically by Pulse News Bot · {today}
                    </p>
                </td>
            </tr>
        </table>

    </body>
    </html>
    """
    return html

# -- FUNCTION 5: Send the email ---------------------------------------
def send_email(html_body):
    """Send the HTML digest email via Gmail SMTP."""
    sender = os.environ.get("EMAIL_SENDER")
    password = os.environ.get("EMAIL_PASSWORD")
    receiver = os.environ.get("EMAIL_RECEIVER")

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"📰 Morning News Digest - {datetime.now().strftime('%d %B %Y')}"
        msg["From"] = sender
        msg["To"] = receiver

        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)

        print("News digest email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# -- FUNCTION 6: Run --------------------------------------------------
def run():
    """Scrape all sources, build the email, send it."""
    print("Scraping news headlines...")

    hindu = scrape_the_hindu()
    bbc = scrape_bbc()
    toi = scrape_toi()

    print(f"The Hindu: {len(hindu)} articles")
    print(f"BBC News: {len(bbc)} articles")
    print(f"Times of India: {len(toi)} articles")

    html = build_html_email(hindu, bbc, toi)

    # Save locally for testing
    with open("news_digest.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Saved news_digest.html")

    send_email(html)

if __name__ == "__main__":
    run()
