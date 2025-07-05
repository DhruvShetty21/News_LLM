import requests
from bs4 import BeautifulSoup
from bs4.element import Tag as Bs4Tag  # ✅ Pyright-compatible Tag

from typing import List, Dict, Optional, Any
import time

higher_ed_keywords = [
    "university", "universities", "college", "higher education", "phd",
    "postgraduate", "campus", "admission", "rankings", "faculty", "research",
    "degree", "institute", "jee", "neet", "engineering", "iit", "mbbs",
    "aiims", "iim", "mba", "btech", "mtech", "bsc", "msc", "bcom", "mcom",
    "ba", "ma", "llb", "llm", "medical", "law", "management", "programming",
    "resume", "placement", "internship", "gate", "cat", "mat", "xat", "ugc",
    "net", "cuet", "nift", "nlu", "nlsiu", "scholarship", "fellowship"
]


def get_session():
    session = requests.Session()
    session.headers.update({
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/114.0.0.0 Safari/537.36"
    })
    return session


def clean_title(title: Optional[Any]) -> str:
    return str(title or "").strip().replace("\n", "").replace("\r", "")


def is_valid_keyword(text: Optional[str]) -> bool:
    return isinstance(text, str) and any(kw in text.lower() for kw in higher_ed_keywords)


def safe_href(href: Any) -> str:
    return str(href) if isinstance(href, str) else ""


def extract_href(tag: Any) -> str:
    if isinstance(tag, Bs4Tag):
        href = tag.get("href", "")
        return safe_href(href)
    return ""


def extract_text(tag: Any) -> str:
    if isinstance(tag, Bs4Tag):
        return tag.get_text(strip=True)
    return ""


def scrape_toi_links() -> List[Dict[str, str]]:
    try:
        session = get_session()
        response = session.get("https://timesofindia.indiatimes.com/topic/education", timeout=15)
        if response.status_code != 200:
            print("Failed to fetch TOI page. Status:", response.status_code)
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        articles = []

        for div in soup.find_all("div", class_="uwU81"):
            if not isinstance(div, Bs4Tag):
                continue

            a_tag = div.find("a")
            if not isinstance(a_tag, Bs4Tag) or not a_tag.get("href"):
                continue

            title_tag = div.find("div", class_="fHv_i")
            title = extract_text(title_tag)
            href = extract_href(a_tag)
            full_url = "https://timesofindia.indiatimes.com" + href

            classification = "Higher Education" if is_valid_keyword(title) else "Other"

            articles.append({
                "title": title,
                "url": full_url,
                "source": "TOI",
                "classification": classification
            })
        print(f"scrape_toi_links: {len(articles)} articles")
        return articles

    
    except Exception as e:
        print(f"Error scraping TOI: {e}")
        return []


def scrape_deccan_herald_higher_ed() -> List[Dict]:
    try:
        session = get_session()
        url = "https://www.deccanherald.com/tags/higher-education"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        seen = set()
        articles = []

        for tag in soup.select('a .headline, .article-title a, h2 a, h3 a'):
            a_tag = tag.find_parent('a') if isinstance(tag, Bs4Tag) and tag.name != 'a' else tag
            title = clean_title(extract_text(tag))
            href = extract_href(a_tag)
            if is_valid_keyword(title) and title not in seen:
                if href.startswith("/"):
                    href = "https://www.deccanherald.com" + href
                articles.append({
                    "title": title,
                    "url": href,
                    "source": "Deccan Herald"
                })
                seen.add(title)
        return articles
    except Exception as e:
        print(f"Error scraping DH: {e}")
        return []


def scrape_financial_express_higher_ed() -> List[Dict[str, str]]:
    try:
        session = get_session()
        url = "https://www.financialexpress.com/about/higher-education/"
        response = session.get(url, timeout=15)
        if response.status_code != 200:
            print("Failed to fetch Financial Express page. Status:", response.status_code)
            return []

        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        seen = set()

        for tag in soup.select('.entry-title a, .listitembx h3 a, h2 a, .title a'):
            if not isinstance(tag, Bs4Tag):
                continue

            title = clean_title(tag.get_text())
            href = tag.get("href", "")

            if not isinstance(href, str) or not href.startswith("http"):
                continue

            if is_valid_keyword(title) and title not in seen:
                articles.append({
                    "title": title,
                    "url": href,
                    "source": "Financial Express"
                })
                seen.add(title)

        return articles
    except Exception as e:
        print(f"Error scraping Financial Express: {e}")
        return []


