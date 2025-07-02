import requests
from bs4 import BeautifulSoup
from news_sources import get_session, clean_title
import time

business_finance_keywords = [
    "business", "finance", "economy", "market", "stock", "investment", "banking",
    "corporate", "company", "industry", "trade", "commerce", "financial", "economic",
    "revenue", "profit", "earnings", "merger", "acquisition", "ipo", "startup",
    "venture", "capital", "funding", "loan", "credit", "debt", "inflation",
    "gdp", "nse", "bse", "sensex", "nifty", "rupee", "dollar", "currency",
    "rbi", "sebi", "mutual fund", "insurance", "tax", "gst", "budget",
    "fiscal", "monetary", "policy", "retail", "manufacturing", "services",
    "infrastructure", "real estate", "automotive", "technology", "pharma",
    "telecom", "energy", "oil", "gas", "coal", "mining", "agriculture",
    "exports", "imports", "fdi", "forex", "commodity", "gold", "silver",
    "crypto", "blockchain", "fintech", "digital payment", "upi", "bank"
]

def scrape_economic_times_business():
    try:
        session = get_session()
        url = "https://economictimes.indiatimes.com/news/economy/policy"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        selectors = ['.eachStory h3 a', '.story-box h4 a', 'h3 a', 'h2 a', '.contentSec h3 a']
        seen_titles = set()
        for selector in selectors:
            for tag in soup.select(selector):
                title = clean_title(tag.get_text())
                href = tag.get('href', '')
                if title and title not in seen_titles and href:
                    if href.startswith('/'):
                        href = "https://economictimes.indiatimes.com" + href
                    elif not href.startswith('http'):
                        continue
                    articles.append({"title": title, "url": href, "source": "Economic Times"})
                    seen_titles.add(title)
        return articles
    except Exception as e:
        print(f"Error scraping Economic Times Business: {e}")
        return []

def scrape_business_standard_finance():
    try:
        session = get_session()
        url = "https://www.business-standard.com/economy"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        selectors = ['.headline a', '.cardlist h2 a', 'h3 a', '.listing-news h4 a']
        seen_titles = set()
        for selector in selectors:
            for tag in soup.select(selector):
                title = clean_title(tag.get_text())
                href = tag.get('href', '')
                if title and title not in seen_titles and href:
                    if href.startswith('/'):
                        href = "https://www.business-standard.com" + href
                    elif not href.startswith('http'):
                        continue
                    articles.append({"title": title, "url": href, "source": "Business Standard"})
                    seen_titles.add(title)
        return articles
    except Exception as e:
        print(f"Error scraping Business Standard Finance: {e}")
        return []

def scrape_moneycontrol_business():
    try:
        session = get_session()
        url = "https://www.moneycontrol.com/news/business/"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        selectors = ['.news_title a', '.FL h2 a', 'h3 a', '.news-item h4 a']
        seen_titles = set()
        for selector in selectors:
            for tag in soup.select(selector):
                title = clean_title(tag.get_text())
                href = tag.get('href', '')
                if title and title not in seen_titles and href:
                    if href.startswith('/'):
                        href = "https://www.moneycontrol.com" + href
                    elif not href.startswith('http'):
                        continue
                    articles.append({"title": title, "url": href, "source": "MoneyControl"})
                    seen_titles.add(title)
        return articles
    except Exception as e:
        print(f"Error scraping MoneyControl Business: {e}")
        return []

def scrape_financial_express_business():
    try:
        session = get_session()
        url = "https://www.financialexpress.com/economy/"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        selectors = ['.entry-title a', '.listitembx h3 a', 'h2 a', '.title a', '.main-story h3 a']
        seen_titles = set()
        skip_keywords = ['related-news', 'photos', 'latest-news']
        for selector in selectors:
            for tag in soup.select(selector):
                title = clean_title(tag.get_text())
                href = tag.get('href', '')
                if any(kw in href for kw in skip_keywords):
                    continue
                if title and title not in seen_titles and href:
                    if href.startswith('/'):
                        href = "https://www.financialexpress.com" + href
                    elif not href.startswith('http'):
                        continue
                    articles.append({"title": title, "url": href, "source": "Financial Express"})
                    seen_titles.add(title)
        return articles
    except Exception as e:
        print(f"Error scraping Financial Express Business: {e}")
        return []

