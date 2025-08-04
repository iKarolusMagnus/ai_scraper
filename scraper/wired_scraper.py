"""
Wired.com specific scraper implementation.
"""
import re
from typing import List, Dict, Optional
from datetime import datetime
from bs4 import BeautifulSoup
import logging
from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)

class TechCrunchScraper(BaseScraper):
    """Scraper specifically designed for TechCrunch.com articles"""
    
    def get_article_links(self, soup: BeautifulSoup) -e List[str]:
        """Extract article links from TechCrunch listing page"""
        links = []
        
        # TechCrunch uses year-based URLs, let's try multiple selectors
        selectors = [
            'a[href*="/202"]',  # Main article links with year
            'h3 a[href*="/202"]',  # Headlines with year links
            '.post-title a',  # Post title links
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            for element in elements:
                href = element.get('href')
                if href:
                    full_url = self.normalize_url(href)
                    if self.is_valid_techcrunch_article_url(full_url):
                        links.append(full_url)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_links = []
        for link in links:
            if link not in seen:
                seen.add(link)
                unique_links.append(link)
        
        return unique_links
    
    def is_valid_techcrunch_article_url(self, url: str) -> bool:
        """Check if URL is a valid TechCrunch article URL"""
        return (
            'techcrunch.com' in url and 
            '/202' in url and  # Year-based URLs
            not any(exclude in url for exclude in ['/events/', '/video/', '/podcast/', '/tag/'])
        )
    
    def scrape_article(self, url: str) -> Optional[Dict]:
        """Scrape a single TechCrunch article"""
        soup = self.get_page(url)
        if not soup:
            return None
        
        try:
            article_data = {
                'url': url,
                'source': 'TechCrunch',
                'scraped_at': datetime.now().isoformat(),
            }
            
            # Extract title
            title_element = soup.select_one(self.config.article_selectors['title'])
            article_data['title'] = title_element.get_text(strip=True) if title_element else 'Unknown Title'
            
            # Extract subtitle/deck
            subtitle_element = soup.select_one(self.config.article_selectors['subtitle'])
            article_data['subtitle'] = subtitle_element.get_text(strip=True) if subtitle_element else ''
            
            # Extract author
            author_element = soup.select_one(self.config.article_selectors['author'])
            article_data['author'] = author_element.get_text(strip=True) if author_element else 'Unknown Author'
            
            # Extract publish date
            date_element = soup.select_one(self.config.article_selectors['date'])
            if date_element:
                datetime_attr = date_element.get('datetime')
                if datetime_attr:
                    try:
                        article_data['published_date'] = datetime.fromisoformat(datetime_attr.replace('Z', '+00:00')).isoformat()
                    except ValueError:
                        article_data['published_date'] = datetime_attr
                else:
                    article_data['published_date'] = date_element.get_text(strip=True)
            else:
                article_data['published_date'] = 'Unknown Date'
            
            # Extract content using TechCrunch-specific approaches
            content_element = (
                soup.select_one(self.config.article_selectors['content']) or
                soup.find('div', class_='wp-block-post-content') or
                soup.find('div', class_='entry-content') or
                soup.find('article')
            )
            
            if content_element:
                # Extract all paragraphs for better content capture
                paragraphs = content_element.find_all('p')
                article_text = '\n\n'.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
                
                article_data['content'] = self.clean_content(content_element)
                article_data['content_text'] = article_text
            else:
                logger.warning(f"No content found for article: {url}")
                article_data['content'] = ''
                article_data['content_text'] = ''
            
            # Extract tags/categories (if available)
            article_data['tags'] = self.extract_tags(soup)
            
            # Generate a clean filename-safe title
            article_data['filename'] = self.generate_filename(article_data['title'], article_data.get('published_date', ''))
            
            return article_data
        
        except Exception as e:
            logger.error(f"Error scraping article {url}: {e}")
            return None
    
    def clean_content(self, content_element: BeautifulSoup) -> str:
        """Clean article content by removing unwanted elements"""
        # Remove unwanted elements
        unwanted_selectors = [
            '.ad', '.advertisement', '.promo', '.newsletter-signup',
            '.social-share', '.related-articles', '.author-bio',
            'script', 'style', 'nav', '.paywall'
        ]
        
        for selector in unwanted_selectors:
            for element in content_element.select(selector):
                element.decompose()
        
        # Convert to HTML string
        return str(content_element)
    
    def extract_tags(self, soup: BeautifulSoup) -> List[str]:
        """Extract tags/categories from the article page"""
        tags = []
        
        # Try different tag selectors
        tag_selectors = [
            '.TagCloudLink a',
            '.ArticleTags a',
            '[data-testid="TagCloud"] a',
            '.tags a'
        ]
        
        for selector in tag_selectors:
            elements = soup.select(selector)
            for element in elements:
                tag = element.get_text(strip=True)
                if tag and tag not in tags:
                    tags.append(tag)
        
        return tags
    
    def generate_filename(self, title: str, date: str) -> str:
        """Generate a clean filename from title and date"""
        # Clean title for filename
        clean_title = re.sub(r'[^\w\s-]', '', title)
        clean_title = re.sub(r'[-\s]+', '-', clean_title)
        clean_title = clean_title.strip('-').lower()
        
        # Extract date prefix if available
        date_prefix = ''
        if date and date != 'Unknown Date':
            try:
                if 'T' in date:  # ISO format
                    date_obj = datetime.fromisoformat(date.replace('Z', '+00:00'))
                else:
                    date_obj = datetime.strptime(date, '%Y-%m-%d')
                date_prefix = date_obj.strftime('%Y%m%d-')
            except ValueError:
                pass
        
        filename = f"{date_prefix}{clean_title}"
        return filename[:100]  # Limit filename length
