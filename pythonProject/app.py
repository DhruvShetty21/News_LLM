import json
import yaml
import os
from scraping.rss_scraper import fetch_articles
from chains.filter_chain import classify_article
from delivery.emailer import send_email

# Dynamically build the correct path to config.yaml
current_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_dir, "config.yaml")

with open(config_path) as f:
    config = yaml.safe_load(f)

USER_FILTER = config["user_filter"]

def main():
    articles = fetch_articles()
    results = []

    for article in articles:
        classification = classify_article(article['content'])
        print(f"📝 Article classified as: {classification}")  # Add this
        if (classification.get('is_educational') and
            classification.get('region') == USER_FILTER['region'] and
            classification.get('content_type') == USER_FILTER['content_type']):
            print("✅ Article matches filter. Added to results.")
            results.append({
                "title": article['title'],
                "link": article['link'],
                "summary": article['summary']
            })


    if config['delivery']['method'] == 'email':
        print(f"📦 Final matched articles: {len(results)}")
        for r in results:
            print(f"- {r['title']}")

        send_email(results)
    else:
        print("Filtered Educational News:\n")
        for r in results:
            print(f"- {r['title']}\n  {r['link']}\n")

if __name__ == "__main__":
    main()
