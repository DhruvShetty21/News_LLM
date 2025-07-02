import requests
from bs4 import BeautifulSoup
from news_sources import get_session, clean_title
import time

higher_ed_keywords = [
    "university", "universities", "college", "higher education", "phd", "postgraduate",
    "campus", "admission", "rankings", "faculty", "research", "degree", "institute",
    "jee", "neet", "engineering", "iit", "mbbs", "aiims", "iim", "mba", "btech", "mtech",
    "bsc", "msc", "bcom", "mcom", "ba", "ma", "llb", "llm", "medical", "law", "management",
    "programming", "resume", "placement", "internship", "gate", "cat", "mat", "xat", "ugc",
    "net", "cuet", "nift", "nlu", "nlsiu", "scholarship", "fellowship"
]

def scrape_hindustan_times_higher_ed():
    try:
        session = get_session()
        url = "https://www.hindustantimes.com/topic/times-higher-education"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        selectors = ['.hdg3 a', 'h3 a', 'h2 a', '.media-heading a']
        seen_titles = set()
        for selector in selectors:
            for tag in soup.select(selector):
                title = clean_title(tag.get_text())
                href = tag.get('href', '')
                if not any(kw in title.lower() for kw in higher_ed_keywords):
                    continue
                if title and title not in seen_titles and href:
                    if href.startswith('/'):
                        href = "https://www.hindustantimes.com" + href
                    elif not href.startswith('http'):
                        continue
                    articles.append({"title": title, "url": href, "source": "Hindustan Times"})
                    seen_titles.add(title)
        return articles
    except Exception as e:
        print(f"Error scraping Hindustan Times Higher Ed: {e}")
        return []

def scrape_ndtv_higher_ed():
    try:
        session = get_session()
        url = "https://www.ndtv.com/topic/higher-education-india"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        selectors = ['.newsHdng a', '.SrchLstPg_ttl-lnk a', 'h2 a', 'h3 a']
        seen_titles = set()
        for selector in selectors:
            for tag in soup.select(selector):
                title = clean_title(tag.get_text())
                href = tag.get('href', '')
                if not any(kw in title.lower() for kw in higher_ed_keywords):
                    continue
                if title and title not in seen_titles and href:
                    if href.startswith('/'):
                        href = "https://www.ndtv.com" + href
                    elif not href.startswith('http'):
                        continue
                    articles.append({"title": title, "url": href, "source": "NDTV"})
                    seen_titles.add(title)
        return articles
    except Exception as e:
        print(f"Error scraping NDTV Higher Ed: {e}")
        return []

def scrape_deccan_herald_higher_ed():
    try:
        session = get_session()
        url = "https://www.deccanherald.com/tags/higher-education"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        selectors = ['a .headline', '.article-title a', 'h2 a', 'h3 a']
        seen_titles = set()
        for selector in selectors:
            for tag in soup.select(selector):
                a_tag = tag.find_parent('a') if tag.name != 'a' else tag
                if not a_tag:
                    continue
                title = clean_title(tag.get_text())
                href = a_tag.get('href', '')
                if not any(kw in title.lower() for kw in higher_ed_keywords):
                    continue
                if title and title not in seen_titles and href:
                    if href.startswith('/'):
                        href = "https://www.deccanherald.com" + href
                    elif not href.startswith('http'):
                        continue
                    articles.append({"title": title, "url": href, "source": "Deccan Herald"})
                    seen_titles.add(title)
        return articles
    except Exception as e:
        print(f"Error scraping Deccan Herald Higher Ed: {e}")
        return []

def scrape_financial_express_higher_ed():
    try:
        session = get_session()
        url = "https://www.financialexpress.com/about/higher-education/"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        selectors = ['.entry-title a', '.listitembx h3 a', 'h2 a', '.title a']
        seen_titles = set()
        skip_keywords = ['related-news', 'photos', 'latest-news']
        for selector in selectors:
            for tag in soup.select(selector):
                title = clean_title(tag.get_text())
                href = tag.get('href', '')
                if any(kw in href for kw in skip_keywords):
                    continue
                if not any(kw in title.lower() for kw in higher_ed_keywords):
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
        print(f"Error scraping Financial Express Higher Ed: {e}")
        return []

