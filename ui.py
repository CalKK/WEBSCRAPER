import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess
import sys
import os
from queue_manager import QueueManager

class LinkedInScraperUI:
    """
    Simple minimalistic UI for interacting with the LinkedIn scraper.
    Features: Scrape button to run workflow, Drafts button to view and copy drafts.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("LinkedIn Scraper UI")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        # Center the window
        self.root.eval('tk::PlaceWindow . center')

        # Title
        title_label = tk.Label(root, text="LinkedIn Scraper", font=("Arial", 16, "bold"))
        title_label.pack(pady=20)

        # Scrape button
        scrape_btn = tk.Button(root, text="Scrape", command=self.run_scrape, 
                               font=("Arial", 12), bg="#4CAF50", fg="white", 
                               width=20, height=2)
        scrape_btn.pack(pady=10)

        # Drafts button
        drafts_btn = tk.Button(root, text="Drafts", command=self.show_drafts, 
                               font=("Arial", 12), bg="#2196F3", fg="white", 
                               width=20, height=2)
        drafts_btn.pack(pady=10)

        # Status label
        self.status_label = tk.Label(root, text="Ready", font=("Arial", 10))
        self.status_label.pack(pady=10)

        # Drafts text area (initially hidden)
        self.drafts_frame = tk.Frame(root)
        self.drafts_text = scrolledtext.ScrolledText(self.drafts_frame, wrap=tk.WORD, 
                                                     width=70, height=20, font=("Arial", 10))
        self.drafts_text.pack(pady=10)

        # Copy button (initially hidden)
        self.copy_btn = tk.Button(self.drafts_frame, text="Copy to Clipboard", 
                                  command=self.copy_draft, font=("Arial", 10), 
                                  bg="#FF9800", fg="white", width=15)
        self.copy_btn.pack(pady=5)

        # Quit button
        quit_btn = tk.Button(root, text="Quit", command=root.quit, 
                             font=("Arial", 10), bg="#f44336", fg="white", 
                             width=10, height=1)
        quit_btn.pack(pady=20)

    def run_scrape(self):
        """Run the scraping workflow using subprocess."""
        self.status_label.config(text="Scraping... Please wait.")
        self.root.update()

        try:
            # Run main.py with urls-file argument
            result = subprocess.run([sys.executable, "main.py", "--urls-file", "urls.txt"], 
                                  capture_output=True, text=True, cwd=os.getcwd())
            
            if result.returncode == 0:
                self.status_label.config(text="Scraping completed successfully!")
                messagebox.showinfo("Success", "Scraping completed! Check drafts.")
            else:
                error_msg = result.stderr or "Unknown error"
                self.status_label.config(text="Scraping failed.")
                messagebox.showerror("Error", f"Scraping failed:\n{error_msg}")
        except Exception as e:
            self.status_label.config(text="Scraping error.")
            messagebox.showerror("Error", f"Failed to run scrape:\n{str(e)}")

    def show_drafts(self):
        """Show drafts from queue in text area."""
        try:
            manager = QueueManager()
            queue_list = manager.list_queue(limit=10)  # Show up to 10 drafts

            if not queue_list:
                self.drafts_text.delete(1.0, tk.END)
                self.drafts_text.insert(tk.END, "No drafts in queue.")
                self.status_label.config(text="No drafts available.")
                return

            # Hide main buttons, show drafts frame
            self.drafts_frame.pack(pady=10, fill=tk.BOTH, expand=True)
            self.drafts_text.pack(pady=10)

            # Build drafts text
            drafts_content = "=== LINKEDIN DRAFTS ===\n\n"
            for i, draft_summary in enumerate(queue_list, 1):
                drafts_content += f"Draft {i} - Category: {draft_summary['category']}\n"
                drafts_content += f"Added: {draft_summary['added_at'][:10]}\n"
                drafts_content += f"Preview: {draft_summary['title_preview']}\n\n"

            # Get full next draft for copying
            next_draft = manager.peek_next_draft()
            if next_draft:
                drafts_content += "--- FULL NEXT DRAFT FOR COPYING ---\n\n"
                drafts_content += next_draft.get('draft', 'No draft content') + "\n\n"
                drafts_content += f"Hashtags: {' '.join(next_draft.get('hashtags', []))}\n"
                drafts_content += f"CTA: {next_draft.get('cta', '')}\n"

            self.drafts_text.delete(1.0, tk.END)
            self.drafts_text.insert(tk.END, drafts_content)
            self.copy_btn.pack(pady=5)
            self.status_label.config(text=f"Showing {len(queue_list)} drafts. Copy the full next draft.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load drafts:\n{str(e)}")
            self.status_label.config(text="Error loading drafts.")

    def copy_draft(self):
        """Copy the full next draft to clipboard."""
        try:
            manager = QueueManager()
            next_draft = manager.peek_next_draft()
            if next_draft:
                full_draft = next_draft.get('draft', '')
                hashtags = ' '.join(next_draft.get('hashtags', []))
                cta = next_draft.get('cta', '')
                
                clipboard_text = f"{full_draft}\n\n{hashtags}\n\n{cta}"
                
                self.root.clipboard_clear()
                self.root.clipboard_append(clipboard_text)
                self.root.update()  # Ensure clipboard is updated
                
                messagebox.showinfo("Copied", "Full draft copied to clipboard!")
                self.status_label.config(text="Draft copied to clipboard.")
            else:
                messagebox.showwarning("Warning", "No draft to copy.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy draft:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LinkedInScraperUI(root)
    root.mainloop()
