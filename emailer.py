import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


import re
import unicodedata

def clean_title(title):
    if not title:
        return None
    
    # First, clean Unicode characters
    # Replace common problematic Unicode characters
    replacements = {
        '"': '"',  # Left double quotation mark
        '"': '"',  # Right double quotation mark
        ''': "'",  # Left single quotation mark
        ''': "'",  # Right single quotation mark
        '—': '-',  # Em dash
        '–': '-',  # En dash
        '…': '...',  # Horizontal ellipsis
        ' ': ' ',  # Non-breaking space
        '′': "'",  # Prime
        '″': '"',  # Double prime
    }
    
    for unicode_char, ascii_char in replacements.items():
        title = title.replace(unicode_char, ascii_char)
    
    # Normalize Unicode and convert to ASCII
    title = unicodedata.normalize('NFKD', title)
    title = title.encode('ascii', 'ignore').decode('ascii')
    
    # Clean whitespace
    title = re.sub(r'\s+', ' ', title.strip())
    
    if len(title) < 10 or len(title) > 200:
        return None
    
    # Filter out navigation items and ads
    skip_words = ['subscribe', 'login', 'register', 'advertisement', 'menu', 'search', 'newsletter']
    if any(word in title.lower() for word in skip_words):
        return None
    
    return title

def build_html_email(articles, topic="News"):
    html_body = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Newsletter</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
            body {{
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                line-height: 1.6;
                color: #1a1a1a;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }}
            .container {{
                max-width: 680px;
                margin: 0 auto;
                background: #ffffff;
                border-radius: 16px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                overflow: hidden;
            }}
            .header {{
                background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
                padding: 40px 30px;
                text-align: center;
                position: relative;
                overflow: hidden;
            }}
            .header h1 {{
                color: white;
                font-size: 28px;
                font-weight: 700;
                margin-bottom: 8px;
                position: relative;
                z-index: 1;
            }}
            .header p {{
                color: rgba(255,255,255,0.9);
                font-size: 16px;
                font-weight: 400;
                position: relative;
                z-index: 1;
            }}
            .content {{
                padding: 40px 30px;
            }}
            .article {{
                background: #f3f4f6;
                border-radius: 12px;
                margin-bottom: 30px;
                border: 1px solid #e5e7eb;
                transition: all 0.3s ease;
                overflow: hidden;
            }}
            .article-content {{
                padding: 24px;
            }}
            .article-title {{
                color: #1a1a1a;
                font-size: 20px;
                font-weight: 600;
                margin-bottom: 18px;
                line-height: 1.4;
            }}
            .read-more {{
                display: inline-block;
                background: #22223b;
                color: #fff !important;
                text-decoration: none;
                padding: 12px 22px;
                border-radius: 8px;
                font-weight: 500;
                font-size: 15px;
                transition: background 0.2s;
            }}
            .read-more:hover {{
                background: #4f46e5;
            }}
            .footer {{
                background: #f8fafc;
                padding: 30px;
                text-align: center;
                border-top: 1px solid #e5e7eb;
            }}
            .footer p {{
                color: #6b7280;
                font-size: 14px;
                margin-bottom: 8px;
            }}
            .footer .timestamp {{
                color: #9ca3af;
                font-size: 12px;
            }}
            .divider {{
                height: 1px;
                background: linear-gradient(90deg, transparent, #e5e7eb, transparent);
                margin: 20px 0;
            }}
            @media (max-width: 600px) {{
                .container {{
                    margin: 10px;
                    border-radius: 12px;
                }}
                .header {{
                    padding: 30px 20px;
                }}
                .header h1 {{
                    font-size: 24px;
                }}
                .content {{
                    padding: 30px 20px;
                }}
                .article-content {{
                    padding: 20px;
                }}
                .article-title {{
                    font-size: 18px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Top {len(articles)} {topic.title()} Articles</h1>
                <p>Your curated news digest, delivered fresh</p>
            </div>
            <div class="content">
    """

    for i, article in enumerate(articles):
        title = clean_title(article.get("title", "Untitled"))
        if not title:
            continue  # Skip if title is empty or filtered out
        link = article.get("url", "#")
        source = article.get("source") or "Unknown Source"
        if not link:
            continue  # Skip articles without a URL

        html_body += f"""
            <div class="article">
                <div class="article-content">
                    <h2 class="article-title">{title} <span style='font-size:0.8em; color:#6b7280;'>({source})</span></h2>
                    <a href="{link}" class="read-more">Read Full Article</a>
                </div>
            </div>
        """
        if i < len(articles) - 1:
            html_body += '<div class="divider"></div>'
        
    from datetime import datetime
    current_time = datetime.now().strftime("%B %d, %Y at %I:%M %p")

    html_body += f"""
            </div>
            <div class="footer">
                <p>Thank you for reading our newsletter!</p>
                <p class="timestamp">Sent on {current_time}</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_body

def send_email(to, subject, body, html_body=None):
    from_email = os.getenv("EMAIL")
    password = os.getenv("PASS")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to

    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    if html_body:
        msg.attach(MIMEText(html_body, "html", "utf-8"))

    # Debug prints
    print("[send_email] : Function called ")
    print("Subject repr:", repr(subject))
    print("From repr:", repr(from_email))
    print("To repr:", repr(to))
    print("Body length:", len(body))
    if html_body:
        print("HTML body length:", len(html_body))
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as server:
            server.login(from_email, password)
            server.send_message(msg)
        print(f"✅ Email sent successfully to {to}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email to {to}: {e}")
        return False