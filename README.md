# LinkedIn Content Scraper & Draft Generator

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5--turbo-412991)](https://openai.com/)

An intelligent web scraping and content processing system that transforms industry news and articles into professional LinkedIn post drafts. Features advanced content cleaning with optional AI-powered refinement using OpenAI's GPT models, ensuring sector-specific relevance and high-quality thought leadership content.

## 🚀 Features

- **Intelligent Web Scraping**: Extracts content from blogs, news sites, and industry publications
- **Multi-Layer Content Cleaning**: Removes ads, navigation, and irrelevant content while maintaining sector purity
- **AI-Powered Enhancement**: Optional LLM cleaning using OpenAI GPT for professional content refinement
- **Sector-Aware Processing**: Specialized handling for e-mobility, manufacturing, politics-governance, AI/ML, and startup sectors
- **Automated Draft Generation**: Creates LinkedIn-ready posts with hashtags, CTAs, and optimal formatting
- **Queue Management**: Persistent draft storage and retrieval system
- **Graphical User Interface**: Tkinter-based UI for easy operation
- **Modular Architecture**: Clean separation of scraping, processing, generation, and queuing components

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Configuration](#configuration)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)
- [Troubleshooting](#troubleshooting)

## 🛠 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Optional: OpenAI API key for LLM features

### Step-by-Step Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/linkedin-scraper.git
   cd linkedin-scraper
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download NLTK data (required for text processing):**
   ```bash
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger')"
   ```

5. **Set up OpenAI API key (optional, for LLM features):**
   ```bash
   export OPENAI_API_KEY='your-api-key-here'  # Linux/Mac
   # or
   set OPENAI_API_KEY=your-api-key-here  # Windows
   ```

### Dependencies

- `requests==2.31.0` - HTTP requests for web scraping
- `beautifulsoup4==4.12.2` - HTML parsing
- `nltk==3.8.1` - Natural language processing
- `python-dotenv==1.0.0` - Environment variable management
- `openai==1.3.0` - AI-powered content cleaning (optional)

## 🚀 Quick Start

1. **Prepare URLs file:**
   Create a `urls.txt` file with one URL per line:
   ```
   https://techcrunch.com/category/startups/
   https://www.theverge.com/tech
   https://www.reuters.com/technology/
   ```

2. **Run the scraper:**
   ```bash
   python main_llm.py --urls-file urls.txt --use-llm
   ```

3. **Retrieve generated drafts:**
   ```bash
   python main_llm.py --queue get
   ```

## 📖 Usage

### Command Line Interface

#### Basic Scraping
```bash
# Scrape from URLs file
python main_llm.py --urls-file urls.txt

# Scrape specific URLs
python main_llm.py --urls https://example.com/article1 https://example.com/article2
```

#### Advanced Scraping with LLM
```bash
# Enable AI-powered content cleaning
python main_llm.py --urls-file urls.txt --use-llm

# Use different LLM model
python main_llm.py --urls-file urls.txt --use-llm --llm-model gpt-4
```

#### Queue Management
```bash
# List drafts in queue
python main_llm.py --queue list

# Get next draft
python main_llm.py --queue get

# Clear all drafts
python main_llm.py --queue clear
```

#### GUI Mode
```bash
# Launch graphical interface
python ui.py
```

### Python API Usage

```python
from scraper import WebScraper
from processor_llm import ContentProcessor
from generator import LinkedInDraftGenerator
from queue_manager import QueueManager

# Initialize components
scraper = WebScraper()
processor = ContentProcessor(use_llm=True)  # Enable LLM cleaning
generator = LinkedInDraftGenerator()
queue = QueueManager()

# Scrape content
urls = ['https://example.com/tech-news']
scraped = scraper.scrape_multiple_urls(urls)

# Process and categorize
processed = processor.batch_process(scraped)

# Generate drafts
drafts = generator.batch_generate(processed)

# Queue drafts
queue.batch_add_drafts(drafts)

# Retrieve draft
draft = queue.get_next_draft()
print(draft['draft'])
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for LLM features | Optional |

### Configuration Options

#### Scraper Configuration
- **User Agent**: Customizable browser user agent
- **Request Timeout**: Default 10 seconds
- **Retry Attempts**: Default 3 retries with exponential backoff
- **Delay Between Requests**: Polite scraping with configurable delays

#### Processor Configuration
- **LLM Model**: Choose between `gpt-3.5-turbo` or `gpt-4`
- **Sector Keywords**: Customizable sector definitions
- **Content Filters**: Adjustable relevance thresholds

#### Generator Configuration
- **Character Limits**: LinkedIn post length constraints
- **Hashtag Limits**: Maximum hashtags per post
- **CTA Options**: Customizable call-to-action phrases

### Advanced Configuration

Create a `.env` file for persistent configuration:
```
OPENAI_API_KEY=your-api-key-here
LLM_MODEL=gpt-3.5-turbo
MAX_RETRIES=3
REQUEST_DELAY=2
```

## 📚 API Reference

### WebScraper Class

```python
class WebScraper:
    def scrape_url(url: str, max_retries: int = 3, delay: float = 1) -> Dict
    def scrape_multiple_urls(urls: List[str], delay_between: float = 2) -> List[Dict]
    def categorize_content(content_dict: Dict) -> Dict
```

### ContentProcessor Class

```python
class ContentProcessor:
    def __init__(self, use_llm: bool = False, llm_model: str = "gpt-3.5-turbo")
    def process_content(content_dict: Dict) -> Dict
    def batch_process(content_list: List[Dict]) -> List[Dict]
    def extract_insights(processed_content_list: List[Dict]) -> Dict
```

### LinkedInDraftGenerator Class

```python
class LinkedInDraftGenerator:
    def generate_draft(processed_content: Dict) -> Dict
    def batch_generate(processed_content_list: List[Dict]) -> List[Dict]
```

### QueueManager Class

```python
class QueueManager:
    def add_draft(draft_dict: Dict) -> None
    def get_next_draft() -> Dict
    def peek_next_draft() -> Dict
    def queue_size() -> int
    def list_queue(limit: int = 5) -> List[Dict]
    def clear_queue() -> None
```

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Install development dependencies: `pip install -r requirements-dev.txt`
4. Run tests: `python -m pytest`
5. Commit changes: `git commit -am 'Add your feature'`
6. Push to branch: `git push origin feature/your-feature-name`
7. Submit a pull request

### Code Standards

- Follow PEP 8 style guidelines
- Add docstrings to all functions and classes
- Write unit tests for new features
- Update documentation for API changes

### Testing

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=src --cov-report=html

# Run specific test file
python -m pytest tests/test_scraper.py
```

### Issue Reporting

- Use GitHub Issues for bug reports and feature requests
- Include detailed steps to reproduce bugs
- Provide sample URLs and expected vs. actual behavior

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 LinkedIn Scraper Project

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Import Errors
**Problem:** `ModuleNotFoundError` when running the application.

**Solution:**
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt

# Check Python version
python --version  # Should be 3.8+

# Reinstall in virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### 2. NLTK Data Missing
**Problem:** NLTK-related errors during processing.

**Solution:**
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger')"
```

#### 3. OpenAI API Errors
**Problem:** LLM features not working.

**Solutions:**
- Verify API key: `echo $OPENAI_API_KEY`
- Check API quota and billing
- Use fallback mode: Remove `--use-llm` flag
- Test API key: `python -c "import openai; openai.api_key='your-key'; print('API key valid')"`

#### 4. Scraping Failures
**Problem:** Websites blocking or returning empty content.

**Solutions:**
- Check URL validity and accessibility
- Add delays between requests: `--delay 3`
- Use different user agent strings
- Verify website allows scraping (check robots.txt)

#### 5. Memory Issues
**Problem:** Large content causing memory errors.

**Solution:**
- Process URLs in smaller batches
- Implement content size limits in scraper
- Use streaming for large content

#### 6. Queue Persistence Issues
**Problem:** Drafts not saving between runs.

**Solution:**
- Check write permissions in current directory
- Verify `drafts_queue.json` is not corrupted
- Clear queue and restart: `python main_llm.py --queue clear`

### Performance Optimization

- **Batch Processing:** Process multiple URLs together for efficiency
- **Caching:** Implement response caching to avoid redundant requests
- **Async Operations:** Consider asyncio for concurrent scraping (future enhancement)
- **Database Storage:** Migrate from JSON to SQLite for larger queues

### Getting Help

- **Documentation:** Check this README and inline code documentation
- **Issues:** Search existing GitHub issues for similar problems
- **Community:** Join discussions in GitHub Discussions
- **Logs:** Enable debug logging: Set logging level to DEBUG

### Debug Mode

Enable detailed logging for troubleshooting:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🙏 Acknowledgments

- OpenAI for GPT model access
- NLTK contributors for natural language processing tools
- Beautiful Soup and Requests libraries for web scraping
- Python community for excellent documentation and support

---

**Made with ❤️ for content creators and thought leaders**

For questions or support, please open an issue on GitHub or contact the maintainers.
