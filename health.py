import requests
from bs4 import BeautifulSoup

health_keywords = [
    "health", "mental health", "public health", "healthcare", "medicine", "doctor",
    "hospital", "covid", "pandemic", "virus", "vaccine", "vaccination", "medical",
    "wellness", "fitness", "disease", "infection", "health policy", "clinical", "surgery",
    "nurse", "healthcare worker", "ICU", "OPD", "emergency", "cancer", "cardiac",
    "diabetes", "neurology", "orthopedic", "psychiatry", "nutrition", "therapy",
    "ayurveda", "homeopathy", "pharma", "pharmaceutical", "biotech", "AIIMS", "MBBS"
]

def get_session():
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0"})
    return session

def clean_title(text):
    return ' '.join(text.strip().split())

def scrape_hindustan_times_health():
    try:
        session = get_session()
        url = "https://www.hindustantimes.com/lifestyle/health"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        seen_titles = set()

        for div in soup.select("div.cartHolder"):
            h3_tag = div.find("h3", class_="hdg3")
            if h3_tag:
                a_tag = h3_tag.find("a", href=True)
                if a_tag:
                    title = clean_title(a_tag.get_text())
                    href = a_tag['href']

                    if not any(kw in title.lower() for kw in health_keywords):
                        continue

                    if href.startswith('/'):
                        href = "https://www.hindustantimes.com" + href
                    elif not href.startswith('http'):
                        continue

                    if title and href and title not in seen_titles:
                        articles.append({
                            "title": title,
                            "url": href,
                            "source": "Hindustan Times"
                        })
                        seen_titles.add(title)
        return articles
    except Exception as e:
        print(f"Error scraping Hindustan Times Health: {e}")
        return []

def scrape_times_now_health():
    try:
        session = get_session()
        url = "https://www.timesnownews.com/health"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")

        articles = []
        seen_titles = set()

        for li in soup.select('li._2LXp'):
            anchor = li.find('a', href=True)
            title_tag = li.find('h3')
            if anchor and title_tag:
                href = anchor['href']
                title = clean_title(title_tag.get_text())
                if title not in seen_titles:
                    articles.append({
                        "title": title,
                        "url": href,
                        "source": "Times Now"
                    })
                    seen_titles.add(title)

        return articles

    except Exception as e:
        print(f"Error scraping Times Now Health: {e}")
        return []

def scrape_times_of_india_health():
    try:
        session = get_session()
        url = "https://timesofindia.indiatimes.com/life-style/health-fitness/health-news"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        
        articles = []
        seen_titles = set()

        for box in soup.select("div.md_news_box"):
            a_tag = box.find("a", href=True, title=True)
            if a_tag:
                title = clean_title(a_tag.get_text())
                href = a_tag["href"]
                if href.startswith("/"):
                    href = "https://timesofindia.indiatimes.com" + href
                if title and title not in seen_titles:
                    articles.append({
                        "title": title,
                        "url": href,
                        "source": "Times of India"
                    })
                    seen_titles.add(title)

        return articles

    except Exception as e:
        print(f"Error scraping Times of India Health News: {e}")
        return []

def indian_express_health():
    try:
        session = get_session()
        url = "https://indianexpress.com/section/lifestyle/health/"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        
        articles = []
        seen_titles = set()

        for article_div in soup.select("div.articles"):
            title_tag = article_div.select_one("h2.title a")
            if not title_tag:
                continue

            title = clean_title(title_tag.get_text())
            href = title_tag.get("href")

            if not href.startswith("http"):
                href = "https://indianexpress.com" + href

            if title and href and title not in seen_titles:
                articles.append({
                    "title": title,
                    "url": href,
                    "source": "Indian Express"
                })
                seen_titles.add(title)

        return articles

    except Exception as e:
        print(f"Error scraping Indian Express Health: {e}")
        return []

def scrape_bbc_health():
    try:
        session = get_session()
        url = "https://www.bbc.com/news/health"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")

        articles = []
        seen_titles = set()

        for a_tag in soup.select("a.ssrcss-gvf9zo-PromoLink, a.ssrcss-5wtq5v-PromoLink"):
            title_tag = a_tag.select_one("p.ssrcss-1sen9vx-PromoHeadline span")
            if not title_tag:
                continue

            title = clean_title(title_tag.get_text())
            href = a_tag.get("href")

            # Skip if title is not health-related
            if not any(kw in title.lower() for kw in health_keywords):
                continue

            # Add prefix if href is relative
            if href and href.startswith("/"):
                href = "https://www.bbc.com" + href

            if title and href and title not in seen_titles:
                articles.append({
                    "title": title,
                    "url": href,
                    "source": "BBC"
                })
                seen_titles.add(title)

        return articles

    except Exception as e:
        print(f"Error scraping BBC Health: {e}")
        return []

