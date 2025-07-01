import time
import requests
from time import sleep
from bs4 import BeautifulSoup

def clean_text(text: str) -> str:
    return ' '.join(text.strip().split())

def get_http_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0"})
    return session

def normalize_title(title: str) -> str:
    return clean_text(title.replace("\n", " ").replace("\xa0", " "))

def ensure_absolute_url(url: str) -> str:
    if url.startswith(('http://', 'https://')):
        return url
    return f"https://www.euronews.com/{url.lstrip('/')}"

environment_keywords = [
    "climate", "pollution", "wildlife", "forest", "biodiversity", "ecosystem",
    "carbon", "green", "ozone", "plastic", "waste", "recycle", "emissions",
    "sustainability", "deforestation", "air quality", "smog", "temperature",
    "global warming", "greenhouse", "rainfall", "heatwave", "flood", "drought",
    "clean energy", "solar", "hydro", "renewable", "sea level", "melting",
    "ganga", "yamuna", "swachh", "pcb", "delhi", "tribal", "van", "eia",
    "moefcc", "wetland", "mangrove", "tree plantation", "biosphere", "earth",
    "nature", "natural disaster", "sanctuary", "project tiger", "plastic ban",
    "pollution control board", "jal shakti", "climate action", "unfccc", "paris agreement"
]

# Add this to the list of country names except India
COUNTRY_KEYWORDS = [
    'afghanistan', 'albania', 'algeria', 'andorra', 'angola', 'argentina', 'armenia', 'australia', 'austria',
    'azerbaijan', 'bahamas', 'bahrain', 'bangladesh', 'barbados', 'belarus', 'belgium', 'belize', 'benin',
    'bhutan', 'bolivia', 'bosnia', 'botswana', 'brazil', 'brunei', 'bulgaria', 'burkina', 'burundi', 'cambodia',
    'cameroon', 'canada', 'cape verde', 'central african republic', 'chad', 'chile', 'china', 'colombia',
    'comoros', 'congo', 'costa rica', 'croatia', 'cuba', 'cyprus', 'czech', 'denmark', 'djibouti', 'dominica',
    'dominican republic', 'east timor', 'ecuador', 'egypt', 'el salvador', 'equatorial guinea', 'eritrea',
    'estonia', 'eswatini', 'ethiopia', 'fiji', 'finland', 'france', 'gabon', 'gambia', 'georgia', 'germany',
    'ghana', 'greece', 'grenada', 'guatemala', 'guinea', 'guinea-bissau', 'guyana', 'haiti', 'honduras',
    'hungary', 'iceland', 'indonesia', 'iran', 'iraq', 'ireland', 'israel', 'italy', 'ivory coast', 'jamaica',
    'japan', 'jordan', 'kazakhstan', 'kenya', 'kiribati', 'korea', 'kosovo', 'kuwait', 'kyrgyzstan', 'laos',
    'latvia', 'lebanon', 'lesotho', 'liberia', 'libya', 'liechtenstein', 'lithuania', 'luxembourg', 'madagascar',
    'malawi', 'malaysia', 'maldives', 'mali', 'malta', 'marshall islands', 'mauritania', 'mauritius', 'mexico',
    'micronesia', 'moldova', 'monaco', 'mongolia', 'montenegro', 'morocco', 'mozambique', 'myanmar', 'namibia',
    'nauru', 'nepal', 'netherlands', 'new zealand', 'nicaragua', 'niger', 'nigeria', 'north macedonia',
    'norway', 'oman', 'pakistan', 'palau', 'palestine', 'panama', 'papua new guinea', 'paraguay', 'peru',
    'philippines', 'poland', 'portugal', 'qatar', 'romania', 'russia', 'rwanda', 'saint kitts', 'saint lucia',
    'saint vincent', 'samoa', 'san marino', 'sao tome', 'saudi arabia', 'senegal', 'serbia', 'seychelles',
    'sierra leone', 'singapore', 'slovakia', 'slovenia', 'solomon islands', 'somalia', 'south africa',
    'south sudan', 'spain', 'sri lanka', 'sudan', 'suriname', 'sweden', 'switzerland', 'syria', 'taiwan',
    'tajikistan', 'tanzania', 'thailand', 'togo', 'tonga', 'trinidad', 'tunisia', 'turkey', 'turkmenistan',
    'tuvalu', 'uganda', 'ukraine', 'united arab emirates', 'united kingdom', 'uk', 'usa', 'united states',
    'uruguay', 'uzbekistan', 'vanuatu', 'vatican', 'venezuela', 'vietnam', 'yemen', 'zambia', 'zimbabwe'
]

