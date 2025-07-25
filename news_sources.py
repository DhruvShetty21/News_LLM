# news_sources.py
import requests
from bs4 import BeautifulSoup
import time
import re


def get_session():
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    })
    return session


def clean_title(title):
    if not title:
        return None
    title = re.sub(r'\s+', ' ', title.strip())
    if len(title) < 10 or len(title) > 200:
        return None
    # Filter out navigation items and ads
    skip_words = ['subscribe', 'login', 'register', 'advertisement', 'menu', 'search', 'newsletter']
    if any(word in title.lower() for word in skip_words):
        return None
    return title



def scrape_flipboard(region="India"):
    try:
        session = get_session()
        session.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://flipboard.com/',
            'DNT': '1',
        })

        if region == "India":
            url = "https://flipboard.com/topic/educationindia"
        else:
            url = "https://flipboard.com/topic/education"

        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []

        # Try multiple selectors for Flipboard's evolving structure
        for item in soup.select('a[href*="/story/"], a.article-link, div.article, article.story'):
            link = item if item.name == 'a' else item.find('a', href=True)
            if not link:
                continue

            title_tag = link.find('h2') or link.find('div', class_='title') or link
            title = clean_title(title_tag.get_text())
            if not title:
                continue

            href = link['href']
            if not href.startswith('http'):
                href = "https://flipboard.com" + href

            articles.append({
                "title": title,
                "url": href,
                "source": "Flipboard"
            })

        return articles
    except Exception as e:
        print(f"Error scraping Flipboard: {e}")
        return []

def scrape_scoopit(region="India"):
    try:
        session = get_session()
        session.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.scoop.it/',
            'DNT': '1',
        })

        if region == "India":
            topics = ["education-in-india", "indian-education-system"]
        else:
            topics = ["education-news", "higher-education-today", "global-education"]

        articles = []
        for topic in topics:
            url = f"https://www.scoop.it/topic/{topic}"
            response = session.get(url, timeout=15)
            soup = BeautifulSoup(response.content, "html.parser")

            # More robust selector
            for item in soup.select('[class*="postItem"]'):
                title_tag = item.find('h2') or item.find('h3') or item.find(class_='title')
                if not title_tag:
                    continue

                title = clean_title(title_tag.get_text())
                if not title:
                    continue

                link = item.find('a', href=True)
                if not link:
                    continue

                href = link['href']
                if href.startswith('/'):
                    href = "https://www.scoop.it" + href

                articles.append({
                    "title": title,
                    "url": href,
                    "source": "Scoop.it"
                })

        return articles[:15]
    except Exception as e:
        print(f"Error scraping Scoop.it: {e}")
        return []
        #Indian News Sources
def scrape_hindustan_times():
    try:
        session = get_session()
        url = "https://www.hindustantimes.com/education"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []

        selectors = ['h3 a', 'h2 a', '.story-box a', '.listView a', '.story-title a']

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
        print(f"Error scraping Hindustan Times: {e}")
        return []

# ...existing code...

