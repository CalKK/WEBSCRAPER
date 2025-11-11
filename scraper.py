import requests
from bs4 import BeautifulSoup
import logging
from urllib.parse import urljoin, urlparse
import time
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebScraper:
    """
    A modular web scraper for extracting content from websites.
    Focuses on blog posts, articles, product updates, industry news, and sector-specific content.
    Includes advanced content cleaning and filtering to maintain sector context and grammar.
    """

    def __init__(self, user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'):
        """
        Initialize the scraper with a default user agent.
        :param user_agent: String to use in request headers to mimic a browser.
        """
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': user_agent})
        self.session.headers.update({'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})
        self.session.headers.update({'Accept-Language': 'en-US,en;q=0.5'})
        self.session.headers.update({'Accept-Encoding': 'gzip, deflate'})
        self.session.headers.update({'Connection': 'keep-alive'})

        # Initialize NLTK components for content cleaning
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))

    def scrape_url(self, url, max_retries=3, delay=1):
        """
        Scrape content from a single URL with enhanced cleaning and filtering.
        :param url: The URL to scrape.
        :param max_retries: Number of retries in case of failure.
        :param delay: Delay between requests to avoid overwhelming the server.
        :return: Dict with 'title', 'content', 'url', or None if failed.
        """
        for attempt in range(max_retries):
            try:
                logger.info(f"Scraping URL: {url} (attempt {attempt + 1})")
                response = self.session.get(url, timeout=10)
                response.raise_for_status()

                soup = BeautifulSoup(response.content, 'html.parser')

                # Extract title
                title = soup.find('title')
                title_text = title.get_text().strip() if title else 'No title'

                # Extract main content - focus on common article/blog selectors
                content_selectors = [
                    'article', 'main', '.post-content', '.entry-content', '.article-body',
                    '.content', '[role="main"]', '.blog-post'
                ]
                content = ''
                for selector in content_selectors:
                    elements = soup.select(selector)
                    if elements:
                        content = ' '.join([elem.get_text().strip() for elem in elements])
                        if len(content) > 100:  # Basic check for relevance
                            break

                # If no content found, try body text
                if not content:
                    content = soup.get_text().strip()

                # Apply advanced content cleaning and filtering
                content = self._clean_and_filter_content(content, title_text)

                logger.info(f"Successfully scraped and cleaned {url}: {len(content)} characters")
                return {
                    'url': url,
                    'title': title_text,
                    'content': content
                }

            except requests.exceptions.RequestException as e:
                logger.error(f"Request error for {url} (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(delay * (attempt + 1))
                else:
                    logger.error(f"Failed to scrape {url} after {max_retries} attempts")
                    return None
            except Exception as e:
                logger.error(f"Unexpected error scraping {url}: {e}")
                return None

    def _clean_and_filter_content(self, content, title):
        """
        Advanced content cleaning and filtering to maintain sector context and grammar.
        :param content: Raw scraped content.
        :param title: Page title for context.
        :return: Cleaned and filtered content.
        """
        if not content:
            return ""

        # Step 1: Basic text cleaning
        content = self._basic_text_cleaning(content)

        # Step 2: Remove irrelevant content (navigation, ads, etc.)
        content = self._remove_irrelevant_content(content)

        # Step 3: Grammar and coherence filtering
        content = self._grammar_and_coherence_filter(content)

        # Step 4: Sector context filtering
        content = self._sector_context_filter(content, title)

        # Step 5: Final polishing
        content = self._final_polish(content)

        return content

    def _basic_text_cleaning(self, content):
        """
        Basic text cleaning: remove extra whitespace, normalize quotes, etc.
        """
        # Remove extra whitespace and normalize
        content = ' '.join(content.split())

        # Normalize quotes and apostrophes
        content = content.replace('"', '"').replace('"', '"')
        content = content.replace(''', "'").replace(''', "'")

        # Remove excessive punctuation
        content = re.sub(r'\.{3,}', '...', content)
        content = re.sub(r'!{2,}', '!', content)
        content = re.sub(r'\?{2,}', '?', content)

        return content

    def _remove_irrelevant_content(self, content):
        """
        Remove navigation elements, ads, and other irrelevant content.
        """
        # Remove common irrelevant phrases
        irrelevant_patterns = [
            r'\b(menu|navigation|nav|header|footer|sidebar|advertisement|ad|banner)\b',
            r'\bcopyright\s+\d{4}',
            r'\bprivacy\s+policy\b',
            r'\bterms\s+of\s+service\b',
            r'\bcontact\s+us\b',
            r'\babout\s+us\b',
            r'\bsign\s+in\b',
            r'\blog\s+in\b',
            r'\bsign\s+up\b',
            r'\bregister\b',
            r'\bnewsletter\b',
            r'\bsubscribe\b'
        ]

        for pattern in irrelevant_patterns:
            content = re.sub(pattern, '', content, flags=re.IGNORECASE)

        # Remove URLs and email addresses
        content = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', content)
        content = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', content)

        # Remove phone numbers
        content = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '', content)

        return ' '.join(content.split())

    def _grammar_and_coherence_filter(self, content):
        """
        Filter for grammatical correctness and coherence.
        """
        if not content:
            return ""

        # Split into sentences
        try:
            sentences = sent_tokenize(content)
        except:
            sentences = content.split('.')

        # Filter sentences based on grammar and coherence
        filtered_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if self._is_grammatical_sentence(sentence):
                filtered_sentences.append(sentence)

        # Rejoin sentences
        content = '. '.join(filtered_sentences)
        if content and not content.endswith('.'):
            content += '.'

        return content

    def _is_grammatical_sentence(self, sentence):
        """
        Basic check for grammatical sentence structure.
        """
        if len(sentence) < 10:  # Too short
            return False
        if len(sentence) > 500:  # Too long
            return False

        # Must contain at least one verb (basic check)
        words = word_tokenize(sentence.lower())
        if not words:
            return False

        # Check for basic sentence structure (subject + verb)
        has_noun = any(word.pos_ == 'NOUN' for word in nltk.pos_tag(words) if hasattr(word, 'pos_'))
        has_verb = any(tag.startswith('VB') for word, tag in nltk.pos_tag(words))

        return has_noun and has_verb

    def _sector_context_filter(self, content, title):
        """
        Filter content to maintain sector-specific context and relevance.
        """
        if not content:
            return ""

        # Define sector-specific context keywords
        sector_contexts = {
            'e-mobility': ['electric', 'vehicle', 'battery', 'charging', 'sustainable', 'mobility', 'green', 'energy', 'transport', 'autonomous'],
            'manufacturing': ['manufacture', 'production', 'supply', 'chain', 'automation', 'robotics', 'factory', 'industry', 'efficiency'],
            'politics-governance': ['government', 'policy', 'regulation', 'election', 'legislation', 'political', 'governance', 'law', 'minister'],
            'artificial intelligence & machine learning': ['artificial', 'intelligence', 'machine', 'learning', 'ai', 'algorithm', 'data', 'neural', 'deep'],
            'startup & innovation': ['startup', 'innovation', 'venture', 'entrepreneur', 'funding', 'business', 'model', 'disruption', 'scalability']
        }

        # Determine sector from title and content
        full_text = (title + ' ' + content).lower()
        sector_scores = {}

        for sector, keywords in sector_contexts.items():
            score = sum(1 for keyword in keywords if keyword in full_text)
            sector_scores[sector] = score

        # Find the most relevant sector
        best_sector = max(sector_scores, key=sector_scores.get) if sector_scores else None

        if best_sector and sector_scores[best_sector] > 0:
            # Filter sentences that are relevant to the sector
            try:
                sentences = sent_tokenize(content)
                relevant_sentences = []

                for sentence in sentences:
                    sentence_lower = sentence.lower()
                    if any(keyword in sentence_lower for keyword in sector_contexts[best_sector]):
                        relevant_sentences.append(sentence)

                if relevant_sentences:
                    content = '. '.join(relevant_sentences)
                    if not content.endswith('.'):
                        content += '.'
            except:
                pass  # Keep original content if sentence tokenization fails

        return content

    def _final_polish(self, content):
        """
        Final polishing: remove duplicates, improve readability.
        """
        if not content:
            return ""

        # Remove duplicate sentences
        try:
            sentences = sent_tokenize(content)
            unique_sentences = []
            seen = set()

            for sentence in sentences:
                normalized = sentence.lower().strip()
                if normalized not in seen and len(normalized) > 10:
                    unique_sentences.append(sentence)
                    seen.add(normalized)

            content = '. '.join(unique_sentences)
        except:
            pass

        # Final cleanup
        content = ' '.join(content.split())
        if content and not content.endswith('.'):
            content += '.'

        return content

    def scrape_multiple_urls(self, urls, delay_between=2):
        """
        Scrape multiple URLs sequentially with cleaning and filtering.
        :param urls: List of URLs to scrape.
        :param delay_between: Delay between scraping each URL.
        :return: List of scraped content dicts.
        """
        results = []
        for url in urls:
            result = self.scrape_url(url)
            if result:
                results.append(result)
            time.sleep(delay_between)  # Polite delay
        return results

    def categorize_content(self, content_dict):
        """
        Enhanced categorization based on keywords for sectors with stricter matching.
        Maintains pure sectoral context without mixing themes by using scoring and word boundaries.
        :param content_dict: Scraped content dict.
        :return: Dict with added 'category' key.
        """
        content = content_dict['content'].lower()
        title = content_dict.get('title', '').lower()
        full_text = content + ' ' + title  # Include title for better categorization

        # Define sector-specific keywords with higher precision - maintaining pure sectoral context
        sectors = {
            'e-mobility': [
                'electric vehicle', 'ev', 'battery', 'charging station', 'autonomous driving',
                'sustainable mobility', 'green energy', 'renewable transport', 'electric car',
                'lithium-ion', 'vehicle electrification', 'smart mobility', 'e-mobility'
            ],
            'manufacturing': [
                'manufacturing', 'supply chain', 'automation', 'industry 4.0', 'robotics',
                'production line', 'factory automation', 'industrial iot', 'smart manufacturing',
                'lean manufacturing', 'quality control', 'production efficiency'
            ],
            'politics-governance': [
                'government', 'policy', 'regulation', 'election', 'legislation', 'parliament',
                'political', 'governance', 'public sector', 'democracy', 'constitution',
                'minister', 'president', 'law', 'bill', 'senate'
            ],
            'artificial intelligence & machine learning': [
                'artificial intelligence', 'machine learning', 'deep learning', 'neural network',
                'data science', 'ai model', 'computer vision', 'natural language processing',
                'predictive analytics', 'algorithm', 'automation ai'
            ],
            'startup & innovation': [
                'startup', 'innovation', 'venture capital', 'tech startup', 'business model',
                'entrepreneurship', 'funding round', 'pitch deck', 'scalability', 'disruption'
            ]
        }

        # Score each sector based on keyword matches with word boundaries for precision
        scores = {}
        for sector, keywords in sectors.items():
            score = 0
            for keyword in keywords:
                # Count occurrences with word boundaries for precision
                score += len(re.findall(r'\b' + re.escape(keyword) + r'\b', full_text))
            scores[sector] = score

        # Find the sector with the highest score
        max_score = max(scores.values()) if scores else 0
        if max_score > 0:
            # If there's a clear winner (at least 2 matches), assign it
            top_sectors = [sector for sector, score in scores.items() if score == max_score]
            if len(top_sectors) == 1 or max_score >= 2:
                content_dict['category'] = top_sectors[0]
                return content_dict

        # Default to general if no clear categorization
        content_dict['category'] = 'general'
        return content_dict

# Example usage (for testing)
if __name__ == "__main__":
    scraper = WebScraper()
    sample_url = "https://example.com/blog-post"  # Replace with real URL
    result = scraper.scrape_url(sample_url)
    if result:
        print(f"Title: {result['title']}")
        print(f"Content preview: {result['content'][:200]}...")
    else:
        print("Scraping failed.")
