#!/usr/bin/env python3
"""
Educational News Filter System
A comprehensive system to filter educational news articles from various sources
using open-source LLMs with geographical and content-based filtering.
"""

import asyncio
import aiohttp
import json
import logging
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import re
from urllib.parse import urljoin, urlparse
import hashlib

# External dependencies (install via pip)
try:
    import feedparser
    from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
    import torch
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    from newspaper import Article
    import spacy
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Install with: pip install feedparser transformers torch scikit-learn newspaper3k spacy")
    print("Also run: python -m spacy download en_core_web_sm")
    exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContentCategory(Enum):
    EDUCATIONAL = "educational"
    GENERAL = "general"
    SENSITIVE = "sensitive"
    UNKNOWN = "unknown"

class GeographicalRegion(Enum):
    NORTH_AMERICA = "north_america"
    EUROPE = "europe"
    ASIA = "asia"
    AFRICA = "africa"
    SOUTH_AMERICA = "south_america"
    OCEANIA = "oceania"
    GLOBAL = "global"

@dataclass
class NewsArticle:
    title: str
    content: str
    url: str
    source: str
    published_date: datetime
    region: GeographicalRegion
    category: ContentCategory
    confidence_score: float
    summary: str
    keywords: List[str]
    article_hash: str

class NewsSourceManager:
    """Manages various news sources and their RSS feeds"""
    
    def __init__(self):
        self.sources = {
            GeographicalRegion.GLOBAL: [
                "https://feeds.bbci.co.uk/news/education/rss.xml",
                "https://www.edweek.org/api/rss.xml",
                "https://hechingerreport.org/feed/",
                "https://www.universityworldnews.com/rss.php",
            ],
            GeographicalRegion.NORTH_AMERICA: [
                "https://www.edweek.org/api/rss.xml",
                "https://hechingerreport.org/feed/",
                "https://www.insidehighered.com/rss.xml",
            ],
            GeographicalRegion.EUROPE: [
                "https://www.universityworldnews.com/rss.php?region=europe",
                "https://www.timeshighereducation.com/rss.xml",
            ],
            GeographicalRegion.ASIA: [
                "https://www.universityworldnews.com/rss.php?region=asia",
                "https://www.scmp.com/rss/318/feed",
            ],
            # Add more regions as needed
        }
    
    def get_sources_for_region(self, region: GeographicalRegion) -> List[str]:
        """Get RSS feeds for a specific region"""
        sources = self.sources.get(region, [])
        sources.extend(self.sources.get(GeographicalRegion.GLOBAL, []))
        return sources