def filter_non_india_articles(title):
    title_lower = title.lower()
    for country in COUNTRY_KEYWORDS:
        if country in title_lower:
            return False
    return True

#--------INDIAN NEWS-------------------

def scrape_deccan_herald():
    try:
        session = get_http_session()
        url = "https://www.deccanherald.com/environment"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = []
        seen_titles = set()
        for a_tag in soup.find_all('a', href=True):
            card = a_tag.find('div', class_='story-card-15')
            if not card:
                continue
            headline = card.find('h2', class_='headline')
            if not headline:
                continue
            title = normalize_title(headline.text)
            if not title or title in seen_titles:
                continue
            href = a_tag['href']
            full_url = f"https://www.deccanherald.com{href}" if href.startswith('/') else href
            articles.append({"title": title, "url": full_url, "source": "Deccan Herald"})
            seen_titles.add(title)
        return articles
    except Exception as e:
        print(f"Error scraping Deccan Herald: {e}")
        return []


def scrape_indian_express():
    try:
        session = get_http_session()
        url = "https://indianexpress.com/about/environment/"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        seen_titles = set()
        for h3 in soup.find_all('h3'):
            a_tag = h3.find('a', href=True)
            if not a_tag:
                continue
            title = normalize_title(a_tag.get_text())
            href = a_tag['href']
            if '/environment/' not in href:
                continue
            if not title or title in seen_titles:
                continue
            articles.append({"title": title, "url": href, "source": "Indian Express"})
            seen_titles.add(title)
        return articles
    except Exception as e:
        print(f"Error scraping Indian Express: {e}")
        return []

def scrape_ndtv():
    try:
        session = get_http_session()
        url = "https://www.ndtv.com/environment"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        seen_titles = set()
        for div in soup.find_all('div', class_='NwsLstPg_txt-wrp'):
            a_tag = div.find('a', class_='NwsLstPg_ttl', href=True)
            if not a_tag:
                continue
            title = normalize_title(a_tag.get_text())
            href = a_tag['href']
            if not title or title in seen_titles:
                continue
            articles.append({"title": title, "url": href, "source": "NDTV"})
            seen_titles.add(title)
        return articles
    except Exception as e:
        print(f"Error scraping NDTV: {e}")
        return []

def scrape_hindustan_times_environment():
    try:
        session = get_http_session()
        url = "https://www.hindustantimes.com/environment"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        seen_titles = set()
        for h3 in soup.find_all('h3', class_='hdg3'):
            a_tag = h3.find('a', href=True)
            if not a_tag:
                continue
            title = normalize_title(a_tag.get_text())
            href = a_tag['href']
            if not title or title in seen_titles:
                continue
            # Filter out articles mentioning any country except India
            if not filter_non_india_articles(title):
                continue
            full_url = f"https://www.hindustantimes.com{href}" if href.startswith('/') else href
            articles.append({"title": title, "url": full_url, "source": "Hindustan Times"})
            seen_titles.add(title)
        return articles
    except Exception as e:
        print(f"Error scraping Hindustan Times Environment: {e}")
        return []

def scrape_times_of_india_environment():
    try:
        session = get_http_session()
        url = "https://timesofindia.indiatimes.com/home/environment"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        seen_titles = set()
        for span in soup.find_all('span', class_='w_tle'):
            a_tag = span.find('a', href=True, title=True)
            if not a_tag:
                continue
            title = normalize_title(a_tag.get_text())
            href = a_tag['href']
            if not title or title in seen_titles:
                continue
            # Filter out articles mentioning any country except India
            if not filter_non_india_articles(title):
                continue
            full_url = f"https://timesofindia.indiatimes.com{href}" if href.startswith('/') else href
            articles.append({"title": title, "url": full_url, "source": "Times of India"})
            seen_titles.add(title)
        return articles
    except Exception as e:
        print(f"Error scraping Times of India Environment: {e}")
        return []