def scrape_guardian_health():
    try:
        session = get_session()
        url = "https://www.theguardian.com/society/health"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")

        articles = []
        seen_titles = set()

        for a_tag in soup.select("a.dcr-2yd10d"):
            href = a_tag.get("href")
            title = a_tag.get("aria-label", "").strip()

            if not href or not title:
                continue

            # Filter by keyword
            if not any(kw in title.lower() for kw in health_keywords):
                continue

            # Fix relative links
            if href.startswith("/"):
                href = "https://www.theguardian.com" + href

            if title not in seen_titles:
                articles.append({
                    "title": clean_title(title),
                    "url": href,
                    "source": "The Guardian"
                })
                seen_titles.add(title)

        return articles

    except Exception as e:
        print(f"Error scraping The Guardian Health: {e}")
        return []

def scrape_nytimes_health():
    try:
        session = get_session()
        url = "https://www.nytimes.com/international/section/health"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")

        articles = []
        seen_titles = set()

        # Pattern 1
        for h3_tag in soup.select("h3.css-1x50auk"):
            a_tag = h3_tag.find("a", href=True)
            if not a_tag:
                continue
            title = clean_title(a_tag.get_text())
            href = a_tag["href"]

            if not any(kw in title.lower() for kw in health_keywords):
                continue
            if href.startswith("/"):
                href = "https://www.nytimes.com" + href
            if title and href and title not in seen_titles:
                articles.append({
                    "title": title,
                    "url": href,
                    "source": "New York Times"
                })
                seen_titles.add(title)

        # Pattern 2
        for a_tag in soup.select("a.css-8hzhxf"):
            h3_tag = a_tag.find("h3")
            if not h3_tag:
                continue
            title = clean_title(h3_tag.get_text())
            href = a_tag["href"]

            if not any(kw in title.lower() for kw in health_keywords):
                continue
            if href.startswith("/"):
                href = "https://www.nytimes.com" + href
            if title and href and title not in seen_titles:
                articles.append({
                    "title": title,
                    "url": href,
                    "source": "New York Times"
                })
                seen_titles.add(title)

        return articles

    except Exception as e:
        print(f"Error scraping New York Times Health: {e}")
        return []


def scrape_bloomberg_health():
    try:
        session = get_session()
        url = "https://www.bloomberg.com/industries/health"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")

        articles = []
        seen_titles = set()

        # Pattern 1 — anchor with class `styles_itemLink__VgyXJ`
        for a_tag in soup.select("a.styles_itemLink__VgyXJ"):
            title_tag = a_tag.select_one("[data-testid='headline'] span")
            if not title_tag:
                continue
            title = clean_title(title_tag.get_text())
            href = a_tag.get("href", "")
            if not href.startswith("http"):
                href = "https://www.bloomberg.com" + href

            if not any(kw in title.lower() for kw in health_keywords):
                continue

            if title not in seen_titles:
                articles.append({
                    "title": title,
                    "url": href,
                    "source": "Bloomberg"
                })
                seen_titles.add(title)

        # Pattern 2 — anchor with class `StoryBlock_storyLink__5nXw8`
        for a_tag in soup.select("a.StoryBlock_storyLink__5nXw8"):
            title_tag = a_tag.select_one("div[data-testid='headline'] span")
            if not title_tag:
                continue
            title = clean_title(title_tag.get_text())
            href = a_tag.get("href", "")
            if not href.startswith("http"):
                href = "https://www.bloomberg.com" + href

            if not any(kw in title.lower() for kw in health_keywords):
                continue

            if title not in seen_titles:
                articles.append({
                    "title": title,
                    "url": href,
                    "source": "Bloomberg"
                })
                seen_titles.add(title)

        return articles

    except Exception as e:
        print(f"Error scraping Bloomberg Health: {e}")
        return []


def scrape_health_news(region="India", sources=None):
    all_articles = []

    india_source_map = {
        "hindustan_times": scrape_hindustan_times_health,
        "ndtv": scrape_times_now_health,
        "deccan_herald": scrape_times_of_india_health,
        "indian_express": indian_express_health,
    }

    global_source_map = {
        "bbc": scrape_bbc_health,
        "guardian": scrape_guardian_health,
        "nyt": scrape_nytimes_health,
        "bloomberg": scrape_bloomberg_health
    }

    source_map = india_source_map if region == "India" else global_source_map

    if sources is None:
        sources = list(source_map.keys())

    for src in sources:
        func = source_map.get(src)
        if func:
            try:
                src_articles = func()
                print(f"Health News ({region} - {src}): {len(src_articles)} articles")
                all_articles.extend(src_articles)
            except Exception as e:
                print(f"Error in scrape_health_news for source {src}: {e}")

    return all_articles 


if __name__ == "__main__":
    print("--- Scraping India Health News ---")
    india_health_articles = scrape_health_news(region="India")
    for i, art in enumerate(india_health_articles, 1):
        print(f"{i}. {art['title']} ({art.get('source', 'Unknown')})\n   {art['url']}\n")

    print("\n--- Scraping Global Health News ---")
    global_health_articles = scrape_health_news(region="Global")
    for i, art in enumerate(global_health_articles, 1):
        print(f"{i}. {art['title']} ({art.get('source', 'Unknown')})\n   {art['url']}\n")