class EducationalContentClassifier:
    """Open-source LLM-based classifier for educational content"""
    
    def __init__(self):
        # Using Hugging Face transformers with open-source models
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Load pre-trained models for classification
        self.educational_classifier = pipeline(
            "text-classification",
            model="microsoft/DialoGPT-medium",  # Can be replaced with other open-source models
            device=0 if torch.cuda.is_available() else -1
        )
        
        # Load model for content analysis
        self.content_analyzer = pipeline(
            "text-classification",
            model="unitary/toxic-bert",  # For sensitive content detection
            device=0 if torch.cuda.is_available() else -1
        )
        
        # Load NLP model for keyword extraction
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            logger.error("Spacy model not found. Run: python -m spacy download en_core_web_sm")
            raise
        
        # Educational keywords and patterns
        self.educational_keywords = {
            'education', 'school', 'university', 'college', 'student', 'teacher',
            'learning', 'curriculum', 'academic', 'research', 'study', 'classroom',
            'pedagogy', 'instruction', 'educational', 'scholar', 'campus',
            'enrollment', 'graduation', 'degree', 'course', 'syllabus', 'exam',
            'educational technology', 'e-learning', 'online learning', 'STEM',
            'literacy', 'educational policy', 'educational reform'
        }
        
        self.sensitive_keywords = {
            'violence', 'crime', 'murder', 'assault', 'terrorism', 'war',
            'explicit', 'adult content', 'graphic', 'disturbing', 'tragedy',
            'disaster', 'death', 'injury', 'accident', 'controversial'
        }

    def classify_content(self, title: str, content: str) -> Tuple[ContentCategory, float]:
        """Classify content as educational, general, or sensitive"""
        combined_text = f"{title} {content[:500]}"  # Limit for model input
        
        # Check for educational content
        educational_score = self._calculate_educational_score(combined_text)
        
        # Check for sensitive content
        sensitive_score = self._calculate_sensitive_score(combined_text)
        
        # Determine category based on scores
        if sensitive_score > 0.7:
            return ContentCategory.SENSITIVE, sensitive_score
        elif educational_score > 0.6:
            return ContentCategory.EDUCATIONAL, educational_score
        elif educational_score > 0.3:
            return ContentCategory.GENERAL, educational_score
        else:
            return ContentCategory.UNKNOWN, max(educational_score, sensitive_score)

    def _calculate_educational_score(self, text: str) -> float:
        """Calculate educational relevance score"""
        text_lower = text.lower()
        
        # Keyword-based scoring
        keyword_score = sum(1 for keyword in self.educational_keywords 
                          if keyword in text_lower) / len(self.educational_keywords)
        
        # NLP-based feature extraction
        doc = self.nlp(text[:1000])  # Limit for processing
        
        # Check for educational entities and patterns
        educational_entities = ['ORG', 'PERSON', 'GPE']  # Organizations, people, places
        entity_score = sum(1 for ent in doc.ents 
                         if ent.label_ in educational_entities) / max(len(doc.ents), 1)
        
        # Combine scores
        final_score = (keyword_score * 0.6) + (entity_score * 0.4)
        return min(final_score, 1.0)

    def _calculate_sensitive_score(self, text: str) -> float:
        """Calculate sensitive content score"""
        text_lower = text.lower()
        
        # Keyword-based scoring
        sensitive_count = sum(1 for keyword in self.sensitive_keywords 
                            if keyword in text_lower)
        
        # Use toxic-bert for additional analysis
        try:
            result = self.content_analyzer(text[:512])  # Model input limit
            toxicity_score = result[0]['score'] if result[0]['label'] == 'TOXIC' else 0
        except Exception as e:
            logger.warning(f"Toxicity analysis failed: {e}")
            toxicity_score = 0
        
        # Combine scores
        keyword_score = min(sensitive_count / 5, 1.0)  # Normalize
        final_score = max(keyword_score, toxicity_score)
        
        return final_score

    def extract_keywords(self, text: str) -> List[str]:
        """Extract relevant keywords from text"""
        doc = self.nlp(text)
        
        # Extract named entities and important nouns
        keywords = []
        for token in doc:
            if (token.pos_ in ['NOUN', 'PROPN'] and 
                len(token.text) > 3 and 
                not token.is_stop and 
                token.is_alpha):
                keywords.append(token.lemma_.lower())
        
        # Add named entities
        for ent in doc.ents:
            if ent.label_ in ['ORG', 'PERSON', 'GPE', 'EVENT']:
                keywords.append(ent.text.lower())
        
        return list(set(keywords))[:10]  # Limit to top 10 unique keywords