def scrape_times_of_india(sources=None):
    try:
        session = get_session()
        url = "https://timesofindia.indiatimes.com/education"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        seen_titles = set()
        # Determine the max articles based on sources
        if sources and isinstance(sources, list) and len(sources) == 1 and sources[0] == "times_of_india":
            MAX_ARTICLES = 60
        else:
            MAX_ARTICLES = 40

        # Primary pattern: Articles in div with class "lSIdy col_l_6 col_m_6"
        for div in soup.select('div.lSIdy.col_l_6.col_m_6'):
            for a_tag in div.find_all('a', href=True):
                span_tag = a_tag.find('span')
                if span_tag:
                    title = clean_title(span_tag.get_text())
                    href = a_tag.get('href', '')

                    if title and title not in seen_titles and href:
                        href = href.split('?')[0]
                        if href.startswith('/'):
                            href = "https://timesofindia.indiatimes.com" + href
                        elif not href.startswith('http'):
                            continue
                        articles.append({"title": title, "url": href, "source": "Times of India"})
                        seen_titles.add(title)
                        if len(articles) >= MAX_ARTICLES:
                            print(f"Times of India scraper found {len(articles)} articles (limit reached)")
                            return articles

        # Secondary pattern: Articles with figcaption and p tags
        for a_tag in soup.find_all('a', href=True):
            if len(articles) >= MAX_ARTICLES:
                print(f"Times of India scraper found {len(articles)} articles (limit reached)")
                return articles
            figcaption = a_tag.find('figcaption')
            if figcaption:
                title = clean_title(figcaption.get_text())
                href = a_tag.get('href', '')
                if title and title not in seen_titles and href and 'education' in href:
                    href = href.split('?')[0]
                    if href.startswith('/'):
                        href = "https://timesofindia.indiatimes.com" + href
                    elif not href.startswith('http'):
                        continue
                    articles.append({"title": title, "url": href, "source": "Times of India"})
                    seen_titles.add(title)

        # Alternative pattern: Look for general education section links with class "linktype1"
        for a_tag in soup.select('a.linktype1[href*="education"]'):
            if len(articles) >= MAX_ARTICLES:
                print(f"Times of India scraper found {len(articles)} articles (limit reached)")
                return articles
            span_tag = a_tag.find('span')
            if span_tag:
                title = clean_title(span_tag.get_text())
                href = a_tag.get('href', '')
                if title and title not in seen_titles and href:
                    href = href.split('?')[0]
                    if href.startswith('/'):
                        href = "https://timesofindia.indiatimes.com" + href
                    elif not href.startswith('http'):
                        continue
                    articles.append({"title": title, "url": href, "source": "Times of India"})
                    seen_titles.add(title)

        print(f"Times of India scraper found {len(articles)} articles")
        return articles

    except Exception as e:
        print(f"Error scraping Times of India: {e}")
        return []

def scrape_indian_express_education():
    try:
        session = get_session()
        url = "https://indianexpress.com/section/education/"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []

        selectors = ['.title a', 'h2 a', '.articles a', '.entry-title a']

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
        print(f"Error scraping Indian Express: {e}")
        return []

def scrape_the_hindu_education():
    try:
        session = get_session()
        url = "https://www.thehindu.com/education/"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []

        selectors = ['.title a', 'h2 a', 'h3 a', '.story-card-news a']

        seen_titles = set()
        for selector in selectors:
            for tag in soup.select(selector):
                title = clean_title(tag.get_text())
                href = tag.get('href', '')

                if title and title not in seen_titles and href:
                    if href.startswith('/'):
                        href = "https://www.thehindu.com" + href
                    elif not href.startswith('http'):
                        continue

                    articles.append({"title": title, "url": href, "source": "The Hindu"})
                    seen_titles.add(title)

        return articles
    except Exception as e:
        print(f"Error scraping The Hindu: {e}")
        return []

def scrape_deccan_herald_education():
    try:
        session = get_session()
        url = "https://www.deccanherald.com/education"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []

        selectors = ['.article-title a', 'h2 a', 'h3 a', '.story-title a']

        seen_titles = set()
        for selector in selectors:
            for tag in soup.select(selector):
                title = clean_title(tag.get_text())
                href = tag.get('href', '')

                if title and title not in seen_titles and href:
                    if href.startswith('/'):
                        href = "https://www.deccanherald.com" + href
                    elif not href.startswith('http'):
                        continue

                    articles.append({"title": title, "url": href, "source": "Deccan Herald"})
                    seen_titles.add(title)

        return articles
    except Exception as e:
        print(f"Error scraping Deccan Herald: {e}")
        return []

def scrape_ndtv_education():
    try:
        session = get_session()
        url = "https://www.ndtv.com/education"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []

        selectors = ['.newsHdng a', 'h2 a', 'h1 a', '.news-title a']

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
        print(f"Error scraping NDTV: {e}")
        return []

