# Configuration for AI Web Scraper
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import os

@dataclass
class WebsiteConfig:
    """Configuration for a specific website"""
    name: str
    base_url: str
    article_list_url: str
    article_selectors: Dict[str, str]
    max_articles: int = 25
    delay_between_requests: float = 3.0
    enabled: bool = True

class Settings:
    # Global settings
    OUTPUT_DIRECTORY = "output/articles"
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    LOG_LEVEL = "INFO"
    
    # Scheduling settings
    SCHEDULE_ENABLED = True
    SCHEDULE_DAY = "monday"  # Day of the week
    SCHEDULE_TIME = "09:00"  # Time in HH:MM format
    
    # Storage settings
    ARTICLE_FORMATS = ["markdown", "json"]
    KEEP_DUPLICATES = False
    MAX_STORAGE_DAYS = 365  # Keep articles for 1 year
    
    # Website configurations
    WEBSITES = {
        "techcrunch_space": WebsiteConfig(
            name="TechCrunch - Space",
            base_url="https://techcrunch.com",
            article_list_url="https://techcrunch.com/category/space/",
            article_selectors={
                "title": "h1",
                "subtitle": "",  # TechCrunch doesn't seem to have subtitles
                "author": ".byline-author a",
                "date": "time[datetime]",
                "content": ".entry-content",
                "article_links": "a[href*='/202']",  # TechCrunch uses year in URL
            },
            max_articles=25,
            delay_between_requests=3.0,
            enabled=True
        ),
        # Future websites can be added here
        # "wired_satellites": WebsiteConfig(...),  # Can re-enable later
        # "ars_technica_space": WebsiteConfig(...),
    }
    
    # Environment-based overrides
    @classmethod
    def get_output_directory(cls) -> str:
        return os.getenv("SCRAPER_OUTPUT_DIR", cls.OUTPUT_DIRECTORY)
    
    @classmethod
    def get_enabled_websites(cls) -> Dict[str, WebsiteConfig]:
        return {k: v for k, v in cls.WEBSITES.items() if v.enabled}
    
    @classmethod
    def is_production(cls) -> bool:
        return os.getenv("ENVIRONMENT", "development") == "production"

