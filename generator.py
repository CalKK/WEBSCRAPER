import logging
import re
from collections import Counter

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LinkedInDraftGenerator:
    """
    A modular generator for creating LinkedIn post drafts from processed content.
    Optimizes for professional tone, adds hashtags, ensures character limits, and suggests CTAs.
    """

    def __init__(self):
        # LinkedIn character limit (including spaces and emojis)
        self.max_chars = 3000
        # Common hashtags by category
        self.category_hashtags = {
            'e-mobility': ['#ElectricVehicles', '#EV', '#SustainableMobility', '#GreenEnergy', '#Innovation'],
            'manufacturing': ['#Manufacturing', '#Industry40', '#Automation', '#SupplyChain', '#Engineering'],
            'politics-governance': ['#Policy', '#Governance', '#Politics', '#Regulation', '#PublicSector'],
            'general': ['#Business', '#Technology', '#News', '#Insights', '#ProfessionalDevelopment']
        }
        # CTA suggestions
        self.ctas = [
            "What are your thoughts on this? Share in the comments below!",
            "Have you experienced something similar? Let's discuss!",
            "Check out the full article for more details.",
            "How is this impacting your industry?",
            "Tag a colleague who might find this interesting!"
        ]

    def generate_draft(self, processed_content):
        """
        Generate a meticulously crafted, opinion-based LinkedIn post draft from processed content.
        Creates exquisite, flowing opinion articles with deep context, personal insights, and professional polish.
        :param processed_content: Dict with processed content data.
        :return: Dict with 'draft', 'hashtags', 'character_count', 'cta'.
        """
        title = processed_content.get('title', '')
        content = processed_content.get('content', '')
        keywords = processed_content.get('keywords', [])
        themes = processed_content.get('themes', [])
        category = processed_content.get('category', 'general')
        sentiment = processed_content.get('sentiment', 'neutral')
        url = processed_content.get('url', '')

        # Create draft structure with sophisticated flow
        draft_parts = []

        # Elegant opening with contextual hook
        category_display = category.replace('-', ' ').title()
        if sentiment == 'positive':
            hook = f"As someone deeply immersed in the {category_display} landscape, I'm genuinely excited about the transformative developments unfolding before our eyes. 🚀 Let me share my perspective on why these changes represent a pivotal moment for our industry."
        elif sentiment == 'negative':
            hook = f"Having closely followed the {category_display} sector, I'm increasingly concerned about the challenges that demand our immediate attention. 🤔 The recent developments highlight systemic issues that we can no longer afford to ignore."
        else:
            hook = f"In my ongoing analysis of {category_display} trends, I've noticed some fascinating patterns emerging that deserve deeper reflection. 📈 Allow me to articulate my thoughts on where we're heading and what it means for professionals like us."

        draft_parts.append(hook)

        # Comprehensive content analysis with multiple perspectives
        detailed_summary = self._create_detailed_summary(content, keywords, themes)
        if detailed_summary:
            draft_parts.append(f"\n\n{detailed_summary}")

        # Personal professional insights with industry context
        if themes and keywords:
            insight_section = self._craft_insight_section(themes, keywords, category, sentiment)
            draft_parts.append(f"\n\n{insight_section}")

        # Forward-looking strategic perspective
        strategic_view = self._develop_strategic_view(category, sentiment, themes)
        draft_parts.append(f"\n\n{strategic_view}")

        # Thought-provoking engagement question
        engagement_question = self._create_engagement_question(category, sentiment)
        draft_parts.append(f"\n\n{engagement_question}")

        # Sophisticated CTA
        cta = self._select_sophisticated_cta(category)
        draft_parts.append(f"\n\n{cta}")

        # Curated hashtags
        hashtags = self._generate_curated_hashtags(category, keywords, themes)
        if hashtags:
            draft_parts.append(f"\n\n{' '.join(hashtags)}")

        # Combine and refine draft
        draft = ''.join(draft_parts)

        # Final polish and character limit enforcement
        draft = self._polish_draft(draft)

        logger.info(f"Generated exquisite opinion draft for {url}: {len(draft)} characters")

        return {
            'draft': draft,
            'hashtags': hashtags,
            'character_count': len(draft),
            'cta': cta,
            'category': category
        }

    def _create_detailed_summary(self, content, keywords, themes):
        """
        Create a comprehensive, context-rich summary that weaves in keywords and themes.
        :param content: Full content text.
        :param keywords: List of extracted keywords.
        :param themes: List of identified themes.
        :return: Detailed summary paragraph.
        """
        # Extract key sentences that contain important information
        sentences = re.split(r'[.!?]+', content.strip())
        key_sentences = []

        # Prioritize sentences containing keywords or themes
        for sentence in sentences[:5]:  # Look at first 5 sentences
            sentence_lower = sentence.lower()
            if any(kw.lower() in sentence_lower for kw in keywords[:3]) or \
               any(theme.lower() in sentence_lower for theme in themes[:2]):
                key_sentences.append(sentence.strip())

        # If no key sentences found, use the first substantial sentence
        if not key_sentences and sentences:
            key_sentences = [sentences[0].strip()]

        # Craft a flowing summary paragraph
        if key_sentences:
            summary_text = ' '.join(key_sentences[:2])  # Combine 1-2 key sentences
            # Add contextual bridge
            summary = f"Delving into the details, {summary_text.lower().rstrip('.')}. This development represents a significant shift in how we approach these challenges."
        else:
            summary = "The content explores critical developments that are reshaping our understanding of current industry dynamics."

        return summary

    def _craft_insight_section(self, themes, keywords, category, sentiment):
        """
        Craft a sophisticated insight section that connects themes, keywords, and professional perspective.
        :param themes: List of themes.
        :param keywords: List of keywords.
        :param category: Content category.
        :param sentiment: Sentiment analysis.
        :return: Insight paragraph.
        """
        primary_themes = themes[:3]
        key_terms = keywords[:4]

        # Create thematic connections
        if primary_themes:
            theme_connections = f"The interconnected themes of {', '.join(primary_themes)} particularly resonate with me. When we examine how {key_terms[0] if key_terms else 'these elements'} intersects with {primary_themes[0]}, we begin to see the broader implications for our field."
        else:
            theme_connections = f"The key concepts of {', '.join(key_terms[:3]) if key_terms else 'innovation and adaptation'} are particularly noteworthy in this context."

        # Add professional perspective based on sentiment
        if sentiment == 'positive':
            perspective = "What excites me most is how these developments create new opportunities for collaboration and growth across traditional boundaries."
        elif sentiment == 'negative':
            perspective = "This situation underscores the urgent need for strategic adaptation and proactive problem-solving within our industry."
        else:
            perspective = "These patterns suggest we're at an inflection point that demands careful consideration and strategic planning."

        return f"{theme_connections} {perspective}"

    def _develop_strategic_view(self, category, sentiment, themes):
        """
        Develop a forward-looking strategic perspective.
        :param category: Content category.
        :param sentiment: Sentiment analysis.
        :param themes: List of themes.
        :return: Strategic view paragraph.
        """
        category_display = category.replace('-', ' ')

        if sentiment == 'positive':
            strategic_view = f"Looking ahead, I believe these {category_display} advancements will fundamentally reshape our operational landscape. The question isn't whether change is coming—it's how we position ourselves to lead it."
        elif sentiment == 'negative':
            strategic_view = f"The challenges we're facing in {category_display} aren't insurmountable, but they do require a fundamental rethinking of our current approaches. Success will depend on our ability to innovate while maintaining stability."
        else:
            strategic_view = f"As we navigate these {category_display} developments, the key will be maintaining strategic flexibility while building on our core competencies. The organizations that thrive will be those that can adapt without losing their fundamental identity."

        return strategic_view

    def _create_engagement_question(self, category, sentiment):
        """
        Create a thought-provoking engagement question tailored to the content.
        :param category: Content category.
        :param sentiment: Sentiment analysis.
        :return: Engagement question.
        """
        category_display = category.replace('-', ' ')

        if sentiment == 'positive':
            questions = [
                f"How do you see these {category_display} innovations impacting your work?",
                f"What opportunities do you think these developments create for our industry?",
                f"How are you preparing your organization for these transformative changes?"
            ]
        elif sentiment == 'negative':
            questions = [
                f"What strategies are you employing to navigate these {category_display} challenges?",
                f"How is your organization adapting to these industry headwinds?",
                f"What lessons can we learn from these developments to strengthen our position?"
            ]
        else:
            questions = [
                f"Where do you see the {category_display} sector heading in the next 12-18 months?",
                f"How are these trends influencing your strategic planning?",
                f"What aspects of these developments are you most focused on right now?"
            ]

        return questions[hash(category + sentiment) % len(questions)]

    def _select_sophisticated_cta(self, category):
        """
        Select a sophisticated, contextually appropriate CTA.
        :param category: Content category.
        :return: Sophisticated CTA string.
        """
        sophisticated_ctas = [
            "I'd genuinely value your perspective on this. What are your thoughts?",
            "This is a conversation worth having—please share your insights below.",
            "Your experience in this area would be incredibly valuable. What's your take?",
            "Let's continue this important discussion. What's your professional viewpoint?",
            "I'm particularly interested in hearing from others in the field. What's your experience?"
        ]

        return sophisticated_ctas[hash(category) % len(sophisticated_ctas)]

    def _generate_curated_hashtags(self, category, keywords, themes):
        """
        Generate a curated set of hashtags that are relevant and professional.
        :param category: Content category.
        :param keywords: List of keywords.
        :param themes: List of themes.
        :return: Curated list of hashtags.
        """
        # Start with category-specific hashtags
        hashtags = self.category_hashtags.get(category, self.category_hashtags['general']).copy()

        # Add sophisticated keyword-based hashtags
        for kw in keywords[:2]:  # Limit to 2 for quality over quantity
            if len(kw) > 3:  # Avoid very short keywords
                hashtag = '#' + ''.join(word.capitalize() for word in kw.split() if len(word) > 2)
                if hashtag not in hashtags and len(hashtag) > 4:
                    hashtags.append(hashtag)

        # Add theme-based hashtags for depth
        for theme in themes[:1]:  # One theme hashtag
            theme_words = theme.split()[:2]  # Take first 2 words of theme
            if len(theme_words) > 1:
                hashtag = '#' + ''.join(word.capitalize() for word in theme_words)
                if hashtag not in hashtags:
                    hashtags.append(hashtag)

        return hashtags[:8]  # Limit to 8 for optimal engagement

    def _polish_draft(self, draft):
        """
        Final polish of the draft: ensure character limit, smooth transitions, professional tone.
        :param draft: Raw draft text.
        :return: Polished draft.
        """
        # Ensure character limit
        if len(draft) > self.max_chars:
            # Try to cut at a paragraph break if possible
            paragraphs = draft.split('\n\n')
            polished_draft = ""
            for para in paragraphs:
                if len(polished_draft + '\n\n' + para) > self.max_chars - 50:  # Leave room for "..."
                    break
                polished_draft += ('\n\n' if polished_draft else '') + para

            draft = polished_draft.rstrip() + "..."
        else:
            draft = draft.rstrip()

        # Final cleanup: ensure proper spacing
        draft = re.sub(r'\n{3,}', '\n\n', draft)  # Max 2 consecutive newlines
        draft = draft.strip()

        return draft

    def _generate_hashtags(self, category, keywords):
        """
        Generate relevant hashtags based on category and keywords.
        :param category: Content category.
        :param keywords: List of keywords.
        :return: List of hashtags.
        """
        hashtags = self.category_hashtags.get(category, self.category_hashtags['general']).copy()

        # Add keyword-based hashtags (capitalize and add #)
        for kw in keywords[:3]:  # Limit to 3
            hashtag = '#' + ''.join(word.capitalize() for word in kw.split())
            if hashtag not in hashtags:
                hashtags.append(hashtag)

        return hashtags[:10]  # Limit total hashtags

    def _select_cta(self, category):
        """
        Select an appropriate CTA based on category.
        :param category: Content category.
        :return: CTA string.
        """
        # For now, rotate through CTAs, but could customize per category
        return self.ctas[hash(category) % len(self.ctas)]

    def batch_generate(self, processed_content_list):
        """
        Generate drafts for a list of processed content.
        :param processed_content_list: List of processed content dicts.
        :return: List of draft dicts.
        """
        drafts = []
        for content in processed_content_list:
            try:
                draft = self.generate_draft(content)
                drafts.append(draft)
            except Exception as e:
                logger.error(f"Error generating draft for {content.get('url', 'unknown')}: {e}")
                drafts.append({'draft': 'Error generating draft', 'hashtags': [], 'character_count': 0, 'cta': '', 'category': content.get('category', 'general')})
        return drafts

# Example usage (for testing)
if __name__ == "__main__":
    generator = LinkedInDraftGenerator()
    sample_processed = {
        'title': 'Advances in Electric Vehicles',
        'content': 'New battery technology is revolutionizing the electric vehicle industry, promising longer ranges and faster charging times.',
        'keywords': ['battery', 'electric', 'vehicle', 'technology'],
        'themes': ['battery technology', 'electric vehicle industry'],
        'category': 'e-mobility',
        'sentiment': 'positive'
    }
    draft = generator.generate_draft(sample_processed)
    print("Draft:")
    print(draft['draft'])
    print(f"\nHashtags: {draft['hashtags']}")
    print(f"Character count: {draft['character_count']}")
