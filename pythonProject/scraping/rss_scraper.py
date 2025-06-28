import feedparser
import requests
import re
from typing import List, Dict
from urllib.parse import urljoin, urlparse
import html

GOOGLE_NEWS_API_KEY = "41c2a568555d44e1aae14071fe43a3d7"

def clean_title(title: str) -> str:
    if not title:
        return None
    title = re.sub(r'\s+', ' ', title.strip())
    if len(title) < 10 or len(title) > 200:
        return None
    skip_words = ['subscribe', 'login', 'register', 'advertisement', 'menu', 'search', 'newsletter']
    if any(word in title.lower() for word in skip_words):
        return None
    return title

def is_valid_image_url(url: str) -> bool:
    """Check if URL is a valid image URL"""
    if not url:
        return False
    
    # Remove query parameters for extension check
    clean_url = url.split('?')[0].lower()
    
    # Check for common image extensions
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg']
    has_extension = any(clean_url.endswith(ext) for ext in image_extensions)
    
    # Check for common image hosting patterns
    image_patterns = [
        'images', 'img', 'photo', 'pics', 'media', 'upload', 'cdn', 'static',
        'thumb', 'resize', 'crop', 'avatar', 'logo', 'banner'
    ]
    has_pattern = any(pattern in url.lower() for pattern in image_patterns)
    
    # Must have either extension or pattern, and be a valid URL
    try:
        parsed = urlparse(url)
        return (has_extension or has_pattern) and bool(parsed.netloc)
    except:
        return False

def extract_image_from_entry(entry, base_url: str = None) -> str:
    """Enhanced image extraction with multiple fallback methods"""
    image_url = None
    
    try:
        # Method 1: media_thumbnail (most reliable)
        if hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
            for thumb in entry.media_thumbnail:
                url = thumb.get('url') or thumb.get('href')
                if is_valid_image_url(url):
                    image_url = url
                    break
        
        # Method 2: media_content
        if not image_url and hasattr(entry, 'media_content') and entry.media_content:
            for media in entry.media_content:
                url = media.get('url') or media.get('href')
                media_type = media.get('type', '').lower()
                if 'image' in media_type and is_valid_image_url(url):
                    image_url = url
                    break
        
        # Method 3: enclosures
        if not image_url and hasattr(entry, 'enclosures') and entry.enclosures:
            for enc in entry.enclosures:
                url = enc.get('href') or enc.get('url')
                enc_type = enc.get('type', '').lower()
                if 'image' in enc_type and is_valid_image_url(url):
                    image_url = url
                    break
        
        # Method 4: Extract from summary/content HTML
        if not image_url:
            content_fields = [
                entry.get('summary', ''),
                entry.get('content', ''),
                entry.get('description', '')
            ]
            
            for content in content_fields:
                if not content:
                    continue
                
                # Decode HTML entities
                content = html.unescape(str(content))
                
                # Multiple regex patterns for image extraction
                img_patterns = [
                    r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>',
                    r'<img[^>]+src=([^\s>]+)',
                    r'src=["\']([^"\']*\.(?:jpg|jpeg|png|gif|webp|bmp)(?:\?[^"\']*)?)["\']',
                    r'background-image:\s*url\(["\']?([^"\')\s]+)["\']?\)',
                    r'data-src=["\']([^"\']+)["\']',
                    r'data-lazy-src=["\']([^"\']+)["\']'
                ]
                
                for pattern in img_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    for match in matches:
                        url = match.strip()
                        if is_valid_image_url(url):
                            # Convert relative URLs to absolute
                            if base_url and url.startswith('/'):
                                url = urljoin(base_url, url)
                            image_url = url
                            break
                    if image_url:
                        break
                if image_url:
                    break
        
        # Method 5: Check for Open Graph or Twitter Card images in links
        if not image_url and hasattr(entry, 'links') and entry.links:
            for link in entry.links:
                if link.get('rel') == 'enclosure' and 'image' in link.get('type', ''):
                    url = link.get('href')
                    if is_valid_image_url(url):
                        image_url = url
                        break
        
        # Method 6: Look for image in tags
        if not image_url and hasattr(entry, 'tags') and entry.tags:
            for tag in entry.tags:
                if 'image' in tag.get('term', '').lower():
                    # Sometimes images are stored in tag attributes
                    for attr in ['href', 'url', 'src']:
                        url = tag.get(attr)
                        if is_valid_image_url(url):
                            image_url = url
                            break
                if image_url:
                    break
        
        # Clean and validate final URL
        if image_url:
            # Remove any surrounding quotes or whitespace
            image_url = image_url.strip('\'"')
            
            # Convert relative URLs to absolute if base_url is provided
            if base_url and not image_url.startswith(('http://', 'https://')):
                image_url = urljoin(base_url, image_url)
            
            # Final validation
            if not is_valid_image_url(image_url):
                image_url = None
    
    except Exception as e:
        print(f"⚠️ Error extracting image: {e}")
        image_url = None
    
    return image_url

