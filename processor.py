import nltk
import logging
from collections import Counter
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

class ContentProcessor:
    """
    A modular content processor for analyzing scraped text.
    Uses NLTK for NLP tasks like keyword extraction, theme identification, and categorization.
    """

    def __init__(self):
        """
        Initialize the processor with NLTK components.
        """
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        logger.info("Initialized NLTK-based ContentProcessor")

    def process_content(self, content_dict):
        """
        Process a single content dict: extract keywords, themes, and enhance categorization.
        :param content_dict: Dict with 'title', 'content', 'url', 'category'.
        :return: Enhanced dict with 'keywords', 'themes', 'sentiment'.
        """
        text = content_dict['content']

        # Tokenize and preprocess
        sentences = sent_tokenize(text)
        words = word_tokenize(text.lower())

        # Remove punctuation and filter
        words = [word for word in words if word.isalnum()]

        # Remove stop words and lemmatize
        filtered_words = [self.lemmatizer.lemmatize(word) for word in words if word not in self.stop_words and len(word) > 2]

        # Extract keywords (most common words)
        keyword_freq = Counter(filtered_words)
        top_keywords = [kw for kw, _ in keyword_freq.most_common(10)]

        # Identify themes (common bigrams/trigrams from sentences)
        themes = []
        for sentence in sentences:
            words_in_sent = word_tokenize(sentence.lower())
            words_in_sent = [w for w in words_in_sent if w.isalnum() and w not in self.stop_words]
            # Simple bigram extraction
            for i in range(len(words_in_sent) - 1):
                bigram = f"{words_in_sent[i]} {words_in_sent[i+1]}"
                themes.append(bigram)

        theme_freq = Counter(themes)
        top_themes = [theme for theme, _ in theme_freq.most_common(5)]

        # Basic sentiment analysis (simple polarity based on positive/negative words)
        positive_words = {'good', 'great', 'excellent', 'positive', 'innovative', 'successful', 'beneficial'}
        negative_words = {'bad', 'poor', 'negative', 'problematic', 'challenging', 'difficult', 'issue'}
        words_set = set(filtered_words)
        positive_count = len(words_set & positive_words)
        negative_count = len(words_set & negative_words)
        sentiment = 'neutral'
        if positive_count > negative_count:
            sentiment = 'positive'
        elif negative_count > positive_count:
            sentiment = 'negative'

        # Enhance category based on keywords
        enhanced_category = self._enhance_category(content_dict['category'], top_keywords)

        content_dict.update({
            'keywords': top_keywords,
            'themes': top_themes,
            'sentiment': sentiment,
            'category': enhanced_category
        })

        logger.info(f"Processed content from {content_dict['url']}: {len(top_keywords)} keywords, {len(top_themes)} themes")
        return content_dict

    def _enhance_category(self, base_category, keywords):
        """
        Enhance the category based on extracted keywords.
        :param base_category: Original category from scraper.
        :param keywords: List of top keywords.
        :return: Enhanced category string.
        """
        keyword_str = ' '.join(keywords).lower()
        if 'electric' in keyword_str or 'vehicle' in keyword_str or 'battery' in keyword_str:
            return 'e-mobility'
        elif 'manufactur' in keyword_str or 'supply' in keyword_str or 'automation' in keyword_str:
            return 'manufacturing'
        elif 'government' in keyword_str or 'policy' in keyword_str or 'regulation' in keyword_str:
            return 'politics-governance'
        else:
            return base_category

    def batch_process(self, content_list):
        """
        Process a list of content dicts.
        :param content_list: List of content dicts.
        :return: List of processed dicts.
        """
        processed = []
        for content in content_list:
            try:
                processed.append(self.process_content(content))
            except Exception as e:
                logger.error(f"Error processing content from {content.get('url', 'unknown')}: {e}")
                processed.append(content)  # Return original if processing fails
        return processed

    def extract_insights(self, processed_content_list):
        """
        Extract overall insights from a list of processed content.
        :param processed_content_list: List of processed content dicts.
        :return: Dict with aggregated insights.
        """
        all_keywords = []
        all_themes = []
        categories = Counter()
        sentiments = Counter()

        for content in processed_content_list:
            all_keywords.extend(content.get('keywords', []))
            all_themes.extend(content.get('themes', []))
            categories[content.get('category', 'unknown')] += 1
            sentiments[content.get('sentiment', 'neutral')] += 1

        top_keywords = [kw for kw, _ in Counter(all_keywords).most_common(20)]
        top_themes = [theme for theme, _ in Counter(all_themes).most_common(10)]

        insights = {
            'total_content': len(processed_content_list),
            'top_keywords': top_keywords,
            'top_themes': top_themes,
            'category_distribution': dict(categories),
            'sentiment_distribution': dict(sentiments)
        }

        logger.info(f"Extracted insights from {len(processed_content_list)} content items")
        return insights

# Example usage (for testing)
if __name__ == "__main__":
    processor = ContentProcessor()
    sample_content = {
        'url': 'https://example.com',
        'title': 'Sample Article',
        'content': 'This is a sample article about electric vehicles and manufacturing innovations in the automotive industry.',
        'category': 'general'
    }
    processed = processor.process_content(sample_content)
    print(f"Keywords: {processed['keywords']}")
    print(f"Themes: {processed['themes']}")
    print(f"Category: {processed['category']}")
    print(f"Sentiment: {processed['sentiment']}")