def scrape_mint_business():
    try:
        session = get_session()
        url = "https://www.livemint.com/economy"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        selectors = ['h2 a', 'h3 a', '.headline a', '.listView h4 a']
        seen_titles = set()
        for selector in selectors:
            for tag in soup.select(selector):
                title = clean_title(tag.get_text())
                href = tag.get('href', '')
                if title and title not in seen_titles and href:
                    if href.startswith('/'):
                        href = "https://www.livemint.com" + href
                    elif not href.startswith('http'):
                        continue
                    articles.append({"title": title, "url": href, "source": "Mint"})
                    seen_titles.add(title)
        return articles
    except Exception as e:
        print(f"Error scraping Mint Business: {e}")
        return []

def scrape_hindustan_times_business():
    try:
        session = get_session()
        url = "https://www.hindustantimes.com/business"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        selectors = ['.hdg3 a', 'h3 a', 'h2 a', '.media-heading a', '.story-title a']
        seen_titles = set()
        for selector in selectors:
            for tag in soup.select(selector):
                title = clean_title(tag.get_text())
                href = tag.get('href', '')
                if title and title not in seen_titles and href:
                    if href.startswith('/'):
                        href = "https://www.hindustantimes.com" + href
                    elif not href.startswith('http'):
                        continue
                    articles.append({"title": title, "url": href, "source": "Hindustan Times"})
                    seen_titles.add(title)
        return articles
    except Exception as e:
        print(f"Error scraping Hindustan Times Business: {e}")
        return []

def scrape_ndtv_business():
    try:
        session = get_session()
        url = "https://www.ndtv.com/business"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        selectors = ['.newsHdng a', '.SrchLstPg_ttl-lnk a', 'h2 a', 'h3 a', '.story-title a']
        seen_titles = set()
        for selector in selectors:
            for tag in soup.select(selector):
                title = clean_title(tag.get_text())
                href = tag.get('href', '')
                if title and title not in seen_titles and href:
                    if href.startswith('/'):
                        href = "https://www.ndtv.com" + href
                    elif not href.startswith('http'):
                        continue
                    articles.append({"title": title, "url": href, "source": "NDTV"})
                    seen_titles.add(title)
        return articles
    except Exception as e:
        print(f"Error scraping NDTV Business: {e}")
        return []

def scrape_deccan_herald_business():
    try:
        session = get_session()
        url = "https://www.deccanherald.com/business"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        selectors = ['a .headline', '.article-title a', 'h2 a', 'h3 a', '.story-title a']
        seen_titles = set()
        for selector in selectors:
            for tag in soup.select(selector):
                a_tag = tag.find_parent('a') if tag.name != 'a' else tag
                if not a_tag:
                    continue
                title = clean_title(tag.get_text())
                href = a_tag.get('href', '')
                if title and title not in seen_titles and href:
                    if href.startswith('/'):
                        href = "https://www.deccanherald.com" + href
                    elif not href.startswith('http'):
                        continue
                    articles.append({"title": title, "url": href, "source": "Deccan Herald"})
                    seen_titles.add(title)
        return articles
    except Exception as e:
        print(f"Error scraping Deccan Herald Business: {e}")
        return []

def scrape_indian_express_business():
    try:
        session = get_session()
        url = "https://indianexpress.com/section/business/"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        selectors = ['h3 a', 'h2 a', '.story-title a']
        seen_titles = set()
        for selector in selectors:
            for tag in soup.select(selector):
                title = clean_title(tag.get_text())
                href = tag.get('href', '')
                if title and title not in seen_titles and href:
                    if href.startswith('/'):
                        href = "https://indianexpress.com" + href
                    elif not href.startswith('http'):
                        continue
                    articles.append({"title": title, "url": href, "source": "Indian Express"})
                    seen_titles.add(title)
        return articles
    except Exception as e:
        print(f"Error scraping Indian Express Business: {e}")
        return []

