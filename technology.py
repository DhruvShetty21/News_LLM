import requests
from bs4 import BeautifulSoup, Tag
from time import sleep
from typing import cast


def clean_text(text):
    return ' '.join(text.strip().split())


def get_session():
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0"})
    return session


def clean_title(text):
    return clean_text(text.replace("\n", " ").replace("\xa0", " "))


def ensure_absolute(url: str) -> str:
    if url.startswith(('http://', 'https://')):
        return url
    return f"https://www.euronews.com/{url.lstrip('/')}"


technology_keywords = [
    "technology", "tech", "ai", "artificial intelligence", "machine learning", "deep learning",
    "data science", "robotics", "quantum", "5g", "iot", "cybersecurity", "hacking", "software",
    "hardware", "semiconductor", "startup", "cloud", "computing", "mobile", "gadget",
    "internet", "app", "programming", "coding", "developer", "python", "javascript",
    "meta", "google", "microsoft", "apple", "openai", "chatgpt", "elon", "tesla", "neuralink"
]


# --- INDIA SOURCES ---

def scrape_times_of_india_tech():
    try:
        session = get_session()
        url = "https://timesofindia.indiatimes.com/technology"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        seen_titles = set()

        # Structure 1: div.lSIdy.col_l_6.col_m_6 with multiple a.linktype1 links
        for div in soup.select('div.lSIdy.col_l_6.col_m_6'):
            for a_tag in div.find_all('a', class_='linktype1', href=True):
                span_tag = a_tag.find('span')
                if span_tag:
                    title = clean_title(span_tag.get_text())
                    href = a_tag.get('href', '')

                    if title and title not in seen_titles and href:
                        # Clean URL parameters
                        href = href.split('?')[0]

                        if href.startswith('/'):
                            href = "https://timesofindia.indiatimes.com" + href
                        elif not href.startswith('http'):
                            continue

                        articles.append({"title": title, "url": href, "source": "Times of India"})
                        seen_titles.add(title)

        # Structure 2: div.GLeza with h5 title
        for div in soup.select('div.GLeza'):
            a_tag = div.find('a', href=True)
            if a_tag:
                h5_tag = a_tag.find('h5')
                if h5_tag:
                    title = clean_title(h5_tag.get_text())
                    href = a_tag.get('href', '')

                    if title and title not in seen_titles and href:
                        # Clean URL parameters
                        href = href.split('?')[0]

                        if href.startswith('/'):
                            href = "https://timesofindia.indiatimes.com" + href
                        elif not href.startswith('http'):
                            continue

                        articles.append({"title": title, "url": href, "source": "Times of India"})
                        seen_titles.add(title)

        print(f"scrape_times_of_india_tech: {len(articles)} articles")
        return articles

    except Exception as e:
        print(f"Error scraping Times of India Technology: {e}")
        return []


def scrape_hindustan_times_tech():
    try:
        url = "https://www.hindustantimes.com/technology"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/114.0.0.0 Safari/537.36"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        articles = []
        seen_titles = set()

        divs = soup.select('div.cartHolder')
        print(f"Found {len(divs)} article blocks")

        for div in divs:
            if not isinstance(div, Tag):
                continue

            a_tag = div.find('a', class_="storyLink")
            if not isinstance(a_tag, Tag):
                continue

            href = a_tag.get("href")
            title = div.get("data-vars-story-title") or a_tag.get_text().strip()

            if not isinstance(title, str) or not title:
                continue

            if not any(kw in title.lower() for kw in technology_keywords):
                continue

            if title not in seen_titles:
                if isinstance(href, str) and href.startswith("/"):
                    href = "https://www.hindustantimes.com" + href
                elif not isinstance(href, str):
                    continue
                articles.append({
                    "title": title,
                    "url": href,
                    "source": "Hindustan Times"
                })
                seen_titles.add(title)
        print(f"scrape_hindustan_times_tech: {len(articles)} articles")
        return articles

    except Exception as e:
        print(f"Error: {e}")
        return []

def scrape_financial_express_tech():
    url = "https://www.financialexpress.com/about/technology-news/"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        seen_titles = set()
        for article in soup.find_all("article"):
            title_tag = cast(Tag, article).find("div", class_="entry-title")
            if not isinstance(title_tag, Tag):
                continue
            a_tag = title_tag.find("a")
            if not isinstance(a_tag, Tag):
                continue
            title = clean_text(a_tag.text)
            href = a_tag.get("href")
            if not title or not isinstance(href, str):
                continue
            if title not in seen_titles:
                articles.append({"title": title, "url": href, "source": "Financial Express"})
                seen_titles.add(title)
        print(f"scrape_financial_express_tech: {len(articles)} articles")
        return articles
    except Exception as e:
        print(f"Error scraping Financial Express: {e}")
        return []


def scrape_indian_express_tech():
    try:
        session = get_session()
        url = "https://indianexpress.com/section/technology/"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        seen_titles = set()
        for tag in soup.select('h3 a, h2 a'):
            if not isinstance(tag, Tag):
                continue
            title = clean_title(tag.get_text())
            href = tag.get("href")
            if not isinstance(href, str):
                continue
            if not any(kw in title.lower() for kw in technology_keywords):
                continue
            if title and title not in seen_titles:
                if href.startswith('/'):
                    href = "https://indianexpress.com" + href
                articles.append({"title": title, "url": href, "source": "Indian Express"})
                seen_titles.add(title)
        print(f"scrape_indian_express_tech: {len(articles)} articles")
        return articles
    except Exception as e:
        print(f"Error scraping Indian Express: {e}")
        return []


