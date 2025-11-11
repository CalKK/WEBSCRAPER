import os
import logging
from openai import OpenAI
from typing import Optional, Dict, Any
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMCleaner:
    """
    A modular LLM-powered content cleaner using OpenAI's GPT models.
    Enhances scraped content with AI-driven cleaning, sector context maintenance,
    and professional polishing for LinkedIn drafts.
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """
        Initialize the LLM cleaner with OpenAI API.
        :param api_key: OpenAI API key (defaults to environment variable OPENAI_API_KEY)
        :param model: GPT model to use (default: gpt-3.5-turbo)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable or pass api_key parameter.")

        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        logger.info(f"Initialized LLM Cleaner with model: {model}")

    def clean_content(self, content_dict: Dict[str, Any], sector: str) -> Dict[str, Any]:
        """
        Clean and enhance scraped content using LLM.
        :param content_dict: Dict with 'title', 'content', 'url', 'category'
        :param sector: Target sector for context maintenance
        :return: Enhanced content dict with 'cleaned_content', 'key_insights', 'relevance_score'
        """
        title = content_dict.get('title', '')
        raw_content = content_dict.get('content', '')
        url = content_dict.get('url', '')

        if not raw_content.strip():
            logger.warning(f"No content to clean for {url}")
            content_dict.update({
                'cleaned_content': '',
                'key_insights': [],
                'relevance_score': 0.0
            })
            return content_dict

        # Prepare the cleaning prompt
        prompt = self._build_cleaning_prompt(title, raw_content, sector)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert content editor specializing in professional business content for LinkedIn. Your task is to clean, refine, and enhance scraped web content while maintaining strict sector relevance."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.3  # Lower temperature for more consistent cleaning
            )

            cleaned_text = response.choices[0].message.content.strip()

            # Parse the LLM response (assuming structured output)
            parsed_result = self._parse_llm_response(cleaned_text)

            content_dict.update({
                'cleaned_content': parsed_result.get('cleaned_content', cleaned_text),
                'key_insights': parsed_result.get('key_insights', []),
                'relevance_score': parsed_result.get('relevance_score', 0.5)
            })

            logger.info(f"LLM cleaned content for {url}: {len(cleaned_text)} characters, relevance: {content_dict['relevance_score']}")

        except Exception as e:
            logger.error(f"LLM cleaning failed for {url}: {e}")
            # Fallback to original content
            content_dict.update({
                'cleaned_content': raw_content,
                'key_insights': [],
                'relevance_score': 0.5
            })

        return content_dict

    def _build_cleaning_prompt(self, title: str, content: str, sector: str) -> str:
        """
        Build the cleaning prompt for the LLM.
        """
        sector_contexts = {
            'e-mobility': 'electric vehicles, batteries, charging infrastructure, sustainable transportation, autonomous driving',
            'manufacturing': 'industrial automation, supply chain, robotics, Industry 4.0, production processes',
            'politics-governance': 'government policy, regulation, legislation, public administration, political processes',
            'startup & innovation': 'entrepreneurship, venture capital, business models, innovation, startup ecosystem',
            'ai & ml': 'artificial intelligence, machine learning, data science, algorithms, automation',
            'general': 'business, technology, industry trends, professional development'
        }

        sector_keywords = sector_contexts.get(sector.lower(), sector_contexts['general'])

        return f"""
Please clean and refine the following scraped web content for professional LinkedIn posting. Focus on the {sector} sector.

TITLE: {title}
RAW CONTENT:
{content[:3000]}... (truncated for length)

SECTOR FOCUS: {sector_keywords}

TASKS:
1. Remove all irrelevant content (ads, navigation, contact info, legal text, etc.)
2. Maintain strict relevance to {sector} topics only
3. Fix grammar and improve readability
4. Extract 3-5 key insights or main points
5. Rate relevance to {sector} sector (0.0 to 1.0)
6. Ensure professional, coherent narrative

OUTPUT FORMAT (JSON):
{{
    "cleaned_content": "The cleaned and refined content here...",
    "key_insights": ["Insight 1", "Insight 2", "Insight 3"],
    "relevance_score": 0.85
}}

Ensure the cleaned content is suitable for LinkedIn professional posting and maintains sector purity.
"""

    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """
        Parse the LLM response, handling both JSON and plain text fallbacks.
        """
        try:
            # Try to parse as JSON
            return json.loads(response)
        except json.JSONDecodeError:
            # Fallback: extract content manually
            logger.warning("LLM response not valid JSON, using fallback parsing")
            return {
                'cleaned_content': response,
                'key_insights': [],
                'relevance_score': 0.5
            }

    def batch_clean(self, content_list: list, sector: str) -> list:
        """
        Clean multiple content items.
        :param content_list: List of content dicts
        :param sector: Target sector
        :return: List of cleaned content dicts
        """
        cleaned = []
        for content in content_list:
            try:
                cleaned.append(self.clean_content(content, sector))
            except Exception as e:
                logger.error(f"Batch cleaning failed for {content.get('url', 'unknown')}: {e}")
                cleaned.append(content)  # Return original if cleaning fails
        return cleaned

    def enhance_with_sector_context(self, content_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Additional enhancement to ensure sector context purity.
        """
        sector = content_dict.get('category', 'general')
        cleaned_content = content_dict.get('cleaned_content', '')

        if not cleaned_content:
            return content_dict

        # Use LLM to further refine sector context
        prompt = f"""
Analyze the following content and ensure it maintains pure {sector} sector context.
Remove any content that doesn't directly relate to {sector} topics.

CONTENT:
{cleaned_content}

Return only the content that is strictly relevant to {sector}, maintaining professional tone.
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a sector specialist ensuring content purity and relevance."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.2
            )

            enhanced_content = response.choices[0].message.content.strip()
            content_dict['cleaned_content'] = enhanced_content
            logger.info(f"Enhanced sector context for {sector}")

        except Exception as e:
            logger.error(f"Sector context enhancement failed: {e}")

        return content_dict

# Example usage (for testing)
if __name__ == "__main__":
    # Note: Requires OPENAI_API_KEY environment variable
    try:
        cleaner = LLMCleaner()
        sample_content = {
            'title': 'Electric Vehicle Market Trends',
            'content': 'The electric vehicle market is growing rapidly. Many companies are investing in battery technology. Navigation menu here. Contact us at info@company.com. Privacy policy applies.',
            'url': 'https://example.com/ev-trends',
            'category': 'e-mobility'
        }
        cleaned = cleaner.clean_content(sample_content, 'e-mobility')
        print("Cleaned content:", cleaned['cleaned_content'][:200])
        print("Key insights:", cleaned['key_insights'])
        print("Relevance score:", cleaned['relevance_score'])
    except ValueError as e:
        print(f"Setup required: {e}")