def get_topic_feeds(topic: str, region: str) -> List[str]:
    topic = topic.lower()
    region = region.lower()

    feeds = {
        "education": {
            "india": [
                "https://indianexpress.com/section/education/feed/",
                "https://www.hindustantimes.com/feeds/rss/education/rssfeed.xml",
                "https://www.jagranjosh.com/rss-feeds/rssfeed-education.xml"
            ],
            "global": [
                "https://www.edutopia.org/rss.xml",
                "https://feeds.bbci.co.uk/news/education/rss.xml",
                "https://www.insidehighered.com/rss/news"
            ]
        },
        "technology": {
            "india": [
                "https://www.gadgets360.com/rss/news",
                "https://tech.hindustantimes.com/rss/tech/news",
                "https://indianexpress.com/section/technology/feed/"
            ],
            "global": [
                "https://www.theverge.com/rss/index.xml",
                "https://techcrunch.com/feed/",
                "https://www.zdnet.com/news/rss.xml"
            ]
        },
        "science": {
            "india": [
                "https://www.thehindu.com/sci-tech/science/feeder/default.rss",
                "https://currentaffairs.adda247.com/feed/",
                "https://www.downtoearth.org.in/rss/science"
            ],
            "global": [
                "https://www.sciencedaily.com/rss/top/science.xml",
                "https://rss.sciam.com/ScientificAmerican-News",
                "https://www.nature.com/subjects/science.rss"
            ]
        },
        "health": {
            "india": [
                "https://www.healthcareradius.in/rss",
                "https://health.economictimes.indiatimes.com/rss/topstories.cms",
                "https://www.expresshealthcare.in/feed/"
            ],
            "global": [
                "https://www.medicalnewstoday.com/rss",
                "https://www.who.int/feeds/entity/mediacentre/news/en/rss.xml",
                "https://www.healthline.com/rss"
            ]
        },
        "business": {
            "india": [
                "https://www.moneycontrol.com/rss/latestnews.xml",
                "https://economictimes.indiatimes.com/rssfeedstopstories.cms",
                "https://www.business-standard.com/rss/home_page_top_stories.rss"
            ],
            "global": [
                "https://www.bloomberg.com/feed/podcast/etf-report.xml",
                "https://www.reuters.com/rssFeed/businessNews",
                "https://feeds.bbci.co.uk/news/business/rss.xml"
            ]
        },
        "finance": {
            "india": [
                "https://www.livemint.com/rss/money",
                "https://www.financialexpress.com/feed/",
                "https://www.thehindubusinessline.com/feeder/default.rss"
            ],
            "global": [
                "https://www.investing.com/rss/news_25.rss",
                "https://www.marketwatch.com/rss/topstories",
                "https://www.cnbc.com/id/100003114/device/rss/rss.html"
            ]
        },
        "environment": {
            "india": [
                "https://www.downtoearth.org.in/rss/environment",
                "https://www.thehindu.com/sci-tech/energy-and-environment/feeder/default.rss",
                "https://www.indiaenvironmentportal.org.in/rss"
            ],
            "global": [
                "https://news.un.org/feed/subscribe/en/news/topic/climate-change/feed/rss.xml",
                "https://www.nature.com/subjects/environmental-sciences.rss",
                "https://www.theguardian.com/environment/rss"
            ]
        }
    }

    general_feeds = [
        "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
        "https://www.thehindu.com/news/national/feeder/default.rss",
        "https://feeds.bbci.co.uk/news/world/rss.xml"
    ]

    topic_feeds = feeds.get(topic, {})
    region_feeds = topic_feeds.get(region, [])
    return region_feeds + general_feeds

