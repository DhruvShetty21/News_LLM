import feedparser

def fetch_articles():
    feed_urls = [
        "https://www.edexlive.com/news/rssfeed/?id=198&getXmlFeed=true",
        "https://timesofindia.indiatimes.com/education/rssfeeds/913168846.cms",
        "https://www.thehindu.com/education/feeder/default.rss"
    ]
    articles = []
    for url in feed_urls:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            articles.append({
                "title": entry.title,
                "link": entry.link,
                "summary": entry.get("summary", ""),
                "content": entry.get("summary", "")
            })
    return articles