def scrape_indian_express_higher_ed():
    try:
        session = get_session()
        url = "https://indianexpress.com/about/higher-education/"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        selectors = ['h3 a', 'h2 a']
        seen_titles = set()
        for selector in selectors:
            for tag in soup.select(selector):
                title = clean_title(tag.get_text())
                href = tag.get('href', '')
                if not any(kw in title.lower() for kw in higher_ed_keywords):
                    continue
                if title and title not in seen_titles and href:
                    if href.startswith('/'):
                        href = "https://indianexpress.com" + href
                    elif not href.startswith('http'):
                        continue
                    articles.append({"title": title, "url": href, "source": "Indian Express"})
                    seen_titles.add(title)
        return articles
    except Exception as e:
        print(f"Error scraping Indian Express Higher Ed: {e}")
        return []

# --- Global Higher Education Sources ---

def scrape_times_higher_education_global():
    try:
        session = get_session()
        url = "https://www.timeshighereducation.com/academic/news"
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
        print(f"Error scraping Times Higher Education: {e}")
        return []

def scrape_inside_higher_ed_global():
    try:
        session = get_session()
        articles = []
        seen_titles = set()

        for page in range(1, 10):  # Scrape pages 1 to 9
            url = f"https://www.insidehighered.com/news?page={page}"
            print(f"Scraping Inside Higher Ed page: {url}")
            response = session.get(url, timeout=15)
            soup = BeautifulSoup(response.content, "html.parser")

            # The title is in a span inside an 'a' tag, which is inside an 'h4'
            for h4_tag in soup.find_all('h4'):
                a_tag = h4_tag.find('a', href=True)
                if not a_tag:
                    continue
                
                span_tag = a_tag.find('span')
                if not span_tag:
                    continue

                title = clean_title(span_tag.get_text())
                href = a_tag.get('href', '')

                if title and href and title not in seen_titles:
                    if href.startswith('/'):
                        href = "https://www.insidehighered.com" + href
                    
                    articles.append({"title": title, "url": href, "source": "Inside Higher Ed"})
                    seen_titles.add(title)
            
            time.sleep(1) # Be polite to the server

        return articles
    except Exception as e:
        print(f"Error scraping Inside Higher Ed: {e}")
        return []

def scrape_guardian_higher_ed_global():
    try:
        session = get_session()
        url = "https://www.theguardian.com/education/higher-education"  # Corrected URL
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
        print(f"Error scraping Guardian Higher Ed: {e}")
        return []

def scrape_chronicle_global():
    try:
        session = get_session()
        url = "https://www.chronicle.com/"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        seen_titles = set()

        # The articles are in 'a' tags with class="Link"
        for tag in soup.select('a.Link'):
            title = clean_title(tag.get_text())
            href = tag.get('href', '')

            # Basic validation to ensure it's an article URL
            if title and href and 'article' in href and title not in seen_titles:
                # The hrefs are already absolute
                articles.append({"title": title, "url": href, "source": "The Chronicle"})
                seen_titles.add(title)

        return articles
    except Exception as e:
        print(f"Error scraping Chronicle Higher Ed: {e}")
        return []

def scrape_higher_ed_news(region="India", sources=None):
    all_articles = []
    
    india_source_map = {
        "hindustan_times": scrape_hindustan_times_higher_ed,
        "ndtv": scrape_ndtv_higher_ed,
        "deccan_herald": scrape_deccan_herald_higher_ed,
        "financial_express": scrape_financial_express_higher_ed,
        "indian_express": scrape_indian_express_higher_ed,
       
    }
    
    global_source_map = {
        "times_higher_education": scrape_times_higher_education_global,
        "inside_higher_ed": scrape_inside_higher_ed_global,
        "guardian": scrape_guardian_higher_ed_global,
        "chronicle": scrape_chronicle_global,
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
                print(f"Higher Ed ({region} - {src}): {len(src_articles)} articles")
                all_articles.extend(src_articles)
            except Exception as e:
                print(f"Error in scrape_higher_ed_news for source {src}: {e}")

    # To-do: Add enhanced duplicate removal here if needed
    return all_articles

if __name__ == "__main__":
    print("--- Scraping India Higher Ed ---")
    india_articles = scrape_higher_ed_news(region="India")
    for i, art in enumerate(india_articles, 1):
        print(f"{i}. {art['title']} ({art['source']})\n   {art['url']}\n")

    print("\n--- Scraping Global Higher Ed ---")
    global_articles = scrape_higher_ed_news(region="Global")
    for i, art in enumerate(global_articles, 1):
        print(f"{i}. {art['title']} ({art['source']})\n   {art['url']}\n")