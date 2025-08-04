"""
Main module to execute the web scraping processes.
"""
import logging
import os
from scraper.techcrunch_scraper import TechCrunchScraper
from config.settings import Settings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    # Create output directory if it doesn't exist
    output_dir = Settings.get_output_directory()
    os.makedirs(output_dir, exist_ok=True)

    # Iterate over enabled website configurations
    for name, config in Settings.get_enabled_websites().items():
        logger.info(f"Starting scraper for {config.name}")
        
        # Initialize wired scraper
        scraper = TechCrunchScraper(config, Settings.USER_AGENT)

        # Scrape the articles
        try:
            articles = scraper.scrape_articles()
            for article in articles:
                save_article(article)
        finally:
            scraper.close()



def save_article(article: dict):
    """Save the scraped article to a file"""
    base_path = Settings.get_output_directory()
    article_path = os.path.join(base_path, article['filename'])
    article_path = article_path[:100]  # Limit path length

    # Save as plain text
    if 'markdown' in Settings.ARTICLE_FORMATS:
        with open(f"{article_path}.md", 'w', encoding='utf-8') as f:
            f.write(f"# {article['title']}\n")
            f.write(f"## {article['subtitle']}\n")
            f.write(f"{article['content_text']}\n")

    # Save as JSON
    if 'json' in Settings.ARTICLE_FORMATS:
        import json
        with open(f"{article_path}.json", 'w', encoding='utf-8') as f:
            json.dump(article, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
   main()

