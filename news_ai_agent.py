import os
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from emailer import send_email, build_html_email
from higher_ed import scrape_higher_ed_news
from entertainment import scrape_entertainment_news
from sports import scrape_sports_news
from business_and_finance import scrape_business_finance_news
from dotenv import load_dotenv
from technology import scrape_technology_news
from news_sources import scrape_news
from environment import scrape_environment_news
from industry import scrape_industry_news
from health import scrape_health_news
from urllib.parse import urlparse
import re

load_dotenv(dotenv_path="scratch.env")
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

def select_top_news_with_gemini(articles, top_n=10, return_scores=False):
    print(f"[Gemini] Preparing to call Gemini LLM with {len(articles)} articles, requesting top {top_n}.")
    if not GEMINI_API_KEY:
        print("Gemini API key not found.")
        return articles[:top_n] if not return_scores else [(art, None) for art in articles[:top_n]]

    llm = ChatGoogleGenerativeAI(
        model="models/gemini-1.5-flash", google_api_key=GEMINI_API_KEY
    )

    prompt = (
        "You are an expert news assistant. "
        "Given the following list of news headlines (with their sources and links), "
        "for each headline, assign an importance score from 1 (least important) to 10 (most important) for inclusion in an education news digest. "
        "Consider newsworthiness, impact, and diversity. "
        "Return your answer as a numbered list in this format:\n"
        "<SOURCE>, <HEADLINE>\n<LINK>\nScore: <score>\n\n"
        "Here is the list:\n"
    )

    for idx, article in enumerate(articles, 1):
        source = article.get("source", "Unknown Source")
        title = article["title"]
        url = article["url"]
        prompt += f"{idx}. {source}, {title}\n{url}\n"

    print("[Gemini] Calling Gemini LLM API...")
    response = llm.invoke([HumanMessage(content=prompt)])
    print("[Gemini] Gemini LLM API call completed.")
    print("Gemini raw output:\n", response.content)

    lines = str(response.content).split("\n")
    scored_articles = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line and "," in line and line[0].isdigit() and "." in line:
            source_headline = line.split(".", 1)[1].strip()
            url = lines[i + 1].strip() if i + 1 < len(lines) else ""
            score_line = lines[i + 2].strip() if i + 2 < len(lines) else ""
            score_match = re.search(r"Score:\s*(\d+)", score_line)
            score = int(score_match.group(1)) if score_match else 0
            for art in articles:
                if art["title"] in source_headline and art["url"] in url:
                    scored_articles.append((art, score))
                    break
            i += 3
        else:
            i += 1

    scored_articles.sort(key=lambda x: x[1], reverse=True)
    return scored_articles[:top_n] if return_scores else [art for art, score in scored_articles[:top_n]]

def create_display_url(url, max_length=50):
    if len(url) <= max_length:
        return url
    if "news.google.com" in url:
        return f"news.google.com/articles/... (Google News)"
    try:
        parsed = urlparse(url)
        domain = parsed.netloc
        if len(domain) > max_length - 10:
            return f"{domain[:max_length - 7]}..."
        path = parsed.path
        remaining = max_length - len(domain) - 3
        if len(path) > remaining:
            return f"{domain}{path[:remaining]}..."
        return f"{domain}{path}"
    except:
        half = (max_length - 5) // 2
        return f"{url[:half]} ... {url[-half:]}"

def format_email(articles):
    if not articles:
        return "No education news articles found for your preferences today.\n\nPlease try again later."

    body = "🎓 Your Education News Digest 🎓\n"
    body += "=" * 50 + "\n\n"

    for i, article in enumerate(articles, 1):
        display_url = create_display_url(article["url"])
        body += f"{i}. {article['title']}\n"
        body += f"   🔗 Full link: {article['url']}\n\n"

    body += "\n" + "=" * 50 + "\n"
    body += "This digest was automatically generated.\n"
    body += "Stay informed, stay educated! 🌟"

    return body

def process_and_send(emails, category, region, top_n=10, sources=None):
    print(f"[process_and_send] Function Called with category={category}, region={region}, top_n={top_n}, sources={sources}")
    errors = []
    articles = []
    topic = ""

    # Scraping
    if category == "higher_ed":
        articles = scrape_higher_ed_news(region=region, sources=sources)
        topic = f"{region} Higher Education"
    elif category == "entertainment":
        articles = scrape_entertainment_news(region=region, sources=sources)
        topic = f"{region} Entertainment"
    elif category == "sports":
        articles = scrape_sports_news(region=region, sources=sources)
        topic = f"{region} Sports"
    elif category == "business_and_finance":
        articles = scrape_business_finance_news(region=region, sources=sources)
        topic = f"{region} Business & Finance"
    elif category == "tech":
        articles = scrape_technology_news(region=region, sources=sources)
        topic = f"{region} Technology"
    elif category == "environment":
        articles = scrape_environment_news(region=region, sources=sources)
        topic = f"{region} Environment"
    elif category == "industry":
        articles = scrape_industry_news(region=region, sources=sources)
        topic = f"{region} Industry"
    elif category == "health":
        articles = scrape_health_news(region=region, sources=sources)
        topic = f"{region} Health"
    else:
        articles, errors = scrape_news(region, sources)
        topic = region if region else "General"

    print(f"[process_and_send] Scraping complete. Found {len(articles)} articles.")

    if not emails:
        return "\u274c Please enter at least one email address"

    email_list = [e.strip() for e in re.split(r"[;,]", emails) if e.strip()]
    invalids = [e for e in email_list if "@" not in e]
    if not email_list or invalids:
        return f"\u274c Invalid email(s): {', '.join(invalids)}"

    if not articles:
        msg = "\u26a0\ufe0f No articles found for the selected region. Please try again later."
        if errors:
            msg += "\n\n\u26a0\ufe0f Some sources failed to scrape:\n" + "\n".join(errors)
        return msg

    print(f"Calling select_top_news_with_gemini with {len(articles)} articles.")
    top_articles = select_top_news_with_gemini(articles, top_n=top_n)
    print(f"Gemini selection complete. {len(top_articles)} articles selected.")

    email_body = format_email(top_articles)
    html_body = build_html_email(top_articles, topic=topic)
    subject = f"{topic} News Digest - (Top {top_n} articles)"

    success, failed = [], []
    for email in email_list:
        if send_email(email, subject, email_body, html_body):
            success.append(email)
        else:
            failed.append(email)

    msg = ""
    if success:
        msg += f"\u2705 Email sent successfully to: {', '.join(success)}\n"
    if failed:
        msg += f"\u274c Failed to send email to: {', '.join(failed)}"
    if errors:
        msg += "\n\n\u26a0\ufe0f Some sources failed to scrape:\n" + "\n".join(errors)
    return msg.strip()
