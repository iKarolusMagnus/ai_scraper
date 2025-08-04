# AI Web Scraper

A focused web scraping tool designed to extract articles from a specific website and organize them in a structured directory format.

## 🎯 Project Overview

This tool scrapes articles from multiple websites and saves them as organized files in a structured directory format. Currently targeting TechCrunch's space section, it's designed for easy expansion to additional websites. The scraper runs autonomously on a schedule, making it perfect for continuous content monitoring.

## 🏗️ Architecture Plan

### Core Components

1. **Scraper Engine** (`scraper/`)
   - Website-specific scrapers
   - Content extraction logic
   - Rate limiting and respectful crawling

2. **Content Processor** (`processor/`)
   - Article parsing and cleaning
   - Metadata extraction (title, date, author, etc.)
   - Content formatting

3. **Storage Manager** (`storage/`)
   - Directory structure management
   - File naming conventions
   - Duplicate detection and handling

4. **Configuration** (`config/`)
   - Target website settings
   - Scraping parameters
   - Output preferences

## 📁 Project Structure

```
ai_scraper/
├── README.md
├── requirements.txt
├── main.py
├── config/
│   ├── __init__.py
│   └── settings.py
├── scraper/
│   ├── __init__.py
│   ├── base_scraper.py
│   ├── techcrunch_scraper.py
│   └── wired_scraper.py
├── processor/
│   ├── __init__.py
│   ├── article_parser.py
│   └── content_cleaner.py
├── storage/
│   ├── __init__.py
│   ├── file_manager.py
│   └── directory_organizer.py
├── utils/
│   ├── __init__.py
│   ├── helpers.py
│   └── logging_config.py
├── output/
│   └── articles/
│       └── [scraped articles will be stored here]
└── tests/
    ├── __init__.py
    ├── test_scraper.py
    ├── test_processor.py
    └── test_storage.py
```

## 🚀 Implementation Plan

### Phase 1: Foundation Setup ✅
- [x] Set up project structure and virtual environment
- [x] Install required dependencies (requests, BeautifulSoup4, etc.)
- [x] Create configuration system for target website
- [x] Implement basic logging

### Phase 2: Core Scraping ✅
- [x] Develop base scraper class with common functionality
- [x] Implement website-specific scraper (TechCrunch)
- [x] Add rate limiting and respectful crawling practices
- [x] Handle different article URL patterns

### Phase 3: Content Processing ✅
- [x] Build article parser to extract title, content, metadata
- [x] Implement content cleaning (remove ads, navigation, etc.)
- [x] Add support for different content formats

### Phase 4: Storage System ✅
- [x] Create directory organization system
- [x] Implement file naming conventions
- [x] Add duplicate detection and handling
- [x] Support multiple output formats (markdown, JSON)

### Phase 5: Automation & Deployment ✅
- [x] Add GitHub Actions workflow for automation
- [x] Implement weekly scheduling
- [x] Automatic commit and push of scraped articles
- [x] Manual trigger capability

## 🛠️ Technical Requirements

### Dependencies
- **Python 3.8+**
- **requests** - HTTP requests handling
- **BeautifulSoup4** - HTML parsing
- **lxml** - Fast XML/HTML parser
- **pydantic** - Data validation and settings management
- **click** - Command-line interface
- **schedule** - Task scheduling (optional)

### Target Website Considerations
- Respect robots.txt
- Implement appropriate delays between requests
- Handle dynamic content (if needed)
- Monitor for anti-bot measures

## 📋 Usage

### Running the Scraper
```bash
# Activate virtual environment (if used)
source .venv/bin/activate

# Scrape articles from configured website
python main.py
```

### Configuration
```python
# config/settings.py
WEBSITE_CONFIGS = [
    "techcrunch_space": WebsiteConfig(
        name="TechCrunch - Space",
        base_url="https://techcrunch.com",
        article_list_url="https://techcrunch.com/category/space/",
        article_selectors={
            "title": "h1",
            "author": ".byline-author a",
            "date": "time[datetime]",
            "content": ".entry-content",
            "article_links": "a[href*='/202']",
        },
        max_articles=25,
        delay_between_requests=3.0,
        enabled=True
    ),
]
```

