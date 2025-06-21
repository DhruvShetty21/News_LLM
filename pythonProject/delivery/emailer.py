import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import yaml
import os

# Dynamically build the correct path to config.yaml
current_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_dir, "..", "config.yaml")

with open(config_path) as f:
    config = yaml.safe_load(f)

EMAIL_CONFIG = config['email']

def send_email(articles):
    if not articles:
        print("⚠️ No articles to email.")
        return

    body = "\n\n".join([f"{a['title']}\n{a['link']}" for a in articles])
    msg = MIMEMultipart()
    msg['From'] = EMAIL_CONFIG['from']
    msg['To'] = EMAIL_CONFIG['to']
    msg['Subject'] = "Your Daily Educational News Digest"
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
            server.starttls()
            server.login(EMAIL_CONFIG['from'], EMAIL_CONFIG['password'])
            server.send_message(msg)
            print(f"✅ Email sent to {EMAIL_CONFIG['to']} with {len(articles)} articles.")
    except Exception as e:
        print(f"❌ Email failed: {e}")