# --- GLOBAL SOURCES ---
def scrape_guardian_tech():
    try:
        url = "https://www.theguardian.com/technology"
        response = requests.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        seen_titles = set()

        for tag in soup.select('a[aria-label]'):
            if not isinstance(tag, Tag):
                continue
            title = clean_title(tag.get('aria-label') or '')
            href = tag.get('href')
            if not title or not isinstance(href, str):
                continue
            if href.startswith('/'):
                href = "https://www.theguardian.com" + href
            if not any(kw in title.lower() for kw in technology_keywords):
                continue
            if '/202' in href and title not in seen_titles:
                articles.append({"title": title, "url": href, "source": "The Guardian"})
                seen_titles.add(title)
        print(f"scrape_guardian_tech: {len(articles)} articles")
        return articles
    except Exception as e:
        print(f"Error scraping Guardian Tech: {e}")
        return []


def scrape_euronews(query="technology", max_pages=1, delay=0.5):
    base_url = "https://www.euronews.com/search"
    headers = {"User-Agent": "Mozilla/5.0"}
    articles = []

    for page in range(1, max_pages + 1):
        print(f"🔎 Scraping page {page}...")
        params = {"query": query, "p": page}
        try:
            res = requests.get(base_url, headers=headers, params=params, timeout=15)
            res.raise_for_status()
        except Exception as exc:
            print(f"❌ Request failed on page {page}: {exc}")
            break

        soup = BeautifulSoup(res.text, "html.parser")
        for a in soup.select("article a.the-media-object__link"):
            if not isinstance(a, Tag):
                continue
            url = a.get("href")
            title = a.get("aria-label") or a.get_text(strip=True)
            if isinstance(url, str) and title:
                if not url.startswith("http"):
                    url = "https://www.euronews.com" + url
                articles.append({"title": title, "url": url, "source": "Euronews"})
        sleep(delay)
    print(f"scrape_euronews: {len(articles)} articles")
    return articles


def scrape_cnbc_tech():
    url = "https://www.cnbc.com/technology/"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        articles = []
        seen_titles = set()
        cards = soup.find_all("div", attrs={"data-test": "Card"})
        for card in cards:
            if not isinstance(card, Tag):
                continue
            title_tag = card.find("a", class_="Card-title")
            if not isinstance(title_tag, Tag):
                continue
            title = clean_text(title_tag.text)
            href = title_tag.get("href")
            if title and isinstance(href, str) and title not in seen_titles:
                articles.append({"title": title, "url": href, "source": "CNBC"})
                seen_titles.add(title)
        print(f"scrape_cnbc_tech: {len(articles)} articles")
        return articles
    except Exception as e:
        print(f"Error scraping CNBC: {e}")
        return []




# --- WRAPPER FUNCTIONS ---
def scrape_india_tech_news():
    all_articles = []
    print("\n--- Scraping India Technology News ---")
    for src_func in [
        scrape_hindustan_times_tech,
        scrape_financial_express_tech,
        scrape_indian_express_tech
    ]:
        try:
            src_articles = src_func()
            if src_articles:
                print(f"Fetched {len(src_articles)} from {src_articles[0]['source']}")
            all_articles.extend(src_articles)
        except Exception as e:
            print(f"Error during Indian scraping: {e}")
    return all_articles


def scrape_global_tech_news():
    all_articles = []
    print("\n--- Scraping Global Technology News ---")
    for src_func in [scrape_guardian_tech, scrape_euronews, scrape_cnbc_tech]:
        try:
            src_articles = src_func()
            if src_articles:
                print(f"Fetched {len(src_articles)} from {src_articles[0]['source']}")
            all_articles.extend(src_articles)
        except Exception as e:
            print(f"Error during Global scraping: {e}")
    return all_articles


def scrape_technology_news(region="India", sources=None):
    india_source_map = {
        "hindustan_times": scrape_hindustan_times_tech,
        "times_of_india": scrape_times_of_india_tech,
        "financial_express": scrape_financial_express_tech,
        "indian_express": scrape_indian_express_tech,
    }
    global_source_map = {
        "guardian": scrape_guardian_tech,
        "euronews": scrape_euronews,
        "cnbc": scrape_cnbc_tech,
    }
    source_map = india_source_map if region == "India" else global_source_map
    if sources is None:
        sources = list(source_map.keys())
    all_articles = []
    for src in sources:
        func = source_map.get(src)
        if func:
            try:
                src_articles = func()
                print(f"Technology News ({region} - {src}): {len(src_articles)} articles")
                all_articles.extend(src_articles)
            except Exception as e:
                print(f"Error in scrape_technology_news for source {src}: {e}")
    return all_articles


# --- MAIN ---
if __name__ == "__main__":
    india_articles = scrape_india_tech_news()
    print(f"\n✅ Total Indian tech articles: {len(india_articles)}\n")
    for i, art in enumerate(india_articles, 1):
        print(f"{i}. {art['title']} ({art['source']})")
        print(f"   {art['url']}\n")

    global_articles = scrape_global_tech_news()
    print(f"\n✅ Total Global tech articles: {len(global_articles)}\n")
    for i, art in enumerate(global_articles, 1):
        print(f"{i}. {art['title']} ({art['source']})")
        print(f"   {art['url']}\n")
