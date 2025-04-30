# PostPilot
# 🗓️ Social Media Scheduler (PostPilot)

This project is a simple, elegant, and interactive post scheduling desktop application built with Python and CustomTkinter. This tool allows users to schedule posts for different platforms, preview scheduled content (with optional images), and view a history of posted content — all in a scrollable, modern interface.
---

## 📁 Project Structure

```bash
.
├── core/
│   └── post.py        # Core logic for creating, validating, and saving posts
│   └── api_client.py
│   └── scheduler.py
│   └── logger.py  
├── data/
│   └── scheduled_posts.json  # Stores all scheduled posts as JSON (auto-created)
│   └── history.json 
├── media/
│   └── [uploaded_media]      # Stores media files copied during post creation
├── main.py           
└── README.md          # Project documentation
└── requirement.txt  
