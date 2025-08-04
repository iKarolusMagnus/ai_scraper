# AI Web Scraper

A focused web scraping tool designed to extract articles from a specific website and organize them in a structured directory format.

## 🎯 Project Overview

This tool scrapes articles from multiple websites and saves them as organized files in a structured directory format. Initially targeting Wired.com's satellites section, it's designed for easy expansion to additional websites. The scraper runs autonomously on a schedule, making it perfect for continuous content monitoring.

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
│   └── website_scraper.py
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

### Phase 1: Foundation Setup
- [ ] Set up project structure and virtual environment
- [ ] Install required dependencies (requests, BeautifulSoup4, etc.)
- [ ] Create configuration system for target website
- [ ] Implement basic logging

### Phase 2: Core Scraping
- [ ] Develop base scraper class with common functionality
- [ ] Implement website-specific scraper
- [ ] Add rate limiting and respectful crawling practices
- [ ] Handle different article URL patterns

### Phase 3: Content Processing
- [ ] Build article parser to extract title, content, metadata
- [ ] Implement content cleaning (remove ads, navigation, etc.)
- [ ] Add support for different content formats

### Phase 4: Storage System
- [ ] Create directory organization system
- [ ] Implement file naming conventions
- [ ] Add duplicate detection and handling
- [ ] Support multiple output formats (markdown, HTML, JSON)

### Phase 5: Enhanced Features
- [ ] Add scheduling/automation capabilities
- [ ] Implement progress tracking and resumption
- [ ] Add article filtering and search functionality
- [ ] Create summary reports

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

## 📋 Usage (Planned)

### Basic Usage
```bash
# Scrape articles from configured website
python main.py scrape

# Scrape with custom parameters
python main.py scrape --max-articles 50 --category tech

# List scraped articles
python main.py list

# Search scraped articles
python main.py search "keyword"
```

### Configuration
```python
# config/settings.py
TARGET_WEBSITE = "https://www.wired.com/tag/satellites/"
OUTPUT_DIRECTORY = "output/articles"
MAX_ARTICLES_PER_RUN = 50
DELAY_BETWEEN_REQUESTS = 3  # seconds (respectful to Wired)
ARTICLE_FORMATS = ["markdown", "json"]
USER_AGENT = "AI Scraper Bot 1.0 (Educational/Research Purpose)"
```

## 📊 Output Structure

Articles will be organized as follows:
```
output/articles/
├── 2024/
│   ├── 01/
│   │   ├── article-title-1.md
│   │   ├── article-title-1.json
│   │   └── article-title-2.md
│   └── 02/
│       └── ...
├── metadata.json
└── scraping_log.txt
```

## 🔧 Configuration Options

- **Website URL and selectors**
- **Output format preferences**
- **Rate limiting settings**
- **Content filtering rules**
- **Directory organization patterns**

## 🚀 Deployment Options

### Cloud Deployment (Recommended)
- **GitHub Actions**: Free scheduled execution with GitHub repos
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

### Target Website: Wired.com Satellites Section
- **URL**: https://www.wired.com/tag/satellites/
- **Focus**: Articles about satellites, space technology, and related topics
- **Content Type**: Technology journalism and analysis
- **Update Frequency**: Regular (daily/weekly)

### Content Extraction Goals
- Article title and subtitle
- Author name and publication date
- Full article content (cleaned)
- Article URL and metadata
- Tags and categories
- Image URLs (if needed)

---

**Note**: This is a living document that will be updated as the project evolves. Always ensure compliance with website terms of service and applicable laws when scraping content.
