# core/logger.py
import json
from datetime import datetime

class HistoryLogger:
    """Handles saving and viewing post history."""
    
    def __init__(self, file_path="data/post_history.json"):
        self.file_path = file_path

    def log(self, data):
        """
        Save a posted item to history with engagement data.
        Now accepts 'data' dict containing post and response.
        """
        try:
            history = self._load_history()
            history.append({
                "platform": data["post"]["platform"],
                "content": data["post"]["content"],
                "timestamp": data["post"]["schedule_time"],
                "engagement": data.get("response", {})
            })
            self._save_history(history)
        except Exception as e:
            print(f"Error logging post: {e}")

        
    def view_history(self, platform=None, date=None):
        """Display posts filtered by platform or date."""
        history = self._load_history()
        
        # Filter logic
        if platform:
            history = [p for p in history if p["platform"].lower() == platform.lower()]
        if date:
            history = [p for p in history if datetime.fromisoformat(p["timestamp"]).date() == date]
        
        # Display results
        if not history:
            print("No posts found.")
            return
        
        for idx, post in enumerate(history, 1):
            print(f"\n[{idx}] {post['platform'].upper()} Post")
            print(f"Time: {datetime.fromisoformat(post['timestamp']).strftime('%Y-%m-%d %H:%M')}")
            print(f"Content: {post['content']}")
            print("Engagement:", post.get("engagement", "No data"))

    # Helper methods
    def _load_history(self):
        """Load history from JSON file."""
        try:
            with open(self.file_path, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []  # Return empty list if file doesn't exist or is invalid

    def _save_history(self, data):
        """Save history to JSON file."""
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=2)
