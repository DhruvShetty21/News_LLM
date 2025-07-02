import requests
from bs4 import BeautifulSoup
import time

# Define keywords related to sports (used for filtering if needed)
sports_keywords = [
    "cricket", "football", "soccer", "tennis", "badminton", "hockey",
    "olympics", "fifa", "ipl", "nba", "kabaddi", "athletics",
    "match", "tournament", "goal", "score", "series", "medal",
    "championship", "sports", "final", "semifinal", "quarterfinal",
    "test", "odi", "t20"
]

# Add this mapping at the top of your file
SPORTS_SOURCE_MAP = {
    "indian_express_sports": "Indian Express",
    "espncricinfo": "ESPN Cricinfo",
    "ndtv_sports": "NDTV Sports",
    "the_hindu": "The Hindu",
    "bbc_sport": "BBC Sport",
    "guardian_sports": "The Guardian",
    "espn_global": "ESPN"
}

# Helper functions to clean titles and initialize sessions
def clean_title(title):
    return title.strip().replace("\n", " ").replace("  ", " ")

def get_session():
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/90.0.4430.85 Safari/537.36"
    })
    return session

# India Sports News

def scrape_espncricinfo():
    try:
        session = get_session()
        articles = []
        seen_titles = set()

        for page_num in range(1, 5):  # Loop through pages 1 to 4
            if page_num == 1:
                url = "https://www.espncricinfo.com/genre/news-1"
            else:
                url = f"https://www.espncricinfo.com/genre/news-1?page={page_num}"

            response = session.get(url, timeout=15)
            soup = BeautifulSoup(response.content, "html.parser")
            headlines = soup.select("h2.ds-text-title-s")

            for headline in headlines:
                title = clean_title(headline.text)
                link_tag = headline.find_parent("a")
                
                if title and link_tag:
                    href = link_tag.get("href", "")
                    if not href.startswith("http"):
                        href = "https://www.espncricinfo.com" + href

                    if href and title not in seen_titles:
                        articles.append({"title": title, "url": href, "source": "ESPN Cricinfo"})
                        seen_titles.add(title)
            
            time.sleep(1)  # Be polite to the server

        return articles
    except Exception as e:
        return []

def scrape_indian_express_sports():
    try:
        session = get_session()
        articles = []
        seen_titles = set()
        for page_num in range(1, 3):  # Pages 1 to 4
            if page_num == 1:
                url = "https://indianexpress.com/section/sports/"
            else:
                url = f"https://indianexpress.com/section/sports/page/{page_num}/"
            response = session.get(url, timeout=15)
            soup = BeautifulSoup(response.content, "html.parser")
            for tag in soup.select(".articles a"):
                title = clean_title(tag.text)
                href = tag.get("href", "")
                if not href.startswith("http"):
                    href = "https://indianexpress.com" + href
                if title and title not in seen_titles:
                    articles.append({"title": title, "url": href, "source": "Indian Express"})
                    seen_titles.add(title)
            time.sleep(1)
        return articles
    except Exception as e:
        return []

def scrape_ndtv_sports():
    try:
        session = get_session()
        url = "https://sports.ndtv.com/"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        seen_titles = set()

        # Combined selectors for the different story structures provided
        stories = soup.select('h3.crd_txt-wrp, a.img-gr, h1.crd_ttl5, h3.crd_ttl')
        for story in stories:
            title = ""
            href = ""
            link_tag = None

            # Handle image-based links (structure 2)
            if story.name == 'a' and 'img-gr' in story.get('class', []):
                link_tag = story
                img = story.find('img')
                if img and img.has_attr('alt'):
                    title = clean_title(img['alt'])
            else: # Handle text-based links (structures 1, 3, 4)
                link_tag = story.find('a')

            if link_tag:
                if not title:  # If title wasn't found in an image alt text
                    title = clean_title(link_tag.get_text())
                href = link_tag.get('href', '')

            if title and href and title not in seen_titles:
                articles.append({"title": title, "url": href, "source": "NDTV Sports"})
                seen_titles.add(title)
                
        return articles
    except Exception as e:
        return []

