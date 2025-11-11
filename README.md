# LinkedIn Scraper and Draft Generator

A comprehensive Python script for web scraping, content processing, LinkedIn post draft generation, and queue management. This tool automates the process of extracting relevant content from websites, analyzing it, and transforming it into professional LinkedIn post drafts.

## Features

- **Web Scraping Module**: Extracts content from blogs, articles, product updates, industry news, and sector-specific content (e-mobility, manufacturing, politics & governance).
- **Content Processing**: Uses NLP to identify key themes, extract insights, and categorize content by relevance and topic area.
- **LinkedIn Draft Generator**: Transforms processed content into LinkedIn post drafts with:
  - Professional tone optimization
  - Appropriate hashtag suggestions
  - Character limit compliance (3000 characters)
  - Call-to-action recommendations
- **Queue Management**: Organizes generated drafts for review and scheduling with persistence.

## Installation

1. Clone or download the project files.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Download the spaCy language model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Usage

### Setting Up URLs

1. Edit the `urls.txt` file and add your website URLs, one per line.
2. Lines starting with `#` are comments and will be ignored.
3. Example:
   ```
   # Company blog
   https://yourcompany.com/blog
   https://yourcompany.com/news

   # Industry news
   https://industrysite.com/articles
   ```

### Command Line Interface

Run the complete workflow with URLs from file:
```bash
python main.py --urls-file urls.txt
```

Or specify URLs directly:
```bash
python main.py --urls "https://example.com/blog1" "https://example.com/blog2"
```

Manage the queue:
```bash
# List drafts in queue
python main.py --queue list

# Get the next draft for review
python main.py --queue get

# Clear the queue
python main.py --queue clear
```

### Programmatic Usage

```python
from scraper import WebScraper
from processor import ContentProcessor
from generator import LinkedInDraftGenerator
from queue_manager import QueueManager

# Initialize components
scraper = WebScraper()
processor = ContentProcessor()
generator = LinkedInDraftGenerator()
queue = QueueManager()

# Scrape content
urls = ["https://example.com/article1", "https://example.com/article2"]
scraped = scraper.scrape_multiple_urls(urls)

# Process content
processed = processor.batch_process(scraped)

# Generate drafts
drafts = generator.batch_generate(processed)

# Add to queue
queue.batch_add_drafts(drafts)
```

## Modules

### scraper.py
Handles web scraping with:
- Polite request handling with delays
- Error handling and retries
- Content extraction from common article selectors
- Basic categorization

### processor.py
Processes scraped content using spaCy:
- Keyword extraction
- Theme identification
- Sentiment analysis
- Enhanced categorization

### generator.py
Generates LinkedIn drafts:
- Professional tone optimization
- Hashtag generation
- Character limit enforcement
- CTA suggestions

### queue_manager.py
Manages draft queue:
- FIFO operations
- JSON persistence
- Queue inspection and management

### main.py
Orchestrates the workflow and provides CLI interface.

## Configuration

- **User Agent**: Configurable in `WebScraper` class
- **spaCy Model**: Default `en_core_web_sm`, changeable in `ContentProcessor`
- **Character Limit**: 3000 characters for LinkedIn posts
- **Queue File**: `drafts_queue.json` for persistence

## Error Handling

The script includes comprehensive error handling:
- Network request failures with retries
- NLP processing errors
- File I/O errors for queue persistence
- Logging for debugging and monitoring

## Dependencies

- requests: HTTP requests
- beautifulsoup4: HTML parsing
- spacy: Natural language processing
- python-dotenv: Environment variable management (optional)

## Testing

Run individual modules for testing:
```bash
python scraper.py
python processor.py
python generator.py
python queue_manager.py
```

## License

This project is open-source. Please ensure compliance with website terms of service when scraping.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with proper documentation
4. Test thoroughly
5. Submit a pull request

## Disclaimer

This tool is for educational and professional use. Always respect website terms of service, robots.txt, and applicable laws when scraping content. Use responsibly and ethically.
