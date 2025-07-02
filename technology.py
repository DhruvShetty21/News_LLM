import requests
from bs4 import BeautifulSoup
import time
from time import sleep


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

def scrape_hindustan_times_tech():
    try:
        session = get_session()
        url = "https://www.hindustantimes.com/technology"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        seen_titles = set()
        divs = soup.select('div.cartHolder.listView')
        for div in divs:
            a_tag = div.select_one('h3.hdg3 a')
            if not a_tag:
                continue
            title = clean_title(a_tag.get_text())
            href = a_tag.get('href', '')
            if not any(kw in title.lower() for kw in technology_keywords):
                continue
            if title and title not in seen_titles and href:
                if href.startswith('/'):
                    href = "https://www.hindustantimes.com" + href
                articles.append({"title": title, "url": href, "source": "Hindustan Times"})
                seen_titles.add(title)
        return articles
    except Exception as e:
        print(f"Error scraping Hindustan Times: {e}")
        return []

def scrape_ndtv_tech():
    try:
        session = get_session()
        url = "https://www.ndtv.com/technology"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        seen_titles = set()
        for tag in soup.select('.newsHdng a, .SrchLstPg_ttl-lnk a, h2 a, h3 a'):
            title = clean_title(tag.get_text())
            href = tag.get('href', '')
            if not any(kw in title.lower() for kw in technology_keywords):
                continue
            if title and title not in seen_titles and href:
                if href.startswith('/'):
                    href = "https://www.ndtv.com" + href
                articles.append({"title": title, "url": href, "source": "NDTV"})
                seen_titles.add(title)
        return articles
    except Exception as e:
        print(f"Error scraping NDTV: {e}")
        return []

def scrape_deccan_herald_tech():
    try:
        session = get_session()
        url = "https://www.deccanherald.com/sci-tech/technology"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        seen_titles = set()
        # Find all story cards in the technology section
        for story_card in soup.find_all('div', class_='story-card-15'):
            h2 = story_card.find('h2', class_='headline')
            if not h2:
                continue
            a_tag = h2.find('a', href=True)
            if not a_tag:
                continue
            title = clean_title(a_tag.text)
            if not any(kw in title.lower() for kw in technology_keywords):
                continue
            href = a_tag['href']
            if href.startswith('/'):
                href = "https://www.deccanherald.com" + href
            if title not in seen_titles:
                articles.append({"title": title, "url": href, "source": "Deccan Herald"})
                seen_titles.add(title)
        return articles
    except Exception as e:
        print(f"Error scraping Deccan Herald: {e}")
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
            title_tag = article.find("div", class_="entry-title")
            if not title_tag:
                continue
            a_tag = title_tag.find("a", href=True)
            if not a_tag:
                continue
            title = clean_text(a_tag.text)
            href = a_tag["href"]
            if title and title not in seen_titles:
                articles.append({"title": title, "url": href, "source": "Financial Express"})
                seen_titles.add(title)
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
            title = clean_title(tag.get_text())
            href = tag.get('href', '')
            if not any(kw in title.lower() for kw in technology_keywords):
                continue
            if title and title not in seen_titles:
                if href.startswith('/'):
                    href = "https://indianexpress.com" + href
                articles.append({"title": title, "url": href, "source": "Indian Express"})
                seen_titles.add(title)
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
            title = clean_title(tag.get('aria-label'))
            href = tag.get('href', '')
            if not any(kw in title.lower() for kw in technology_keywords):
                continue
            if title and href and '/202' in href and title not in seen_titles:
                articles.append({"title": title, "url": href, "source": "The Guardian"})
                seen_titles.add(title)
        return articles
    except Exception as e:
        print(f"Error scraping Guardian Tech: {e}")
        return []

def scrape_euronews(query="technology", max_pages=3, delay=0.3):
    api_url = "https://www.euronews.com/api/search"
    headers = {"User-Agent": "Mozilla/5.0"}
    articles = []
    for page in range(1, max_pages + 1):
        print(f"🔎 Scraping Euronews page {page}...")
        params = {"query": query, "page": page, "size": 10}
        try:
            res = requests.get(api_url, headers=headers, params=params, timeout=15)
            res.raise_for_status()
            results = res.json()
            if not isinstance(results, list) or not results:
                print("🛑 No more results.")
                break
        except Exception as exc:
            print(f"❌ Page {page} failed: {exc}")
            break
        for item in results:
            title = clean_text(item.get("title", ""))
            url = ensure_absolute(item.get("url", ""))
            if title and url:
                articles.append({"title": title, "url": url, "source": "Euronews"})
        sleep(delay)
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
            title_tag = card.find("a", class_="Card-title")
            if title_tag and title_tag.text and title_tag['href']:
                title = clean_text(title_tag.text)
                href = title_tag['href']
                if title not in seen_titles:
                    articles.append({"title": title, "url": href, "source": "CNBC"})
                    seen_titles.add(title)
        return articles
    except Exception as e:
        print(f"Error scraping CNBC: {e}")
        return []

# --- WRAPPER FUNCTIONS ---

def scrape_india_tech_news():
    all_articles = []
    print("\n--- Scraping India Technology News ---")
    for src_func in [
        scrape_hindustan_times_tech, scrape_ndtv_tech,
        scrape_deccan_herald_tech, scrape_financial_express_tech,
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
        "ndtv": scrape_ndtv_tech,
        "deccan_herald": scrape_deccan_herald_tech,
        "financial_express": scrape_financial_express_tech,
        "indian_express": scrape_indian_express_tech,
    }
    global_source_map = {
        "guardian": scrape_guardian_tech,
        "euronews": scrape_euronews,
        "cnbc": scrape_cnbc_tech,
    }
    if region == "India":
        source_map = india_source_map
    else:
        source_map = global_source_map
    if sources is None:
        sources = list(source_map.keys())
    all_articles = []
    for src in sources:
        func = source_map.get(src)
        if func:
            try:
                src_articles = func() if src != "euronews" else func()  # euronews takes default query
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