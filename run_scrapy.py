#!/usr/bin/env python3
"""
Main script to run Scrapy spiders for space and satellite news scraping.
"""

import os
import sys
import subprocess
import argparse
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Available spiders
SPIDERS = {
    'techcrunch': 'TechCrunch space articles',
    'theverge': 'The Verge space and satellite articles',
    'wired': 'Wired space and satellite articles',
    'uktn': 'UKTN space tech articles',
    'zdnet': 'ZDNet space articles',
    'copernicus': 'Copernicus Data Space Ecosystem news',
    'openaccess': 'Open Access Government space news'
}

def ensure_output_directory():
    """Ensure the output directory exists"""
    output_dir = Path("output/articles")
    output_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Output directory: {output_dir.absolute()}")

def run_spider(spider_name, extra_args=None):
    """Run a specific spider"""
    if spider_name not in SPIDERS:
        logger.error(f"Unknown spider: {spider_name}")
        logger.info(f"Available spiders: {', '.join(SPIDERS.keys())}")
        return False
    
    logger.info(f"Starting spider: {spider_name} - {SPIDERS[spider_name]}")
    
    # Build command
    cmd = ["scrapy", "crawl", spider_name]
    if extra_args:
        cmd.extend(extra_args)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info(f"Spider {spider_name} completed successfully")
            return True
        else:
            logger.error(f"Spider {spider_name} failed with return code {result.returncode}")
            logger.error(f"Error output: {result.stderr}")
            return False
            
    except FileNotFoundError:
        logger.error("Scrapy not found. Please install it with: pip install scrapy scrapy-user-agents")
        return False
    except Exception as e:
        logger.error(f"Unexpected error running spider {spider_name}: {e}")
        return False

def run_all_spiders(extra_args=None):
    """Run all available spiders"""
    logger.info("Starting all spiders...")
    
    successful = 0
    failed = 0
    
    for spider_name in SPIDERS.keys():
        if run_spider(spider_name, extra_args):
            successful += 1
        else:
            failed += 1
        
        logger.info("-" * 50)
    
    logger.info(f"Summary: {successful} successful, {failed} failed")
    return failed == 0

def main():
    parser = argparse.ArgumentParser(description="Run Scrapy spiders for space and satellite news")
    
    parser.add_argument(
        'spider',
        nargs='?',
        choices=list(SPIDERS.keys()) + ['all'],
        help='Spider to run (or "all" to run all spiders)'
    )
    
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='List available spiders'
    )
    
    parser.add_argument(
        '--output-format', '-o',
        choices=['json', 'csv', 'xml'],
        help='Output format (in addition to individual JSON/MD files)'
    )
    
    parser.add_argument(
        '--limit', '-n',
        type=int,
        help='Limit number of items to scrape per spider'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    if args.list:
        logger.info("Available spiders:")
        for name, description in SPIDERS.items():
            logger.info(f"  {name}: {description}")
        return
    
    if not args.spider:
        parser.print_help()
        return
    
    # Ensure output directory exists
    ensure_output_directory()
    
    # Build extra arguments for Scrapy
    extra_args = []
    
    if args.output_format:
        extra_args.extend(['-o', f'output/articles/scrapy_output.{args.output_format}'])
    
    if args.limit:
        extra_args.extend(['-s', f'CLOSESPIDER_ITEMCOUNT={args.limit}'])
    
    if args.verbose:
        extra_args.extend(['-s', 'LOG_LEVEL=DEBUG'])
    
    # Run the spider(s)
    if args.spider == 'all':
        success = run_all_spiders(extra_args)
    else:
        success = run_spider(args.spider, extra_args)
    
    if success:
        logger.info("✅ Scraping completed successfully!")
        logger.info("Check the output/articles/ directory for scraped articles")
    else:
        logger.error("❌ Scraping failed!")
        sys.exit(1)

if __name__ == '__main__':
    main()
