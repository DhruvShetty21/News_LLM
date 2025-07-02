import requests
from bs4 import BeautifulSoup
from news_sources import get_session, clean_title
import time

# --- Indian Entertainment Sources (Placeholders) ---

def scrape_india_today_entertainment_india():
    try:
        session = get_session()
        url = "https://www.indiatoday.in/entertainment"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        seen_titles = set()

        # The articles are in 'a' tags with a 'title' attribute, inside an 'h3'
        for tag in soup.select('h3 a[title]'):
            title = clean_title(tag.get('title'))
            href = tag.get('href', '')

            if title and href and title not in seen_titles:
                if href.startswith('/'):
                    href = "https://www.indiatoday.in" + href
                
                articles.append({"title": title, "url": href, "source": "India Today"})
                seen_titles.add(title)
                
        return articles
    except Exception as e:
        print(f"Error scraping India Today Entertainment: {e}")
        return []

def scrape_financial_express_entertainment_india():
    try:
        session = get_session()
        url = "https://www.financialexpress.com/life/entertainment/"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        seen_titles = set()

        # Each article is within a div with class 'entry-wrapper'
        for item in soup.select('div.entry-wrapper'):
            title_tag = item.find('h2', class_='entry-title')
            summary_tag = item.find('div', class_='post-excerpt')
            
            if not title_tag or not title_tag.find('a'):
                continue
                
            href = title_tag.find('a')['href']
            
            # Use summary as title if available, otherwise use the main title
            if summary_tag and summary_tag.find('p'):
                title = clean_title(summary_tag.p.get_text())
            else:
                title = clean_title(title_tag.a.get_text())

            if title and href and title not in seen_titles:
                # URLs are absolute
                articles.append({"title": title, "url": href, "source": "Financial Express"})
                seen_titles.add(title)

        return articles
    except Exception as e:
        print(f"Error scraping Financial Express Entertainment: {e}")
        return []

def scrape_ndtv_entertainment_india():
    try:
        session = get_session()
        url = "https://www.ndtv.com/topic/entertainment-news"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        seen_titles = set()

        # The articles are in 'a' tags inside an 'h3' with a specific class
        for item in soup.select('h3.SrchLstPg_ttl-lnk'):
            a_tag = item.find('a', class_='SrchLstPg_ttl')
            if not a_tag:
                continue
                
            title = clean_title(a_tag.get_text())
            href = a_tag.get('href', '')

            if title and href and title not in seen_titles:
                # URLs are already absolute
                articles.append({"title": title, "url": href, "source": "NDTV"})
                seen_titles.add(title)

        return articles
    except Exception as e:
        print(f"Error scraping NDTV Entertainment: {e}")
        return []

def scrape_deccan_herald_entertainment_india():
    try:
        session = get_session()
        url = "https://www.deccanherald.com/entertainment"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        seen_titles = set()

        # The articles are in 'a' tags, with the title in an 'h2' tag
        for a_tag in soup.select('a[href*="/entertainment/"]'):
            h2_tag = a_tag.find('h2', class_='headline')
            if not h2_tag:
                continue

            title = clean_title(h2_tag.get_text())
            href = a_tag.get('href', '')

            if title and href and title not in seen_titles:
                if href.startswith('/'):
                    href = "https://www.deccanherald.com" + href
                
                articles.append({"title": title, "url": href, "source": "Deccan Herald"})
                seen_titles.add(title)

        return articles
    except Exception as e:
        print(f"Error scraping Deccan Herald Entertainment: {e}")
        return []

def scrape_hindustan_times_entertainment_india():
    try:
        session = get_session()
        url = "https://www.hindustantimes.com/entertainment"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        seen_titles = set()

        for link in soup.select('h3 a[href*="/entertainment/"], h2 a[href*="/entertainment/"]'):
            title = clean_title(link.get_text())
            href = link.get('href', '')

            if title and href and title not in seen_titles:
                if href.startswith('/'):
                    href = "https://www.hindustantimes.com" + href
                articles.append({"title": title, "url": href, "source": "Hindustan Times"})
                seen_titles.add(title)
        return articles
    except Exception as e:
        print(f"Error scraping Hindustan Times Entertainment: {e}")
        return []

def scrape_times_of_india_entertainment_india():
    try:
        session = get_session()
        url = "https://timesofindia.indiatimes.com/entertainment"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        seen_titles = set()

        for link in soup.select('a.border_color.VeCXM.SFmi8'):
            p_tag = link.find('p', class_='CRKrj style_change')
            if not p_tag:
                continue
            title = clean_title(p_tag.get_text())
            href = link.get('href', '')
            if title and href and title not in seen_titles:
                if not href.startswith('http'):
                    href = "https://timesofindia.indiatimes.com" + href
                articles.append({"title": title, "url": href, "source": "Times of India"})
                seen_titles.add(title)
        return articles
    except Exception as e:
        print(f"Error scraping Times of India Entertainment: {e}")
        return []

def scrape_indian_express_entertainment_india():
    try:
        session = get_session()
        url = "https://indianexpress.com/section/entertainment/"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        seen_titles = set()

        for link in soup.select('h2.myie-article-title a, h3.myie-article-title a'):
            title = clean_title(link.get('title', ''))
            href = link.get('href', '')

            if title and href and title not in seen_titles:
                articles.append({"title": title, "url": href, "source": "Indian Express"})
                seen_titles.add(title)
        return articles
    except Exception as e:
        print(f"Error scraping Indian Express Entertainment: {e}")
        return []