def scrape_financial_express_education(max_pages=5):
    try:
        session = get_session()
        articles = []
        seen_titles = set()
        MAX_ARTICLES = 30

        for page in range(1, max_pages + 1):
            if len(articles) >= MAX_ARTICLES:
                print(f"Financial Express scraper found {len(articles)} articles (limit reached)")
                return articles
            if page == 1:
                url = "https://www.financialexpress.com/about/education/"
            else:
                url = f"https://www.financialexpress.com/about/education/page/{page}/"
            response = session.get(url, timeout=15)
            soup = BeautifulSoup(response.content, "html.parser")
            for entry in soup.select('div.entry-wrapper'):
                if len(articles) >= MAX_ARTICLES:
                    print(f"Financial Express scraper found {len(articles)} articles (limit reached)")
                    return articles
                title_tag = entry.select_one('div.entry-title a')
                if not title_tag:
                    continue
                title = clean_title(title_tag.get_text())
                href = title_tag.get('href', '')
                if title and title not in seen_titles and href:
                    articles.append({"title": title, "url": href, "source": "Financial Express"})
                    seen_titles.add(title)
        print(f"Financial Express scraper found {len(articles)} articles")
        return articles
    except Exception as e:
        print(f"Error scraping Financial Express: {e}")
        return []

def scrape_bbc_education():
    try:
        session = get_session()
        url = "https://www.bbc.com/news/education"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []

        selectors = ['h3 a', 'h2 a', '.gel-layout__item a', '.media__content a']

        seen_titles = set()
        for selector in selectors:
            for tag in soup.select(selector):
                title = clean_title(tag.get_text())
                href = tag.get('href', '')

                if title and title not in seen_titles and href:
                    if href.startswith('/'):
                        href = "https://www.bbc.com" + href
                    elif not href.startswith('http'):
                        continue

                    articles.append({"title": title, "url": href, "source": "BBC"})
                    seen_titles.add(title)

        return articles
    except Exception as e:
        print(f"Error scraping BBC: {e}")
        return []

def scrape_guardian_education():
    try:
        session = get_session()
        url = "https://www.theguardian.com/education"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []

        selectors = ['.fc-item__title a', '.u-faux-block-link__overlay', 'h3 a']

        seen_titles = set()
        for selector in selectors:
            for tag in soup.select(selector):
                title = clean_title(tag.get_text())
                href = tag.get('href', '')

                if title and title not in seen_titles and href:
                    if href.startswith('/'):
                        href = "https://www.theguardian.com" + href
                    elif not href.startswith('http'):
                        continue

                    articles.append({"title": title, "url": href, "source": "The Guardian"})
                    seen_titles.add(title)

        return articles
    except Exception as e:
        print(f"Error scraping Guardian: {e}")
        return []

def scrape_nytimes_education():
    try:
        session = get_session()
        url = "https://www.nytimes.com/section/education"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []

        selectors = ['h3 a', 'h2 a', '.css-1l4spti a']

        seen_titles = set()
        for selector in selectors:
            for tag in soup.select(selector):
                title = clean_title(tag.get_text())
                href = tag.get('href', '')

                if title and title not in seen_titles and href:
                    if href.startswith('/'):
                        href = "https://www.nytimes.com" + href
                    elif not href.startswith('http'):
                        continue

                    articles.append({"title": title, "url": href, "source": "NY Times"})
                    seen_titles.add(title)

        return articles
    except Exception as e:
        print(f"Error scraping NY Times: {e}")
        return []

