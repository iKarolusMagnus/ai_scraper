# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, Compose, MapCompose
from w3lib.html import remove_tags
import re


def clean_text(text):
    """Clean text by removing extra whitespace and normalizing"""
    if not text:
        return ""
    # Remove HTML tags
    text = remove_tags(text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_filename(url):
    """Extract a filename from URL and title"""
    import urllib.parse
    from datetime import datetime
    
    # Get base name from URL
    parsed = urllib.parse.urlparse(url)
    path_parts = parsed.path.strip('/').split('/')
    base_name = path_parts[-1] if path_parts and path_parts[-1] else 'article'
    
    # Remove file extension and clean
    base_name = re.sub(r'\.[^.]*$', '', base_name)
    base_name = re.sub(r'[^\w\-]', '-', base_name)
    base_name = re.sub(r'-+', '-', base_name).strip('-')
    
    # Add date prefix
    date_prefix = datetime.now().strftime('%Y%m%d')
    filename = f"{date_prefix}-{base_name}"
    
    return filename[:100]  # Limit length


class ArticleItem(scrapy.Item):
    """Main article item with all relevant fields"""
    
    # Basic article information
    title = scrapy.Field(
        input_processor=MapCompose(clean_text),
        output_processor=TakeFirst()
    )
    
    subtitle = scrapy.Field(
        input_processor=MapCompose(clean_text),
        output_processor=TakeFirst()
    )
    
    url = scrapy.Field(
        output_processor=TakeFirst()
    )
    
    # Content fields
    content_text = scrapy.Field(
        input_processor=MapCompose(clean_text),
        output_processor=TakeFirst()
    )
    
    content_html = scrapy.Field(
        output_processor=TakeFirst()
    )
    
    # Metadata fields
    author = scrapy.Field(
        input_processor=MapCompose(clean_text),
        output_processor=TakeFirst()
    )
    
    published_date = scrapy.Field(
        output_processor=TakeFirst()
    )
    
    source = scrapy.Field(
        output_processor=TakeFirst()
    )
    
    category = scrapy.Field(
        input_processor=MapCompose(clean_text),
        output_processor=TakeFirst()
    )
    
    tags = scrapy.Field()
    
    # Technical fields
    scraped_at = scrapy.Field(
        output_processor=TakeFirst()
    )
    
    filename = scrapy.Field(
        input_processor=MapCompose(str),
        output_processor=TakeFirst()
    )
    
    # Additional fields for specific sources
    image_urls = scrapy.Field()
    reading_time = scrapy.Field(
        output_processor=TakeFirst()
    )
    
    summary = scrapy.Field(
        input_processor=MapCompose(clean_text),
        output_processor=TakeFirst()
    )