def scrape_the_hindu_entertainment_india():
    articles = []
    seen_titles = set()
    session = get_session()
    
    try:
        for page in range(1, 5):
            url = f"https://www.thehindu.com/entertainment/?page={page}"
            response = session.get(url, timeout=15)
            soup = BeautifulSoup(response.content, "html.parser")

            for link in soup.select('h3.title > a, h2.title > a'):
                title = clean_title(link.get_text())
                href = link.get('href', '')

                if title and href and title not in seen_titles:
                    articles.append({"title": title, "url": href, "source": "The Hindu"})
                    seen_titles.add(title)
        return articles
    except Exception as e:
        print(f"Error scraping The Hindu Entertainment: {e}")
        return []

# --- Global Entertainment Sources (Placeholders) ---

def scrape_bbc_entertainment_global():
    print("Scraping BBC Entertainment (Global)...")
    # To-do: Add scraping logic here
    return []

def scrape_guardian_film_global():
    print("Scraping The Guardian Film (Global)...")
    # To-do: Add scraping logic here
    return []

def scrape_washington_post_entertainment_global():
    try:
        session = get_session()
        url = "https://www.washingtonpost.com/entertainment/"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        seen_titles = set()

        for a_tag in soup.select('a.wpds-c-ibuqEe[href*="/arts-entertainment/"]'):
            p_tag = a_tag.find('p', class_='wpds-c-exSVqq')
            if not p_tag:
                continue
            title = clean_title(p_tag.get_text())
            href = a_tag.get('href', '')
            if title and href and title not in seen_titles:
                articles.append({"title": title, "url": href, "source": "Washington Post"})
                seen_titles.add(title)
        return articles
    except Exception as e:
        print(f"Error scraping Washington Post Entertainment: {e}")
        return []

def scrape_cnn_entertainment_global():
    try:
        session = get_session()
        url = "https://edition.cnn.com/entertainment"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        seen_titles = set()
        # Both structures use a.container__link--type-article
        for a_tag in soup.select('a.container__link--type-article'):
            span = a_tag.find('span', class_='container__headline-text')
            if not span:
                continue
            title = clean_title(span.get_text())
            href = a_tag.get('href', '')
            if title and href and title not in seen_titles:
                if href.startswith('/'):
                    href = 'https://edition.cnn.com' + href
                articles.append({"title": title, "url": href, "source": "CNN Entertainment"})
                seen_titles.add(title)
        return articles
    except Exception as e:
        print(f"Error scraping CNN Entertainment: {e}")
        return []

def scrape_entertainment_news(region="India", sources=None):
    """
    Scrapes entertainment news from various sources based on the selected region.
    """
    all_articles = []
    
    india_source_map = {
        "india_today_entertainment": scrape_india_today_entertainment_india,
        "financial_express_entertainment": scrape_financial_express_entertainment_india,
        "ndtv_entertainment": scrape_ndtv_entertainment_india,
        "deccan_herald_entertainment": scrape_deccan_herald_entertainment_india,
        "hindustan_times_entertainment": scrape_hindustan_times_entertainment_india,
        "times_of_india_entertainment": scrape_times_of_india_entertainment_india,
        "indian_express_entertainment": scrape_indian_express_entertainment_india,
        "the_hindu_entertainment": scrape_the_hindu_entertainment_india,
    }
    
    global_source_map = {
        "bbc_entertainment": scrape_bbc_entertainment_global,
        "guardian_film": scrape_guardian_film_global,
        "washington_post_entertainment": scrape_washington_post_entertainment_global,
        "cnn_entertainment": scrape_cnn_entertainment_global,
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
                print(f"Entertainment ({region} - {src}): {len(src_articles)} articles")
                all_articles.extend(src_articles)
                time.sleep(1) # Be polite
            except Exception as e:
                print(f"Error in scrape_entertainment_news for source {src}: {e}")

    return all_articles

if __name__ == "__main__":
    print("\n--- Testing Indian Entertainment Sources ---\n")
    india_source_map = {
        "india_today_entertainment": scrape_india_today_entertainment_india,
        "financial_express_entertainment": scrape_financial_express_entertainment_india,
        "ndtv_entertainment": scrape_ndtv_entertainment_india,
        "deccan_herald_entertainment": scrape_deccan_herald_entertainment_india,
        "hindustan_times_entertainment": scrape_hindustan_times_entertainment_india,
        "times_of_india_entertainment": scrape_times_of_india_entertainment_india,
        "indian_express_entertainment": scrape_indian_express_entertainment_india,
        "the_hindu_entertainment": scrape_the_hindu_entertainment_india,
    }
    for name, func in india_source_map.items():
        print(f"\nSource: {name}")
        articles = func()
        for art in articles:
            print(f"- {art['title']} ({art['url']})")
        print(f"Total: {len(articles)} articles\n")

    print("\n--- Testing Global Entertainment Sources ---\n")
    global_source_map = {
        "bbc_entertainment": scrape_bbc_entertainment_global,
        "guardian_film": scrape_guardian_film_global,
        "washington_post_entertainment": scrape_washington_post_entertainment_global,
        "cnn_entertainment": scrape_cnn_entertainment_global,
    }
    for name, func in global_source_map.items():
        print(f"\nSource: {name}")
        articles = func()
        for art in articles:
            print(f"- {art['title']} ({art['url']})")
        print(f"Total: {len(articles)} articles\n") 