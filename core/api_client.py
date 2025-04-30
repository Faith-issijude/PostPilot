# api_client.py

import random
import requests
from dotenv import load_dotenv
import os
import facebook as fb
from core.post import Post  # Assuming Post class is in core/post.py


class APIClient:
    def __init__(self):
        # In real implementation, this is where you'd load API tokens
        self.platforms = ["twitter", "facebook", "linkedin"]

        load_dotenv()  # Load environment variables from .env file
        self.FACEBOOK_API_KEY = os.getenv("FACEBOOK_API_KEY")


    
    def post(self, platform, content, media_url=None):
        """Post to the specified platform with content and optional media URL"""
        platform = platform.lower()
        if platform not in self.platforms:
            return {
                "success": False,
                "message": f"Unsupported platform: {platform}"
            }
        
        if platform == "facebook":
            # Call the real Facebook API method
            return self._post_to_facebook(content, media_url)
        

        # Simulate a delay or network call (optional)
        print(f"[API MOCK] Posting to {platform.title()}: {content}")

        # Simulated response (e.g., fake engagement metrics)
        response = {
            "success": True,
            "platform": platform,
            "content": content,
            "likes": random.randint(5, 200),
            "shares": random.randint(1, 50),
            "comments": random.randint(0, 20)
        }
        return response
    
    def _post_to_facebook(self, content, media_url=None):
        """Post to Facebook: handles both text and media (e.g., photo)"""
        try:
            if media_url:
                # 📸 If there's a media/photo URL, use the photo endpoint
                page_id = "640475215814950"
                url = f"https://graph.facebook.com/v19.0/{page_id}/photos"
                 # Open the file to be uploaded
                with open(media_url, "rb") as photo:
                    payload = {
                        "caption": content,  # Optional message with the image
                        "access_token": self.FACEBOOK_API_KEY
                    }
                    files = {
                        "source": photo  # Attach the image file for upload
                    }

                    response = requests.post(url, data=payload, files=files)
            else:
                # ✍️ Otherwise, it's a text post to the feed
                page_id = "640475215814950"
                url = f"https://graph.facebook.com/v19.0/{page_id}/feed"
                payload = {
                    "message": content,
                    "access_token": self.FACEBOOK_API_KEY
                }

            response = requests.post(url, data=payload)
            response_data = response.json()

            if response.status_code == 200:
                return {
                    "success": True,
                    "platform": "facebook",
                    "content": content,
                    "media": media_url,
                    "likes": random.randint(5, 200),
                    "shares": random.randint(1, 50),
                    "comments": random.randint(0, 20)
                }
            else:
                return {
                    "success": False,
                    "message": f"Failed to post on Facebook: {response_data.get('error', 'Unknown error')}"
                }

        except Exception as e:
            return {
                "success": False,
                "message": f"Exception posting to Facebook: {str(e)}"
            }
        
  