def scrape_the_hindu_sports():
    try:
        session = get_session()
        articles = []
        seen_titles = set()
        for page_num in range(1, 7):  # Pages 1 to 6
            url = f"https://www.thehindu.com/sport/other-sports/?page={page_num}"
            response = session.get(url, timeout=15)
            soup = BeautifulSoup(response.content, "html.parser")
            for h3 in soup.find_all("h3", class_=["title", "title big"]):
                a_tag = h3.find("a", href=True)
                if a_tag:
                    title = clean_title(a_tag.get_text())
                    href = a_tag["href"]
                    if not href.startswith("http"):
                        href = "https://www.thehindu.com" + href
                    if title and href and title not in seen_titles:
                        articles.append({"title": title, "url": href, "source": "The Hindu"})
                        seen_titles.add(title)
            time.sleep(1)
        return articles
    except Exception as e:
        return []

# Global Sports News

def scrape_espn():
    try:
        session = get_session()
        url = "https://www.espn.com/"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        seen_titles = set()

        for tag in soup.select("section.headlineStack li a"):
            title = clean_title(tag.text)
            href = tag.get("href", "")
            if not href.startswith("http"):
                href = "https://www.espn.com" + href

            if title and title not in seen_titles:
                articles.append({"title": title, "url": href, "source": "ESPN"})
                seen_titles.add(title)

        return articles
    except Exception as e:
        return []

def scrape_guardian_sports():
    try:
        session = get_session()
        url = "https://www.theguardian.com/sport"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        seen_titles = set()

        for tag in soup.select("a[aria-label]"):
            title = clean_title(tag.get("aria-label"))
            href = tag.get("href", "")

            if title and href and "/202" in href and title not in seen_titles:
                articles.append({"title": title, "url": href, "source": "The Guardian"})
                seen_titles.add(title)

        return articles
    except Exception as e:
        return []

def scrape_bbc_sport():
    try:
        session = get_session()
        url = "https://www.bbc.com/sport"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        seen_titles = set()

        for h3 in soup.find_all("h3"):
            a_tag = h3.find("a", href=True)
            if a_tag:
                # Headline is inside <span aria-hidden="false"> if present
                headline_tag = a_tag.find("span", attrs={"aria-hidden": "false"})
                if headline_tag:
                    title = clean_title(headline_tag.get_text())
                else:
                    title = clean_title(a_tag.get_text())
                href = a_tag["href"]
                if href.startswith("/"):
                    href = "https://www.bbc.com" + href
                if title and href and title not in seen_titles:
                    articles.append({"title": title, "url": href, "source": "BBC Sport"})
                    seen_titles.add(title)
        return articles
    except Exception as e:
        return []

# Controller function
def scrape_sports_news(region="India", sources=None):
    all_articles = []

    india_source_map = {
        "espncricinfo": scrape_espncricinfo,
        "indian_express_sports": scrape_indian_express_sports,
        "ndtv_sports": scrape_ndtv_sports,
        "the_hindu": scrape_the_hindu_sports,
    }
    global_source_map = {
        "espn_global": scrape_espn,
        "guardian_sports": scrape_guardian_sports,
        "bbc_sport": scrape_bbc_sport,
    }
    source_map = india_source_map if region == "India" else global_source_map

    if sources is None:
        sources = list(source_map.keys())

    for src in sources:
        func = source_map.get(src)
        if func:
            try:
                result = func()
                all_articles.extend(result)
            except Exception as e:
                pass
    return all_articles

if __name__ == "__main__":
    print("--- Scraping India Sports News ---")
    india_news = scrape_sports_news("India")
    for i, art in enumerate(india_news, 1):
        print(f"{i}. {art['title']} ({art['source']})\n   {art['url']}\n")

    print("\n--- Scraping Global Sports News ---")
    global_news = scrape_sports_news("Global")
    for i, art in enumerate(global_news, 1):
        print(f"{i}. {art['title']} ({art['source']})\n   {art['url']}\n") 