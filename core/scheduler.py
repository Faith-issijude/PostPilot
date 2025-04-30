# core/scheduler.py
import time
from datetime import datetime
import json
from core.api_client import APIClient
from core.logger import HistoryLogger

class Scheduler:
    def __init__(self, schedule_file='data/scheduled_posts.json'):
        self.schedule_file = schedule_file
        self.api_client = APIClient()  # Your API client
        self.logger = HistoryLogger()  # History logger
        
    def load_scheduled_posts(self):
        """Load posts from JSON file"""
        try:
            with open(self.schedule_file, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []  # Return empty list if file doesn't exist/corrupt

    def save_updated_schedule(self, posts):
        """Save updated schedule after posting"""
        with open(self.schedule_file, 'w') as file:
            json.dump(posts, file, indent=4)

    def check_and_post(self):
        """Main posting logic - MOCK VERSION"""
        scheduled_posts = self.load_scheduled_posts()
        now = datetime.now().strftime("%Y-%m-%d %H:%M") # Must match your Post time format
        print(f"⏰ Current Scheduler Time: {now}")  # Debug line
    
        updated_schedule = []

        for post in scheduled_posts:
            print(f"🕒 Checking post scheduled for: {post['schedule_time']}")  # Debug
            if post["schedule_time"] == now:
                print("🎯 Time matched! Attempting to post...")  # Debug
                
                # Check if media_path is available, if so, pass it as media_url
                media_url = post.get("media_path")  # Get the media path if exists
            
                # MOCK POSTING - Pass media_url when posting
                response = self.api_client.post(post["platform"], post["content"], media_url=media_url)
            
                # MOCK POSTING - Always succeeds
                # response = self.api_client.post(post["platform"], post["content"])
                
                # Log successful post
                self.logger.log({
                    "post": post,
                    "status": "success",
                    "response": response,
                    "timestamp": now
                })
                
                print(f"✅ Posted to {post['platform']}: {post['content'][:30]}...")
            else:
                updated_schedule.append(post)  # Keep unscheduled posts

        self.save_updated_schedule(updated_schedule)

    def run(self):
        """Main scheduler loop"""
        print("⏰ Scheduler running (mock mode)...")
        while True:
            self.check_and_post()
            time.sleep(60)  # Check every minute