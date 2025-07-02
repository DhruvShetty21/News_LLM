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

def scrape_times_of_india():
    try:
        session = get_session()
        url = "https://timesofindia.indiatimes.com/topic/education"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []

        selectors = ['span.w_tle a', '.story-list a', '.list5 a']

        seen_titles = set()
        for selector in selectors:
            for tag in soup.select(selector):
                title = clean_title(tag.get_text())
                href = tag.get('href', '')

                if title and title not in seen_titles and href:
                    if href.startswith('/'):
                        href = "https://timesofindia.indiatimes.com" + href
                    elif not href.startswith('http'):
                        continue

                    articles.append({"title": title, "url": href, "source": "Times of India"})
                    seen_titles.add(title)

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

def scrape_financial_express_education():
    try:
        session = get_session()
        url = "https://www.financialexpress.com/education/"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []

        selectors = ['.listitembx h3 a', 'h2 a', '.title a']

        seen_titles = set()
        for selector in selectors:
            for tag in soup.select(selector):
                title = clean_title(tag.get_text())
                href = tag.get('href', '')

                if title and title not in seen_titles and href:
                    if href.startswith('/'):
                        href = "https://www.financialexpress.com" + href
                    elif not href.startswith('http'):
                        continue

                    articles.append({"title": title, "url": href, "source": "Financial Express"})
                    seen_titles.add(title)

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
    if not sources:
        print(f"Scraping news for region: {region}")

        # Primary sources (scrape more from these)
        flipboard = scrape_flipboard(region)
        print(f"Flipboard articles: {len(flipboard)}")
        articles.extend(flipboard)
        time.sleep(2)

        scoopit = scrape_scoopit(region)
        print(f"Scoop.it articles: {len(scoopit)}")
        articles.extend(scoopit)
        time.sleep(2)

        # Secondary sources (scrape fewer from these)
        if region == "India":
            default_sources = [
                scrape_hindustan_times,
                scrape_times_of_india,
                scrape_indian_express_education,
                scrape_the_hindu_education,
                scrape_deccan_herald_education,
                scrape_ndtv_education,
                scrape_financial_express_education,
                scrape_india_today_education  # <-- Added India Today here
            ]
        else:
            default_sources = [
                scrape_bbc_education,
                scrape_guardian_education,
                scrape_nytimes_education,
                scrape_washington_post_education,
                scrape_telegraph_education,
                scrape_times_higher_education,
                scrape_inside_higher_ed,
                scrape_edweek,
                scrape_chronicle
            ]

        for source in default_sources:
            try:
                source_articles = source()
                articles.extend(source_articles)
                time.sleep(2)
            except Exception as e:
                error_msg = f"Error scraping {source.__name__}: {e}"
                print(error_msg)
                errors.append(error_msg)
    else:
        source_map = {
            # "google_news": scrape_google_news,  # REMOVED
            "flipboard": lambda: scrape_flipboard(region),
            "scoopit": lambda: scrape_scoopit(region),
            "hindustan_times": scrape_hindustan_times,
            "times_of_india": scrape_times_of_india,
            "indian_express": scrape_indian_express_education,
            "the_hindu": scrape_the_hindu_education,
            "deccan_herald": scrape_deccan_herald_education,
            "ndtv": scrape_ndtv_education,
            "financial_express": scrape_financial_express_education,
            "india_today": scrape_india_today_education,  # <-- Added India Today here
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
        for src in sources:
            func = source_map.get(src)
            if func:
                try:
                    articles.extend(func())
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