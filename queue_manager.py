import logging
import json
import os
from collections import deque
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QueueManager:
    """
    A simple queue management system for organizing LinkedIn post drafts.
    Uses deque for efficient FIFO operations and JSON for persistence.
    """

    def __init__(self, queue_file='drafts_queue.json'):
        """
        Initialize the queue manager.
        :param queue_file: Path to the JSON file for persisting the queue.
        """
        self.queue = deque()
        self.queue_file = queue_file
        self.load_queue()

    def add_draft(self, draft_dict):
        """
        Add a draft to the queue.
        :param draft_dict: Dict containing the draft details (from generator).
        """
        # Add timestamp and status
        draft_dict['added_at'] = datetime.now().isoformat()
        draft_dict['status'] = 'pending'
        self.queue.append(draft_dict)
        self.save_queue()
        logger.info(f"Added draft to queue: {draft_dict.get('category', 'unknown')} - {len(draft_dict['draft'])} chars")

    def get_next_draft(self):
        """
        Retrieve and remove the next draft from the queue (FIFO).
        :return: Draft dict or None if queue is empty.
        """
        if self.queue:
            draft = self.queue.popleft()
            draft['status'] = 'retrieved'
            self.save_queue()
            logger.info(f"Retrieved draft from queue: {draft.get('category', 'unknown')}")
            return draft
        else:
            logger.warning("Queue is empty")
            return None

    def peek_next_draft(self):
        """
        Peek at the next draft without removing it.
        :return: Draft dict or None if queue is empty.
        """
        if self.queue:
            return list(self.queue)[0]
        return None

    def queue_size(self):
        """
        Get the current size of the queue.
        :return: Integer size.
        """
        return len(self.queue)

    def list_queue(self, limit=5):
        """
        List the first N drafts in the queue.
        :param limit: Number of drafts to list.
        :return: List of draft summaries.
        """
        summaries = []
        for i, draft in enumerate(list(self.queue)[:limit]):
            summary = {
                'position': i + 1,
                'category': draft.get('category', 'unknown'),
                'title_preview': draft.get('draft', '')[:50] + '...',
                'added_at': draft.get('added_at', 'unknown'),
                'status': draft.get('status', 'unknown')
            }
            summaries.append(summary)
        return summaries

    def save_queue(self):
        """
        Save the queue to a JSON file for persistence.
        """
        try:
            with open(self.queue_file, 'w') as f:
                json.dump(list(self.queue), f, indent=2)
            logger.debug(f"Queue saved to {self.queue_file}")
        except Exception as e:
            logger.error(f"Error saving queue: {e}")

    def load_queue(self):
        """
        Load the queue from a JSON file.
        """
        if os.path.exists(self.queue_file):
            try:
                with open(self.queue_file, 'r') as f:
                    loaded_queue = json.load(f)
                    self.queue = deque(loaded_queue)
                logger.info(f"Loaded queue from {self.queue_file}: {len(self.queue)} items")
            except Exception as e:
                logger.error(f"Error loading queue: {e}")
                self.queue = deque()

    def clear_queue(self):
        """
        Clear all drafts from the queue.
        """
        self.queue.clear()
        self.save_queue()
        logger.info("Queue cleared")

    def batch_add_drafts(self, drafts_list):
        """
        Add multiple drafts to the queue.
        :param drafts_list: List of draft dicts.
        """
        for draft in drafts_list:
            self.add_draft(draft)

# Example usage (for testing)
if __name__ == "__main__":
    manager = QueueManager()
    sample_draft = {
        'draft': 'Sample LinkedIn post draft.',
        'hashtags': ['#Sample', '#Test'],
        'character_count': 25,
        'cta': 'What do you think?',
        'category': 'general'
    }
    manager.add_draft(sample_draft)
    print(f"Queue size: {manager.queue_size()}")
    next_draft = manager.get_next_draft()
    if next_draft:
        print("Next draft preview:", next_draft['draft'][:50])
    print("Queue summaries:", manager.list_queue())