# --- Global Business & Finance Sources ---

def scrape_reuters_business_global():
    try:
        session = get_session()
        url = "https://www.reuters.com/business/"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        seen_titles = set()

        # Target story headline links
        for tag in soup.select('a[data-testid="Heading"]'):
            title = clean_title(tag.get_text())
            href = tag.get('href', '')

            if title and href and title not in seen_titles:
                if href.startswith('/'):
                    href = "https://www.reuters.com" + href
                
                articles.append({"title": title, "url": href, "source": "Reuters"})
                seen_titles.add(title)
                
        return articles
    except Exception as e:
        print(f"Error scraping Reuters Business: {e}")
        return []

def scrape_bloomberg_business_global():
    try:
        session = get_session()
        articles = []
        seen_titles = set()

        urls = [
            "https://www.bloomberg.com/business",
            "https://www.bloomberg.com/markets"
        ]

        for url in urls:
            print(f"Scraping Bloomberg page: {url}")
            response = session.get(url, timeout=15)
            soup = BeautifulSoup(response.content, "html.parser")

            # Bloomberg story headlines
            for tag in soup.select('a[href*="/news/articles/"]'):
                title = clean_title(tag.get_text())
                href = tag.get('href', '')

                if title and href and title not in seen_titles:
                    if href.startswith('/'):
                        href = "https://www.bloomberg.com" + href
                    
                    articles.append({"title": title, "url": href, "source": "Bloomberg"})
                    seen_titles.add(title)
            
            time.sleep(1) # Be polite to the server

        return articles
    except Exception as e:
        print(f"Error scraping Bloomberg Business: {e}")
        return []

def scrape_financial_times_global():
    try:
        session = get_session()
        url = "https://www.ft.com/companies"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        seen_titles = set()

        # Target headline links
        for tag in soup.select('a[data-trackable="heading-link"]'):
            title = clean_title(tag.get_text())
            href = tag.get('href', '')

            if title and href and title not in seen_titles:
                if href.startswith('/'):
                    href = "https://www.ft.com" + href
                
                articles.append({"title": title, "url": href, "source": "Financial Times"})
                seen_titles.add(title)
                
        return articles
    except Exception as e:
        print(f"Error scraping Financial Times: {e}")
        return []

def scrape_cnbc_business_global():
    try:
        session = get_session()
        url = "https://www.cnbc.com/business/"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        seen_titles = set()

        # Target article headline links
        selectors = ['.Card-headline a', '.InlineArticleHeadline a', 'h3 a', 'h2 a']
        for selector in selectors:
            for tag in soup.select(selector):
                title = clean_title(tag.get_text())
                href = tag.get('href', '')

                if title and href and title not in seen_titles:
                    if href.startswith('/'):
                        href = "https://www.cnbc.com" + href
                    
                    articles.append({"title": title, "url": href, "source": "CNBC"})
                    seen_titles.add(title)

        return articles
    except Exception as e:
        print(f"Error scraping CNBC Business: {e}")
        return []

def scrape_wall_street_journal_global():
    try:
        session = get_session()
        url = "https://www.wsj.com/news/business"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        seen_titles = set()

        # WSJ headline links
        for tag in soup.select('h3 a, h2 a'):
            title = clean_title(tag.get_text())
            href = tag.get('href', '')

            # Basic validation for an article link
            if title and href and '/articles/' in href and title not in seen_titles:
                if href.startswith('/'):
                    href = "https://www.wsj.com" + href
                
                articles.append({"title": title, "url": href, "source": "Wall Street Journal"})
                seen_titles.add(title)
                
        return articles
    except Exception as e:
        print(f"Error scraping Wall Street Journal: {e}")
        return []