class NewsArticleFetcher:
    """Fetches and processes news articles from various sources"""
    
    def __init__(self, classifier: EducationalContentClassifier):
        self.classifier = classifier
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def fetch_rss_feed(self, url: str) -> List[Dict]:
        """Fetch RSS feed and return article data"""
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    content = await response.text()
                    feed = feedparser.parse(content)
                    
                    articles = []
                    for entry in feed.entries:
                        articles.append({
                            'title': entry.get('title', ''),
                            'url': entry.get('link', ''),
                            'published': entry.get('published', ''),
                            'summary': entry.get('summary', ''),
                            'source': feed.feed.get('title', url)
                        })
                    
                    return articles
                else:
                    logger.warning(f"Failed to fetch RSS feed {url}: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Error fetching RSS feed {url}: {e}")
            return []
    
    async def fetch_article_content(self, url: str) -> str:
        """Fetch full article content"""
        try:
            article = Article(url)
            article.download()
            article.parse()
            return article.text
        except Exception as e:
            logger.warning(f"Failed to fetch article content from {url}: {e}")
            return ""
    
    async def process_article(self, article_data: Dict, region: GeographicalRegion) -> Optional[NewsArticle]:
        """Process a single article and classify it"""
        try:
            # Fetch full content
            content = await self.fetch_article_content(article_data['url'])
            if not content:
                content = article_data.get('summary', '')
            
            # Parse publication date
            try:
                published_date = datetime.strptime(
                    article_data['published'], 
                    "%a, %d %b %Y %H:%M:%S %z"
                )
            except:
                published_date = datetime.now()
            
            # Classify content
            category, confidence = self.classifier.classify_content(
                article_data['title'], content
            )
            
            # Extract keywords
            keywords = self.classifier.extract_keywords(f"{article_data['title']} {content}")
            
            # Generate article hash for deduplication
            article_hash = hashlib.md5(
                f"{article_data['title']}{article_data['url']}".encode()
            ).hexdigest()
            
            # Create summary
            summary = content[:200] + "..." if len(content) > 200 else content
            
            return NewsArticle(
                title=article_data['title'],
                content=content,
                url=article_data['url'],
                source=article_data['source'],
                published_date=published_date,
                region=region,
                category=category,
                confidence_score=confidence,
                summary=summary,
                keywords=keywords,
                article_hash=article_hash
            )
            
        except Exception as e:
            logger.error(f"Error processing article {article_data.get('url', 'unknown')}: {e}")
            return None

class NewsDatabase:
    """SQLite database for storing processed articles"""
    
    def __init__(self, db_path: str = "educational_news.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database schema"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT,
                    url TEXT UNIQUE NOT NULL,
                    source TEXT,
                    published_date TIMESTAMP,
                    region TEXT,
                    category TEXT,
                    confidence_score REAL,
                    summary TEXT,
                    keywords TEXT,
                    article_hash TEXT UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_category ON articles(category)
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_region ON articles(region)
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_published ON articles(published_date)
            """)
    
    def save_article(self, article: NewsArticle) -> bool:
        """Save article to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO articles 
                    (title, content, url, source, published_date, region, category, 
                     confidence_score, summary, keywords, article_hash)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    article.title,
                    article.content,
                    article.url,
                    article.source,
                    article.published_date,
                    article.region.value,
                    article.category.value,
                    article.confidence_score,
                    article.summary,
                    json.dumps(article.keywords),
                    article.article_hash
                ))
                return True
        except sqlite3.IntegrityError:
            logger.info(f"Article already exists: {article.title}")
            return False
        except Exception as e:
            logger.error(f"Error saving article: {e}")
            return False
    
    def get_articles(self, 
                    region: Optional[GeographicalRegion] = None,
                    category: Optional[ContentCategory] = None,
                    days_back: int = 7,
                    limit: int = 100) -> List[Dict]:
        """Retrieve articles with filters"""
        query = "SELECT * FROM articles WHERE published_date >= ?"
        params = [datetime.now() - timedelta(days=days_back)]
        
        if region:
            query += " AND region = ?"
            params.append(region.value)
        
        if category:
            query += " AND category = ?"
            params.append(category.value)
        
        query += " ORDER BY published_date DESC LIMIT ?"
        params.append(limit)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