def fetch_rss_articles(topic: str, region: str) -> List[Dict]:
    rss_urls = get_topic_feeds(topic, region)
    articles = []
    successful_feeds = 0
    total_images_found = 0

    for url in rss_urls:
        try:
            print(f"📡 Parsing RSS feed: {url}")
            feed = feedparser.parse(url)
            
            if not feed.entries:
                print(f"⚠️ No entries found in {url}")
                continue
                
            successful_feeds += 1
            base_url = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
            
            for entry in feed.entries:
                title = clean_title(entry.get("title", ""))
                if not title:
                    continue

                # Enhanced image extraction
                image_url = extract_image_from_entry(entry, base_url)
                if image_url:
                    total_images_found += 1

                # Clean summary by removing HTML tags
                summary = entry.get("summary", "")
                clean_summary = re.sub(r"<[^<]+?>", "", html.unescape(summary))

                articles.append({
                    "title": title,
                    "link": entry.get("link", ""),
                    "summary": clean_summary,
                    "content": summary,
                    "image": image_url,
                    "source": f"RSS Feed - {urlparse(url).netloc}"
                })

            print(f"✅ Successfully parsed {len(feed.entries)} entries from {urlparse(url).netloc}")

        except Exception as e:
            print(f"❌ Error parsing RSS from {url}: {e}")
            continue

    print(f"📊 RSS Summary: {successful_feeds}/{len(rss_urls)} feeds successful, {total_images_found} images found")
    return articles

def fetch_google_news_articles(topic: str, region: str) -> List[Dict]:
    print("🌐 Fetching from Google News API...")
    try:
        url = f"https://newsapi.org/v2/everything?q={topic}&language=en&pageSize=50&apiKey={GOOGLE_NEWS_API_KEY}"
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            print(f"❌ Google News API error {response.status_code}: {response.text}")
            return []

        data = response.json()
        articles = []
        images_found = 0
        
        for item in data.get("articles", []):
            title = clean_title(item.get("title", ""))
            if not title:
                continue
            
            # Get image from Google News API
            image_url = item.get("urlToImage", "")
            if image_url and is_valid_image_url(image_url):
                images_found += 1
            else:
                image_url = None
            
            articles.append({
                "title": title,
                "link": item.get("url", ""),
                "summary": item.get("description", ""),
                "content": item.get("content", ""),
                "image": image_url,
                "source": f"Google News - {item.get('source', {}).get('name', 'Unknown')}"
            })
        
        print(f"✅ Google News: {len(articles)} articles, {images_found} with images")
        return articles

    except Exception as e:
        print(f"❌ Exception during Google News fetch: {e}")
        return []

def fetch_articles(topic: str, region: str) -> List[Dict]:
    print(f"\n🚀 Starting article fetching for: {topic} [{region.title()}]")

    rss_articles = fetch_rss_articles(topic, region)
    rss_articles = rss_articles[:200]  # ✅ LIMIT to 200 RSS articles
    print(f"📡 RSS articles: {len(rss_articles)}")

    google_news_articles = fetch_google_news_articles(topic, region)
    print(f"🌐 Google News articles: {len(google_news_articles)}")

    all_articles = rss_articles + google_news_articles

    # Remove duplicates
    seen = set()
    unique_articles = []
    total_with_images = 0
    
    for article in all_articles:
        key = article.get("title", "") + article.get("link", "")
        if key not in seen:
            seen.add(key)
            unique_articles.append(article)
            if article.get("image"):
                total_with_images += 1

    print(f"✅ Final unique articles: {len(unique_articles)}")
    print(f"🖼️ Articles with images: {total_with_images}/{len(unique_articles)} ({total_with_images/len(unique_articles)*100:.1f}%)")
    
    return unique_articles

# Debug run
if __name__ == "__main__":
    articles = fetch_articles("education", "india")
    print(f"\n📊 Sample articles with images:")
    count = 0
    for i, article in enumerate(articles, 1):
        if article.get('image'):
            count += 1
            print(f"{count}. {article['title']}")
            print(f"   🖼️ Image: {article['image']}")
            print(f"   📰 Source: {article['source']}")
            print()
            if count >= 5:  # Show first 5 with images
                break