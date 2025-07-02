import requests
from bs4 import BeautifulSoup
import time

def clean_text(text):
    return ' '.join(text.strip().split())

def scrape_the_hindu_industry():
    articles = []
    seen_titles = set()
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0"})
    try:
        for page in range(1, 4):
            url = f"https://www.thehindu.com/business/Industry/?page={page}"
            response = session.get(url, timeout=15)
            soup = BeautifulSoup(response.content, "html.parser")
            for h3 in soup.find_all('h3', class_='title big'):
                a_tag = h3.find('a', href=True)
                if not a_tag:
                    continue
                title = clean_text(a_tag.get_text())
                href = a_tag['href']
                if title and title not in seen_titles:
                    articles.append({"title": title, "url": href, "source": "The Hindu"})
                    seen_titles.add(title)
        return articles
    except Exception as e:
        print(f"Error scraping The Hindu Industry: {e}")
        return []

def scrape_financial_express_industry():
    articles = []
    seen_titles = set()
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0"})
    try:
        for page in range(1, 5):
            url = f"https://www.financialexpress.com/business/industry/page/{page}/" if page > 1 else "https://www.financialexpress.com/business/industry/"
            response = session.get(url, timeout=15)
            soup = BeautifulSoup(response.content, "html.parser")
            for h2 in soup.find_all('h2', class_='entry-title'):
                a_tag = h2.find('a', href=True)
                if not a_tag:
                    continue
                title = clean_text(a_tag.get_text())
                href = a_tag['href']
                if title and title not in seen_titles:
                    articles.append({"title": title, "url": href, "source": "Financial Express"})
                    seen_titles.add(title)
        return articles
    except Exception as e:
        print(f"Error scraping Financial Express Industry: {e}")
        return []

def scrape_manufacturing_today_india():
    articles = []
    seen_titles = set()
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0"})
    try:
        url = "https://www.manufacturingtodayindia.com/"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        for a_tag in soup.find_all('a', rel='bookmark', href=True):
            title = clean_text(a_tag.get_text())
            href = a_tag['href']
            if title and title not in seen_titles:
                articles.append({"title": title, "url": href, "source": "Manufacturing Today India"})
                seen_titles.add(title)
        return articles
    except Exception as e:
        print(f"Error scraping Manufacturing Today India: {e}")
        return []

def scrape_bbc_industry():
    articles = []
    seen_titles = set()
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0"})
    try:
        url = "https://www.bbc.com/news/topics/c0repy5vn95t"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        for a_tag in soup.find_all('a', attrs={"data-testid": "internal-link"}, href=True):
            href = a_tag['href']
            if not href.startswith('http'):
                href = "https://www.bbc.com" + href
            h2 = a_tag.find('h2', attrs={"data-testid": "card-headline"})
            p = a_tag.find('p', attrs={"data-testid": "card-description"})
            if not h2:
                continue
            headline = clean_text(h2.get_text())
            summary = clean_text(p.get_text()) if p else ''
            title = headline + (f" — {summary}" if summary else "")
            if title and title not in seen_titles:
                articles.append({"title": title, "url": href, "source": "BBC"})
                seen_titles.add(title)
        return articles
    except Exception as e:
        print(f"Error scraping BBC Industry: {e}")
        return []

def scrape_nytimes_industry():
    articles = []
    seen_titles = set()
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0"})
    try:
        url = "https://www.nytimes.com/topic/subject/factories-and-manufacturing"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        for a_tag in soup.find_all('a', class_='css-8hzhxf', href=True):
            h3 = a_tag.find('h3')
            if not h3:
                continue
            title = clean_text(h3.get_text())
            href = a_tag['href']
            if not href.startswith('http'):
                href = "https://www.nytimes.com" + href
            if title and title not in seen_titles:
                articles.append({"title": title, "url": href, "source": "NY Times"})
                seen_titles.add(title)
        return articles
    except Exception as e:
        print(f"Error scraping NY Times Industry: {e}")
        return []

def scrape_guardian_industry():
    articles = []
    seen_titles = set()
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0"})
    try:
        url = "https://www.theguardian.com/business/industry"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        for a_tag in soup.find_all('a', attrs={"aria-label": True}, href=True):
            title = clean_text(a_tag['aria-label'])
            href = a_tag['href']
            if not href.startswith('http'):
                href = "https://www.theguardian.com" + href
            if title and title not in seen_titles:
                articles.append({"title": title, "url": href, "source": "The Guardian"})
                seen_titles.add(title)
        return articles
    except Exception as e:
        print(f"Error scraping Guardian Industry: {e}")
        return []

def scrape_bloomberg_industry():
    articles = []
    seen_titles = set()
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0"})
    try:
        url = "https://www.bloomberg.com/industries"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        for a_tag in soup.find_all('a', class_='StoryBlock_storyLink__5nXw8', href=True):
            headline_div = a_tag.find('div', attrs={"data-testid": "headline"})
            span = headline_div.find('span') if headline_div else None
            title = clean_text(span.get_text()) if span else ''
            href = a_tag['href']
            if not href.startswith('http'):
                href = "https://www.bloomberg.com" + href
            if title and title not in seen_titles:
                articles.append({"title": title, "url": href, "source": "Bloomberg"})
                seen_titles.add(title)
        return articles
    except Exception as e:
        print(f"Error scraping Bloomberg Industry: {e}")
        return []

def scrape_industry_news(region="India", sources=None):
    india_source_map = {
        "the_hindu": scrape_the_hindu_industry,
        "financial_express": scrape_financial_express_industry,
        "manufacturing_today": scrape_manufacturing_today_india,
    }
    global_source_map = {
        "bbc": scrape_bbc_industry,
        "nytimes": scrape_nytimes_industry,
        "guardian": scrape_guardian_industry,
        "bloomberg": scrape_bloomberg_industry,
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
                src_articles = func()
                all_articles.extend(src_articles)
            except Exception as e:
                print(f"Error in scrape_industry_news for source {src}: {e}")
    return all_articles

if __name__ == "__main__":
    print("--- Scraping India Industry News ---")
    india_articles = scrape_industry_news(region="India")
    for i, art in enumerate(india_articles, 1):
        print(f"{i}. {art['title']} ({art['source']})\n   {art['url']}\n")

    print("\n--- Scraping Global Industry News ---")
    global_articles = scrape_industry_news(region="Global")
    for i, art in enumerate(global_articles, 1):
        print(f"{i}. {art['title']} ({art['source']})\n   {art['url']}\n") 