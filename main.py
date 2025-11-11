import logging
import argparse
import sys
from scraper import WebScraper
from processor import ContentProcessor
from generator import LinkedInDraftGenerator
from queue_manager import QueueManager

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LinkedInScraperApp:
    """
    Main application class to orchestrate the LinkedIn scraper workflow.
    """

    def __init__(self):
        self.scraper = WebScraper()
        self.processor = ContentProcessor()
        self.generator = LinkedInDraftGenerator()
        self.queue_manager = QueueManager()

    def run_workflow(self, urls):
        """
        Run the complete workflow: scrape, process, generate, queue.
        :param urls: List of URLs to process.
        """
        logger.info(f"Starting workflow for {len(urls)} URLs")

        # Step 1: Scrape content
        scraped_content = self.scraper.scrape_multiple_urls(urls)
        if not scraped_content:
            logger.error("No content scraped. Exiting.")
            return

        # Categorize scraped content
        categorized_content = [self.scraper.categorize_content(content) for content in scraped_content]
        logger.info(f"Scraped and categorized {len(categorized_content)} content items")

        # Step 2: Process content
        processed_content = self.processor.batch_process(categorized_content)
        logger.info(f"Processed {len(processed_content)} content items")

        # Step 3: Generate drafts
        drafts = self.generator.batch_generate(processed_content)
        logger.info(f"Generated {len(drafts)} LinkedIn drafts")

        # Step 4: Add to queue
        self.queue_manager.batch_add_drafts(drafts)
        logger.info(f"Added {len(drafts)} drafts to queue")

        # Print summary
        self.print_summary(processed_content, drafts)

    def print_summary(self, processed_content, drafts):
        """
        Print a summary of the workflow results.
        """
        print("\n" + "="*50)
        print("WORKFLOW SUMMARY")
        print("="*50)
        print(f"Total URLs processed: {len(processed_content)}")
        print(f"Drafts generated: {len(drafts)}")
        print(f"Queue size: {self.queue_manager.queue_size()}")

        # Category distribution
        categories = {}
        for content in processed_content:
            cat = content.get('category', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1
        print("\nContent by category:")
        for cat, count in categories.items():
            print(f"  {cat}: {count}")

        print("\nNext draft in queue:")
        next_draft = self.queue_manager.peek_next_draft()
        if next_draft:
            print(f"  Category: {next_draft.get('category', 'unknown')}")
            print(f"  Preview: {next_draft['draft'][:100]}...")
        else:
            print("  No drafts in queue")

    def manage_queue(self, action, limit=5):
        """
        Manage the queue: list, get next, clear.
        :param action: 'list', 'get', 'clear'
        :param limit: For list action, number of items to show.
        """
        if action == 'list':
            queue_list = self.queue_manager.list_queue(limit)
            print(f"\nQueue contents (first {limit} items):")
            for item in queue_list:
                print(f"  {item['position']}. {item['category']} - {item['title_preview']} ({item['added_at']})")
        elif action == 'get':
            draft = self.queue_manager.get_next_draft()
            if draft:
                print("\nRetrieved draft:")
                print(f"Category: {draft.get('category', 'unknown')}")
                print(f"Character count: {draft.get('character_count', 0)}")
                print(f"CTA: {draft.get('cta', '')}")
                print(f"Hashtags: {draft.get('hashtags', [])}")
                print(f"Draft:\n{draft['draft']}")
            else:
                print("No drafts in queue.")
        elif action == 'clear':
            confirm = input("Are you sure you want to clear the queue? (y/N): ")
            if confirm.lower() == 'y':
                self.queue_manager.clear_queue()
                print("Queue cleared.")
            else:
                print("Queue not cleared.")
        else:
            print("Invalid action. Use 'list', 'get', or 'clear'.")

def main():
    parser = argparse.ArgumentParser(description="LinkedIn Scraper and Draft Generator")
    parser.add_argument('--urls', nargs='+', help='List of URLs to scrape')
    parser.add_argument('--urls-file', type=str, help='Path to file containing URLs (one per line)')
    parser.add_argument('--queue', choices=['list', 'get', 'clear'], help='Queue management action')
    parser.add_argument('--limit', type=int, default=5, help='Limit for queue list (default: 5)')

    args = parser.parse_args()

    app = LinkedInScraperApp()

    if args.urls:
        app.run_workflow(args.urls)
    elif args.urls_file:
        try:
            with open(args.urls_file, 'r') as f:
                urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            if urls:
                app.run_workflow(urls)
            else:
                print("No valid URLs found in file.")
        except FileNotFoundError:
            print(f"URLs file '{args.urls_file}' not found.")
        except Exception as e:
            print(f"Error reading URLs file: {e}")
    elif args.queue:
        app.manage_queue(args.queue, args.limit)
    else:
        print("Usage:")
        print("  python main.py --urls <url1> <url2> ...     # Run workflow with URLs")
        print("  python main.py --urls-file urls.txt          # Run workflow with URLs from file")
        print("  python main.py --queue list                  # List queue")
        print("  python main.py --queue get                   # Get next draft")
        print("  python main.py --queue clear                 # Clear queue")
        print("\nExample:")
        print("  python main.py --urls-file urls.txt")

if __name__ == "__main__":
    main()