def scrape_indian_express_higher_ed() -> List[Dict]:
    try:
        session = get_session()
        url = "https://indianexpress.com/about/higher-education/"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        seen = set()
        articles = []

        for tag in soup.select('h3 a, h2 a'):
            title = clean_title(extract_text(tag))
            href = extract_href(tag)
            if is_valid_keyword(title) and title not in seen:
                if href.startswith("/"):
                    href = "https://indianexpress.com" + href
                articles.append({
                    "title": title,
                    "url": href,
                    "source": "Indian Express"
                })
                seen.add(title)
        return articles
    except Exception as e:
        print(f"Error scraping IE: {e}")
        return []


def scrape_times_higher_education_global() -> List[Dict]:
    try:
        session = get_session()
        url = "https://www.timeshighereducation.com/academic/news"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        seen = set()
        articles = []

        for tag in soup.select('a[data-position="teaser-card"]'):
            h3 = tag.find('h3', class_='teaser-card__title') if isinstance(tag, Bs4Tag) else None
            title = clean_title(extract_text(h3))
            href = extract_href(tag)
            if title and href and title not in seen:
                if href.startswith("/"):
                    href = "https://www.timeshighereducation.com" + href
                articles.append({
                    "title": title,
                    "url": href,
                    "source": "Times Higher Education"
                })
                seen.add(title)
        return articles
    except Exception as e:
        print(f"Error scraping THE: {e}")
        return []


def scrape_inside_higher_ed_global() -> List[Dict]:
    try:
        session = get_session()
        seen = set()
        articles = []

        for page in range(1, 4):
            url = f"https://www.insidehighered.com/news?page={page}"
            response = session.get(url, timeout=15)
            soup = BeautifulSoup(response.content, "html.parser")

            for h4 in soup.find_all('h4'):
                a = h4.find('a') if isinstance(h4, Bs4Tag) else None
                span = a.find('span') if isinstance(a, Bs4Tag) else None
                title = clean_title(extract_text(span))
                href = extract_href(a)
                if title and href and title not in seen:
                    if href.startswith("/"):
                        href = "https://www.insidehighered.com" + href
                    articles.append({
                        "title": title,
                        "url": href,
                        "source": "Inside Higher Ed"
                    })
                    seen.add(title)
            time.sleep(1)
        return articles
    except Exception as e:
        print(f"Error scraping IHE: {e}")
        return []


def scrape_guardian_higher_ed_global() -> List[Dict]:
    try:
        session = get_session()
        url = "https://www.theguardian.com/education/higher-education"
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        seen = set()
        articles = []

        for tag in soup.select('a[aria-label]'):
            title = clean_title(tag.get("aria-label", ""))
            href = extract_href(tag)
            if title and href and '/202' in href and title not in seen:
                if not href.startswith("http"):
                    href = "https://www.theguardian.com" + href
                articles.append({
                    "title": title,
                    "url": href,
                    "source": "The Guardian"
                })
                seen.add(title)
        return articles
    except Exception as e:
        print(f"Error scraping Guardian: {e}")
        return []


def scrape_higher_ed_news(region="India", sources=None):
    all_articles = []

    india_sources = {
        "deccan_herald": scrape_deccan_herald_higher_ed,
        "financial_express": scrape_financial_express_higher_ed,
        "indian_express": scrape_indian_express_higher_ed,
        "toi": scrape_toi_links,
    }

    global_sources = {
        "times_higher_education": scrape_times_higher_education_global,
        "inside_higher_ed": scrape_inside_higher_ed_global,
        "guardian": scrape_guardian_higher_ed_global,
    }

    source_map = india_sources if region == "India" else global_sources
    sources = sources or list(source_map.keys())

    for key in sources:
        func = source_map.get(key)
        if func:
            try:
                items = func()
                print(f"{region} - {key}: {len(items)} articles")
                all_articles.extend(items)
            except Exception as e:
                print(f"Error in {key}: {e}")

    return all_articles


# ---------- Entry Point ----------
if __name__ == "__main__":
    print("------ INDIA ARTICLES ------")
    india = scrape_higher_ed_news("India")
    for i, art in enumerate(india, 1):
        print(f"{i}. {art['title']} ({art['source']})\n   {art['url']}")

    print("\n------ GLOBAL ARTICLES ------")
    global_ = scrape_higher_ed_news("Global")
    for i, art in enumerate(global_, 1):
        print(f"{i}. {art['title']} ({art['source']})\n   {art['url']}")