def scrape_washington_post_education():
    try:
        session = get_session()
        url = "https://www.washingtonpost.com/education/"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []

        selectors = ['h3 a', 'h2 a', '.headline a', '.title a']

        seen_titles = set()
        for selector in selectors:
            for tag in soup.select(selector):
                title = clean_title(tag.get_text())
                href = tag.get('href', '')

                if title and title not in seen_titles and href:
                    if href.startswith('/'):
                        href = "https://www.washingtonpost.com" + href
                    elif not href.startswith('http'):
                        continue

                    articles.append({"title": title, "url": href, "source": "Washington Post"})
                    seen_titles.add(title)

        return articles
    except Exception as e:
        print(f"Error scraping Washington Post: {e}")
        return []

def scrape_telegraph_education():
    try:
        session = get_session()
        url = "https://www.telegraph.co.uk/education/"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []

        selectors = ['h3 a', 'h2 a', '.list-headline a', '.card__heading a']

        seen_titles = set()
        for selector in selectors:
            for tag in soup.select(selector):
                title = clean_title(tag.get_text())
                href = tag.get('href', '')

                if title and title not in seen_titles and href:
                    if href.startswith('/'):
                        href = "https://www.telegraph.co.uk" + href
                    elif not href.startswith('http'):
                        continue

                    articles.append({"title": title, "url": href, "source": "The Telegraph"})
                    seen_titles.add(title)

        return articles
    except Exception as e:
        print(f"Error scraping Telegraph: {e}")
        return []

def scrape_times_higher_education():
    try:
        session = get_session()
        url = "https://www.timeshighereducation.com/news"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []

        selectors = ['h3 a', 'h2 a', '.views-field-title a', '.article-title a']

        seen_titles = set()
        for selector in selectors:
            for tag in soup.select(selector):
                title = clean_title(tag.get_text())
                href = tag.get('href', '')

                if title and title not in seen_titles and href:
                    if href.startswith('/'):
                        href = "https://www.timeshighereducation.com" + href
                    elif not href.startswith('http'):
                        continue

                    articles.append({"title": title, "url": href, "source": "Times Higher Education"})
                    seen_titles.add(title)

        return articles
    except Exception as e:
        print(f"Error scraping Times Higher Education: {e}")
        return []

def scrape_inside_higher_ed():
    try:
        session = get_session()
        url = "https://www.insidehighered.com/news"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []

        selectors = ['h3 a', 'h2 a', '.views-field-title a', '.article-title a']

        seen_titles = set()
        for selector in selectors:
            for tag in soup.select(selector):
                title = clean_title(tag.get_text())
                href = tag.get('href', '')

                if title and title not in seen_titles and href:
                    if href.startswith('/'):
                        href = "https://www.insidehighered.com" + href
                    elif not href.startswith('http'):
                        continue

                    articles.append({"title": title, "url": href, "source": "Inside Higher Ed"})
                    seen_titles.add(title)

        return articles
    except Exception as e:
        print(f"Error scraping Inside Higher Ed: {e}")
        return []

def scrape_edweek():
    try:
        session = get_session()
        url = "https://www.edweek.org/"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []

        selectors = ['h3 a', 'h2 a', '.article-title a', '.headline a']

        seen_titles = set()
        for selector in selectors:
            for tag in soup.select(selector):
                title = clean_title(tag.get_text())
                href = tag.get('href', '')

                if title and title not in seen_titles and href:
                    if href.startswith('/'):
                        href = "https://www.edweek.org" + href
                    elif not href.startswith('http'):
                        continue

                    articles.append({"title": title, "url": href, "source": "EdWeek"})
                    seen_titles.add(title)

        return articles
    except Exception as e:
        print(f"Error scraping EdWeek: {e}")
        return []

def scrape_chronicle():
    try:
        session = get_session()
        url = "https://www.chronicle.com/"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []

        selectors = ['h3 a', 'h2 a', '.hed a', '.title a']

        seen_titles = set()
        for selector in selectors:
            for tag in soup.select(selector):
                title = clean_title(tag.get_text())
                href = tag.get('href', '')

                if title and title not in seen_titles and href:
                    if href.startswith('/'):
                        href = "https://www.chronicle.com" + href
                    elif not href.startswith('http'):
                        continue

                    articles.append({"title": title, "url": href, "source": "The Chronicle"})
                    seen_titles.add(title)

        return articles
    except Exception as e:
        print(f"Error scraping Chronicle: {e}")
        return []