class EducationalNewsFilter:
    """Main system orchestrator"""
    
    def __init__(self):
        self.source_manager = NewsSourceManager()
        self.classifier = EducationalContentClassifier()
        self.database = NewsDatabase()
    
    async def fetch_and_process_news(self, 
                                   region: GeographicalRegion = GeographicalRegion.GLOBAL,
                                   max_articles_per_source: int = 20):
        """Fetch and process news from all sources for a region"""
        sources = self.source_manager.get_sources_for_region(region)
        logger.info(f"Processing {len(sources)} sources for region {region.value}")
        
        total_processed = 0
        total_educational = 0
        
        async with NewsArticleFetcher(self.classifier) as fetcher:
            for source_url in sources:
                logger.info(f"Fetching from: {source_url}")
                
                # Fetch RSS feed
                rss_articles = await fetcher.fetch_rss_feed(source_url)
                
                # Process articles
                for article_data in rss_articles[:max_articles_per_source]:
                    article = await fetcher.process_article(article_data, region)
                    
                    if article:
                        total_processed += 1
                        
                        # Save to database
                        if self.database.save_article(article):
                            if article.category == ContentCategory.EDUCATIONAL:
                                total_educational += 1
                                logger.info(f"Educational article saved: {article.title}")
        
        logger.info(f"Processing complete. Total: {total_processed}, Educational: {total_educational}")
        return total_processed, total_educational
    
    def get_educational_news(self, 
                           region: Optional[GeographicalRegion] = None,
                           days_back: int = 7,
                           limit: int = 50) -> List[Dict]:
        """Get filtered educational news"""
        return self.database.get_articles(
            region=region,
            category=ContentCategory.EDUCATIONAL,
            days_back=days_back,
            limit=limit
        )
    
    def get_filtered_news(self, 
                        region: Optional[GeographicalRegion] = None,
                        exclude_sensitive: bool = True,
                        days_back: int = 7,
                        limit: int = 50) -> List[Dict]:
        """Get general news with sensitive content filtered out"""
        articles = self.database.get_articles(
            region=region,
            days_back=days_back,
            limit=limit * 2  # Get more to filter
        )
        
        if exclude_sensitive:
            articles = [a for a in articles if a['category'] != ContentCategory.SENSITIVE.value]
        
        return articles[:limit]
    
    async def run_continuous_monitoring(self, interval_hours: int = 6):
        """Run continuous monitoring of news sources"""
        logger.info(f"Starting continuous monitoring every {interval_hours} hours")
        
        while True:
            try:
                # Process all regions
                for region in GeographicalRegion:
                    logger.info(f"Processing region: {region.value}")
                    await self.fetch_and_process_news(region)
                
                # Wait for next cycle
                await asyncio.sleep(interval_hours * 3600)
                
            except KeyboardInterrupt:
                logger.info("Monitoring stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in continuous monitoring: {e}")
                await asyncio.sleep(300)  # Wait 5 minutes before retry

# CLI Interface and Example Usage
async def main():
    """Main function demonstrating the system"""
    news_filter = EducationalNewsFilter()
    
    print("Educational News Filter System")
    print("=" * 50)
    
    # Fetch and process news
    print("\n1. Fetching and processing news...")
    total, educational = await news_filter.fetch_and_process_news(
        region=GeographicalRegion.GLOBAL,
        max_articles_per_source=10
    )
    
    print(f"Processed {total} articles, found {educational} educational articles")
    
    # Get educational news
    print("\n2. Latest educational news:")
    educational_articles = news_filter.get_educational_news(limit=5)
    
    for i, article in enumerate(educational_articles, 1):
        print(f"\n{i}. {article['title']}")
        print(f"   Source: {article['source']}")
        print(f"   Confidence: {article['confidence_score']:.2f}")
        print(f"   Summary: {article['summary'][:100]}...")
        print(f"   URL: {article['url']}")
    
    # Get filtered general news
    print("\n3. General news (sensitive content filtered):")
    general_articles = news_filter.get_filtered_news(
        exclude_sensitive=True,
        limit=3
    )
    
    for i, article in enumerate(general_articles, 1):
        print(f"\n{i}. {article['title']}")
        print(f"   Category: {article['category']}")
        print(f"   Source: {article['source']}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nSystem stopped by user")
    except Exception as e:
        print(f"System error: {e}")
        logger.error(f"System error: {e}")