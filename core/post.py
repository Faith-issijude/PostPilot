# core/post.py

import json
from datetime import datetime
from pathlib import Path 

SUPPORTED_PLATFORMS = ['Twitter', 'Facebook', 'LinkedIn']
SCHEDULE_FILE = 'data/scheduled_posts.json'


class Post:
    def __init__(self, platform: str, content: str, schedule_time: str , media_path: str = ""):
        self.platform = platform.capitalize()
        self.content = content.strip()
        self.schedule_time = schedule_time  # Format: YYYY-MM-DD HH:MM
        self.media_path = media_path  
        
    def __repr__(self):
        return f"<Post platform={self.platform} time={self.schedule_time}>"

    def to_dict(self):
        return {
            "platform": self.platform,
            "content": self.content,
            "schedule_time": self.schedule_time,
            "media_path": self.media_path
        }
        # Added media_path to the dictionary representation

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            platform=data["platform"],
            content=data["content"],
            schedule_time=data["schedule_time"],
            media_path=data.get("media_path", "")  # Handle missing media_path gracefully
        )

    def is_due(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        return now == self.schedule_time

    def is_valid(self):
        try:
            datetime.strptime(self.schedule_time, "%Y-%m-%d %H:%M")
            return bool(self.content.strip()) and bool(self.platform)
        except ValueError:
            return False


def prompt_user_for_post():
    # Removed clear_console() for now
    print("📌 Schedule a New Post")
    print("Supported Platforms:")
    for idx, platform in enumerate(SUPPORTED_PLATFORMS, start=1):
        print(f"{idx}. {platform}")
    
    try:
        platform_choice = int(input("Select a platform (1-3): "))
        platform = SUPPORTED_PLATFORMS[platform_choice - 1]
    except (ValueError, IndexError):
        print("❌ Invalid choice.")
        return

    content = input("Enter the post content: ").strip()
    schedule_time = input("Enter scheduled time (YYYY-MM-DD HH:MM): ").strip()

    post = Post(platform, content, schedule_time)

    if not post.is_valid():
        print("❌ Invalid post. Please check the content and datetime format.")
        return

    save_post(post)
    print("✅ Post scheduled successfully!")


def save_post(post: Post):
    from shutil import copyfile
    from pathlib import Path
    import os

    Path('data').mkdir(parents=True, exist_ok=True)
    Path('media').mkdir(parents=True, exist_ok=True)  # NEW: Ensure media/ folder exists

    # Handle media saving (if any)
    if post.media_path and os.path.exists(post.media_path):
        # Copy the image to the media folder with a unique filename
        filename = os.path.basename(post.media_path)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        new_filename = f"{timestamp}_{filename}"
        new_media_path = os.path.join("media", new_filename)
        copyfile(post.media_path, new_media_path)

        # Update the post's media_path to the new location
        post.media_path = new_media_path

    # Load existing posts
    try:
        with open(SCHEDULE_FILE, 'r') as f:
            posts = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        posts = []

    # Save with the updated order: platform, content, schedule_time, media_path
    post_data = {
        "platform": post.platform,
        "content": post.content,
        "schedule_time": post.schedule_time,
        "media_path": post.media_path or ""   # always add media_path
    }

    posts.append(post_data)

    with open(SCHEDULE_FILE, 'w') as f:
        json.dump(posts, f, indent=4)