def scrape_times_higher_education_business_global():
    try:
        session = get_session()
        url = "https://www.timeshighereducation.com/news/business"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        seen_titles = set()

        # Each article is in an 'a' tag that contains the title in a 'h3' tag.
        for tag in soup.select('a[data-position="teaser-card"]'):
            title_tag = tag.find('h3', class_='teaser-card__title')
            if not title_tag:
                continue
                
            title = clean_title(title_tag.get_text())
            href = tag.get('href', '')

            if title and href and title not in seen_titles:
                if not href.startswith('http'):
                    href = "https://www.timeshighereducation.com" + href
                
                articles.append({"title": title, "url": href, "source": "Times Higher Education"})
                seen_titles.add(title)
                
        return articles
    except Exception as e:
        print(f"Error scraping Times Higher Education Business: {e}")
        return []

def scrape_guardian_business_global():
    try:
        session = get_session()
        url = "https://www.theguardian.com/business"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        seen_titles = set()

        # Target <a> tags with an 'aria-label' as it contains the title.
        for tag in soup.select('a[aria-label]'):
            title = clean_title(tag.get('aria-label'))
            href = tag.get('href', '')

            # Basic validation for an article link
            if title and href and '/202' in href and title not in seen_titles:
                if not href.startswith('http'):
                    href = "https://www.theguardian.com" + href
                
                articles.append({"title": title, "url": href, "source": "The Guardian"})
                seen_titles.add(title)
                
        return articles
    except Exception as e:
        print(f"Error scraping Guardian Business: {e}")
        return []

def scrape_business_finance_news(region="India", sources=None):
    all_articles = []
    
    india_source_map = {
        "economic_times": scrape_economic_times_business,
        "business_standard": scrape_business_standard_finance,
        "moneycontrol": scrape_moneycontrol_business,
        "financial_express": scrape_financial_express_business,
        "mint": scrape_mint_business,
        "hindustan_times": scrape_hindustan_times_business,
        "ndtv": scrape_ndtv_business,
        "deccan_herald": scrape_deccan_herald_business,
        "indian_express": scrape_indian_express_business,
    }
    
    global_source_map = {
        "reuters": scrape_reuters_business_global,
        "bloomberg": scrape_bloomberg_business_global,
        "financial_times": scrape_financial_times_global,
        "cnbc": scrape_cnbc_business_global,
        "wall_street_journal": scrape_wall_street_journal_global,
        "times_higher_education": scrape_times_higher_education_business_global,
        "guardian": scrape_guardian_business_global,
    }

    if region == "India":
        source_map = india_source_map
    else: # Global
        source_map = global_source_map

    if sources is None:
        sources = list(source_map.keys())

    for src in sources:
        func = source_map.get(src)
        if func:
            try:
                src_articles = func()
                print(f"Business & Finance ({region} - {src}): {len(src_articles)} articles")
                all_articles.extend(src_articles)
                time.sleep(1)  # Be polite between source requests
            except Exception as e:
                print(f"Error in scrape_business_finance_news for source {src}: {e}")

    # Remove duplicates based on title
    unique_articles = []
    seen_titles = set()
    for article in all_articles:
        title_lower = article['title'].lower()
        if title_lower not in seen_titles:
            unique_articles.append(article)
            seen_titles.add(title_lower)
    
    return unique_articles

if __name__ == "__main__":
    print("--- Scraping India Business & Finance ---")
    india_articles = scrape_business_finance_news(region="India")
    for i, art in enumerate(india_articles, 1):
        print(f"{i}. {art['title']} ({art['source']})\n   {art['url']}\n")

    print("\n--- Scraping Global Business & Finance ---")
    global_articles = scrape_business_finance_news(region="Global")
    for i, art in enumerate(global_articles, 1):
        print(f"{i}. {art['title']} ({art['source']})\n   {art['url']}\n")
    
    print(f"\nTotal India Articles: {len(india_articles)}")
    print(f"Total Global Articles: {len(global_articles)}")
    print(f"Grand Total: {len(india_articles) + len(global_articles)}")