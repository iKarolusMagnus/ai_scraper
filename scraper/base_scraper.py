"""
Base scraper class with common functionality for all website scrapers.
"""
import time
import requests
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import logging
from config.settings import WebsiteConfig

logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    """Abstract base class for website scrapers"""
    
    def __init__(self, config: WebsiteConfig, user_agent: str):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        self.scraped_urls = set()
        
    def get_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse a web page"""
        try:
            logger.info(f"Fetching: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Respect rate limiting
            time.sleep(self.config.delay_between_requests)
            
            return BeautifulSoup(response.content, 'lxml')
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def normalize_url(self, url: str) -> str:
        """Normalize URL to absolute form"""
        if url.startswith('http'):
            return url
        return urljoin(self.config.base_url, url)
    
    def is_valid_article_url(self, url: str) -> bool:
        """Check if URL is a valid article URL (to be implemented by subclasses)"""
        parsed = urlparse(url)
        return parsed.netloc and parsed.path
    
    @abstractmethod
    def get_article_links(self, soup: BeautifulSoup) -> List[str]:
        """Extract article links from listing page"""
        pass
    
    @abstractmethod
    def scrape_article(self, url: str) -> Optional[Dict]:
        """Scrape a single article and return structured data"""
        pass
    
    def scrape_articles(self, max_articles: Optional[int] = None) -> List[Dict]:
        """Main method to scrape articles from the configured website"""
        max_articles = max_articles or self.config.max_articles
        articles = []
        
        logger.info(f"Starting scrape of {self.config.name}")
        
        # Get the main listing page
        soup = self.get_page(self.config.article_list_url)
        if not soup:
            logger.error(f"Failed to fetch listing page: {self.config.article_list_url}")
            return articles
        
        # Extract article links
        article_links = self.get_article_links(soup)
        logger.info(f"Found {len(article_links)} article links")
        
        # Scrape individual articles
        for i, link in enumerate(article_links[:max_articles]):
            if link in self.scraped_urls:
                logger.debug(f"Skipping already scraped URL: {link}")
                continue
                
            article = self.scrape_article(link)
            if article:
                articles.append(article)
                self.scraped_urls.add(link)
                logger.info(f"Scraped article {i+1}/{max_articles}: {article.get('title', 'Unknown')}")
            else:
                logger.warning(f"Failed to scrape article: {link}")
        
        logger.info(f"Completed scraping {len(articles)} articles from {self.config.name}")
        return articles
    
    def close(self):
        """Clean up resources"""
        self.session.close()