def scrape_the_hindu_environment():
    try:
        session = get_http_session()
        articles = []
        seen_titles = set()
        for page in range(1, 6):  # Pages 1 to 5
            url = f"https://www.thehindu.com/sci-tech/energy-and-environment/?page={page}"
            response = session.get(url, timeout=15)
            soup = BeautifulSoup(response.content, "html.parser")
            for h3 in soup.find_all("h3", class_="title big"):
                a_tag = h3.find("a", href=True)
                if not a_tag:
                    continue
                title = normalize_title(a_tag.get_text())
                href = a_tag["href"]
                if not title or title in seen_titles:
                    continue
                # Filter out articles mentioning any country except India
                if not filter_non_india_articles(title):
                    continue
                articles.append({"title": title, "url": href, "source": "The Hindu"})
                seen_titles.add(title)
        return articles
    except Exception as e:
        print(f"Error scraping The Hindu Environment: {e}")
        return []

#--------GLOBAL NEWS-------------------


def scrape_cnbc():
    url = "https://www.cnbc.com/environment/"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        articles = []
        seen_titles = set()
        for card in soup.find_all("div", attrs={"data-test": "Card"}):
            title_tag = card.find("a", class_="Card-title")
            if title_tag and title_tag.text and title_tag['href']:
                title = clean_text(title_tag.text)
                href = title_tag['href']
                if title not in seen_titles:
                    articles.append({"title": title, "url": href, "source": "CNBC"})
                    seen_titles.add(title)
        return articles
    except Exception:
        return []

def scrape_euronews(query="environment", max_pages=3, delay=0.3):
    api_url = "https://www.euronews.com/api/search"
    headers = {"User-Agent": "Mozilla/5.0"}
    articles = []
    for page in range(1, max_pages + 1):
        params = {"query": query, "page": page, "size": 10}
        try:
            res = requests.get(api_url, headers=headers, params=params, timeout=15)
            res.raise_for_status()
            results = res.json()
            if not isinstance(results, list) or not results:
                break
        except Exception:
            break
        for item in results:
            title = clean_text(item.get("title", ""))
            url = ensure_absolute_url(item.get("url", ""))
            if title and url:
                articles.append({"title": title, "url": url, "source": "Euronews"})
        sleep(delay)
    return articles

def scrape_guardian():
    try:
        session = get_http_session()
        url = "https://www.theguardian.com/environment"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        seen_titles = set()
        for tag in soup.select('a[aria-label]'):
            title = normalize_title(tag.get("aria-label"))
            href = tag.get("href", "")
            if title and href and "/202" in href and title not in seen_titles:
                full_url = href if href.startswith("http") else "https://www.theguardian.com" + href
                articles.append({"title": title, "url": full_url, "source": "The Guardian"})
                seen_titles.add(title)
        return articles
    except Exception:
        return []


def scrape_environment_news(region="India", sources=None):
    india_source_map = {
        "deccan_herald": scrape_deccan_herald,
        "indian_express": scrape_indian_express,
        "ndtv": scrape_ndtv,
        "hindustan_times": scrape_hindustan_times_environment,
        "times_of_india": scrape_times_of_india_environment,
        "the_hindu": scrape_the_hindu_environment,
    }
    global_source_map = {
        "euronews": scrape_euronews,
        "cnbc": scrape_cnbc,
        "guardian": scrape_guardian,
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
                # euronews takes a query, others do not
                src_articles = func() if src != "euronews" else func()
                all_articles.extend(src_articles)
            except Exception as e:
                print(f"Error in scrape_environment_news for source {src}: {e}")
    return all_articles

if __name__ == "__main__":
    print("--- Scraping India Environment News ---")
    india_articles = scrape_environment_news(region="India")
    for i, art in enumerate(india_articles, 1):
        print(f"{i}. {art['title']} ({art['source']})\n   {art['url']}\n")

    print("\n--- Scraping Global Environment News ---")
    global_articles = scrape_environment_news(region="Global")
    for i, art in enumerate(global_articles, 1):
        print(f"{i}. {art['title']} ({art['source']})\n   {art['url']}\n")