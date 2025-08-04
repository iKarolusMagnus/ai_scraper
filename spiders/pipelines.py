# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import os
import hashlib
from datetime import datetime
from itemadapter import ItemAdapter
from spiders.items import extract_filename


class ArticleValidationPipeline:
    """Validate article items and add missing fields"""
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Ensure required fields exist
        if not adapter.get('title'):
            raise ValueError("Missing required field: title")
        
        if not adapter.get('url'):
            raise ValueError("Missing required field: url")
        
        # Add scraped timestamp
        adapter['scraped_at'] = datetime.now().isoformat()
        
        # Generate filename if not present
        if not adapter.get('filename'):
            adapter['filename'] = extract_filename(adapter['url'])
        
        # Set source from spider name if not present
        if not adapter.get('source'):
            adapter['source'] = spider.name
            
        return item


class DuplicatesPipeline:
    """Remove duplicate articles based on URL"""
    
    def __init__(self):
        self.urls_seen = set()
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        url = adapter['url']
        
        if url in self.urls_seen:
            spider.logger.info(f"Duplicate item found: {url}")
            raise ValueError(f"Duplicate item: {url}")
        else:
            self.urls_seen.add(url)
        
        return item


class JsonWriterPipeline:
    """Write articles to individual JSON files"""
    
    def __init__(self):
        self.output_dir = None
    
    def open_spider(self, spider):
        # Get output directory from settings
        self.output_dir = spider.settings.get('OUTPUT_DIR', 'output/articles')
        os.makedirs(self.output_dir, exist_ok=True)
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        filename = adapter.get('filename', 'unknown')
        
        # Write to individual JSON file
        json_path = os.path.join(self.output_dir, f"{filename}.json")
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(dict(adapter), f, ensure_ascii=False, indent=2)
        
        spider.logger.info(f"Saved JSON: {json_path}")
        return item


class MarkdownWriterPipeline:
    """Write articles to Markdown files"""
    
    def __init__(self):
        self.output_dir = None
    
    def open_spider(self, spider):
        # Get output directory from settings
        self.output_dir = spider.settings.get('OUTPUT_DIR', 'output/articles')
        os.makedirs(self.output_dir, exist_ok=True)
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        filename = adapter.get('filename', 'unknown')
        
        # Create markdown content
        content = self._create_markdown(adapter)
        
        # Write to markdown file
        md_path = os.path.join(self.output_dir, f"{filename}.md")
        
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        spider.logger.info(f"Saved Markdown: {md_path}")
        return item
    
    def _create_markdown(self, adapter):
        """Create markdown content from article data"""
        lines = []
        
        # Title
        if adapter.get('title'):
            lines.append(f"# {adapter['title']}")
            lines.append("")
        
        # Subtitle
        if adapter.get('subtitle'):
            lines.append(f"## {adapter['subtitle']}")
            lines.append("")
        
        # Metadata
        lines.append("---")
        
        if adapter.get('author'):
            lines.append(f"**Author:** {adapter['author']}")
        
        if adapter.get('published_date'):
            lines.append(f"**Published:** {adapter['published_date']}")
        
        if adapter.get('source'):
            lines.append(f"**Source:** {adapter['source']}")
        
        if adapter.get('url'):
            lines.append(f"**URL:** {adapter['url']}")
        
        if adapter.get('category'):
            lines.append(f"**Category:** {adapter['category']}")
        
        if adapter.get('tags'):
            tags = adapter['tags']
            if isinstance(tags, list):
                lines.append(f"**Tags:** {', '.join(tags)}")
            else:
                lines.append(f"**Tags:** {tags}")
        
        if adapter.get('reading_time'):
            lines.append(f"**Reading Time:** {adapter['reading_time']}")
        
        lines.append(f"**Scraped:** {adapter.get('scraped_at', 'N/A')}")
        lines.append("---")
        lines.append("")
        
        # Summary
        if adapter.get('summary'):
            lines.append("## Summary")
            lines.append("")
            lines.append(adapter['summary'])
            lines.append("")
        
        # Content
        if adapter.get('content_text'):
            lines.append("## Content")
            lines.append("")
            lines.append(adapter['content_text'])
        
        return "\n".join(lines)


class FilterSpacePipeline:
    """Filter articles to only include space/satellite related content"""
    
    SPACE_KEYWORDS = {
        'space', 'satellite', 'satellites', 'rocket', 'rockets', 'launch', 'orbit',
        'orbital', 'spacecraft', 'spacex', 'nasa', 'astronaut', 'mars', 'moon', 
        'lunar', 'solar', 'constellation', 'starlink', 'kuiper', 'oneweb', 
        'launch pad', 'falcon', 'starship', 'dragon', 'artemis', 'gateway',
        'iss', 'international space station', 'space station', 'space force',
        'space agency', 'rocket lab', 'blue origin', 'virgin galactic',
        'space exploration', 'space technology', 'space industry', 'spaceport',
        'space debris', 'space weather', 'space mission', 'space program'
    }
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Check if article contains space-related keywords
        text_to_check = []
        
        if adapter.get('title'):
            text_to_check.append(adapter['title'].lower())
        
        if adapter.get('subtitle'):
            text_to_check.append(adapter['subtitle'].lower())
        
        if adapter.get('content_text'):
            # Check first 500 characters for performance
            text_to_check.append(adapter['content_text'][:500].lower())
        
        combined_text = ' '.join(text_to_check)
        
        # Check for space keywords
        for keyword in self.SPACE_KEYWORDS:
            if keyword in combined_text:
                return item  # Keep the item
        
        # No space keywords found, drop the item
        spider.logger.info(f"Filtering out non-space article: {adapter.get('title', 'Unknown')}")
        raise ValueError("Article not related to space/satellites")