## 📊 Output Structure

Articles are organized as follows:
```
output/articles/
├── [year]/
│   ├── [month]/
│   │   ├── article-title-1.md
│   │   ├── article-title-1.json
│   │   └── article-title-2.md
│   └── ...
├── metadata.json
└── scraping_log.txt
```

## 🔧 Configuration Options

- **Website URL and selectors**
- **Output format preferences**
- **Rate limiting settings**
- **Content filtering rules**
- **Directory organization patterns**

## 🤖 Automated Deployment (GitHub Actions)

### Current Setup ✅
The scraper is fully automated using GitHub Actions and runs:
- **Schedule**: Every Monday at 9:00 AM UTC
- **Manual Trigger**: Available via GitHub web interface or CLI
- **Auto-Commit**: New articles are automatically committed to the repository

### Managing the Automation

#### View Recent Runs
```bash
# View workflow runs
gh run list --workflow="scraper.yml"

# View detailed run information
gh run view [RUN_ID]
```

#### Manual Trigger
```bash
# Trigger scraper manually
gh workflow run "Web Scraper - Weekly Run"

# Via GitHub web interface
# Go to Actions tab → Web Scraper - Weekly Run → Run workflow
```

#### Monitor Results
- **GitHub Actions**: https://github.com/iKarolusMagnus/ai_scraper/actions
- **New Articles**: Check the `output/articles/` directory after each run
- **Commit History**: Each run creates a new commit with scraped articles

### Changing the Schedule
Edit `.github/workflows/scraper.yml` and modify the cron expression:
```yaml
schedule:
  - cron: '0 9 * * 1'  # Every Monday at 9 AM UTC
  # Examples:
  # - cron: '0 6 * * *'    # Daily at 6 AM UTC
  # - cron: '0 12 * * 0'   # Every Sunday at noon UTC
  # - cron: '0 0 1 * *'    # First day of each month
```

## 🚀 Alternative Deployment Options

### Other Cloud Options
- **AWS Lambda + EventBridge**: Serverless scheduled execution
- **Google Cloud Functions + Scheduler**: Serverless with Google Cloud
- **Heroku Scheduler**: Simple add-on for Heroku apps
- **DigitalOcean App Platform**: Managed deployment with cron jobs

### Self-Hosted Options
- **VPS with cron**: Traditional server-based scheduling
- **Docker containers**: Containerized deployment
- **Raspberry Pi**: Low-cost home automation

## 📈 Future Enhancements

- AI-powered content analysis and tagging
- Web interface for browsing scraped articles
- Integration with content management systems
- Advanced monitoring and alerting
- Multi-format export (RSS, API, etc.)

## 🤝 Contributing

1. Follow the established code structure
2. Add tests for new functionality
3. Update documentation for changes
4. Respect website terms of service

## ⚖️ Legal and Ethical Considerations

- Always check and respect robots.txt
- Follow website terms of service
- Implement reasonable rate limiting
- Only scrape publicly available content
- Consider reaching out to website owners for permission

## 📝 Development Notes

### Next Steps
1. Choose the specific target website
2. Set up the development environment
3. Begin with Phase 1 implementation
4. Test with a small subset of articles first

### Target Website: TechCrunch Space Section
- **URL**: https://techcrunch.com/category/space/
- **Focus**: Articles about space industry, technology, and startups
- **Content Type**: Technology journalism and analysis
- **Update Frequency**: Latest updates once a week (every Monday)

### Content Extraction Goals
- Article title and subtitle
- Author name and publication date
- Full article content (cleaned)
- Article URL and metadata
- Tags and categories
- Image URLs (if needed)

---

**Note**: This is a living document that will be updated as the project evolves. Always ensure compliance with website terms of service and applicable laws when scraping content.
