# PostPilot
# 🗓️ Social Media Scheduler (PostPilot)

This project is a simple, elegant, and interactive post scheduling desktop application built with Python and CustomTkinter. This tool allows users to schedule posts for different platforms, preview scheduled content (with optional images), and view a history of posted content — all in a scrollable, modern interface.


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

## 📦 Features

- ✅ **Post Scheduling**: Choose platform, write content, set a date and time, and optionally attach media.
- 📋 **View Scheduled Posts**: Browse all upcoming posts in a scrollable table.
- 📚 **Post History**: View all previously posted content with mock engagement (likes, shares, comments).
- 🖼️ **Media Support**: Attach `.jpg`, `.jpeg`, `.png`, or `.gif` images to your posts.

---

## 🛠 Requirements

pip install -r requirements.txt

## 🚀 How to Run
---

1. Clone the repository or download the files.
2. Make sure you have all dependencies installed.
3. Run the app using:
python main.py


##✏️ How to Use
1. Click on "Create Post".
2. Select your platform (Facebook, Twitter, etc.).
3. Enter your content.
4. Pick a date and time.
5. (Optional) Attach media.
6. Click "Schedule Post" to save.
You can later:
See all scheduled posts via "Scheduled Posts".
Review past posts under "Post History".


##✨ Author
Developed with ❤️ by Faithfulness Issjude and Ahmad Ibrahim