def scrape_india_today_education():
    try:
        session = get_session()
        url = "https://www.indiatoday.in/education-today/news"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []

        # Each article is inside a div with class 'B1S3_content__wrap__9mSB6'
        for item in soup.select('div.B1S3_content__wrap__9mSB6'):
            a_tag = item.find('a', href=True, title=True)
            if not a_tag:
                continue
            title = a_tag['title'].strip()
            href = a_tag['href']
            if href.startswith('/'):
                href = "https://www.indiatoday.in" + href

            articles.append({"title": title, "url": href, "source": "India Today" })

        return articles
    except Exception as e:
        print(f"Error scraping India Today: {e}")
        return []

def scrape_news(region, sources=None):
    articles = []
    errors = []

    # Define source maps like other category files
    india_source_map = {
        "flipboard": lambda: scrape_flipboard(region),
        "scoopit": lambda: scrape_scoopit(region),
        "hindustan_times": scrape_hindustan_times,
        "times_of_india": (lambda: scrape_times_of_india(sources)),
        "indian_express": scrape_indian_express_education,
        "the_hindu": scrape_the_hindu_education,
        "deccan_herald": scrape_deccan_herald_education,
        "ndtv": scrape_ndtv_education,
        "financial_express": scrape_financial_express_education,
        "india_today": scrape_india_today_education,
    }

    global_source_map = {
        "flipboard": lambda: scrape_flipboard(region),
        "scoopit": lambda: scrape_scoopit(region),
        "bbc": scrape_bbc_education,
        "guardian": scrape_guardian_education,
        "nytimes": scrape_nytimes_education,
        "washington_post": scrape_washington_post_education,
        "telegraph": scrape_telegraph_education,
        "times_higher_education": scrape_times_higher_education,
        "inside_higher_ed": scrape_inside_higher_ed,
        "edweek": scrape_edweek,
        "chronicle": scrape_chronicle,
    }

    if region == "India":
        source_map = india_source_map
    else:
        source_map = global_source_map

    if sources is None:
        sources = list(source_map.keys())

    print(f"Scraping selected sources: {sources} for region: {region}")

    for src in sources:
        func = source_map.get(src)
        if func:
            try:
                src_articles = func()
                print(f"General Education ({region} - {src}): {len(src_articles)} articles")
                articles.extend(src_articles)
                time.sleep(2)
            except Exception as e:
                error_msg = f"Error scraping {src}: {e}"
                print(error_msg)
                errors.append(error_msg)


    # Enhanced duplicate removal
    seen_urls = set()
    seen_titles = set()
    unique_articles = []

    for article in articles:
        # Normalize URL
        url = article['url'].split('?')[0].split('#')[0].lower()

        # Normalize title
        title = re.sub(r'[^a-zA-Z0-9]', '', article['title'].lower())[:60]

        if url not in seen_urls and title not in seen_titles:
            unique_articles.append(article)
            seen_urls.add(url)
            seen_titles.add(title)

    print(f"Total unique articles found: {len(unique_articles)}")
    return unique_articles, errors

# ---------- Entry Point ----------
if __name__ == "__main__":
    print("------ INDIA ARTICLES ------")
    india_articles, india_errors = scrape_news("India")
    for i, art in enumerate(india_articles, 1):
        print(f"{i}. {art['title']} ({art['source']})\n   {art['url']}")

    print("\n------ GLOBAL ARTICLES ------")
    global_articles, global_errors = scrape_news("Global")
    for i, art in enumerate(global_articles, 1):
        print(f"{i}. {art['title']} ({art['source']})\n   {art['url']}")
