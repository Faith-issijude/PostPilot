# PostPilot
# 🗓️ Social Media Scheduler (PostPilot)

This project is a simple, elegant, and interactive post scheduling desktop application built with Python and CustomTkinter. This tool allows users to schedule posts for different platforms, preview scheduled content (with optional images), and view a history of posted content — all in a scrollable, modern interface.

## 📦 Features

- ✅ **Post Scheduling**: Choose platform, write content, set a date and time, and optionally attach media.
- 📋 **View Scheduled Posts**: Browse all upcoming posts in a scrollable table.
- 📚 **Post History**: View all previously posted content with mock engagement (likes, shares, comments).
- 🖼️ **Media Support**: Attach `.jpg`, `.jpeg`, `.png`, or `.gif` images to your posts.
- 🤖 **AI-Generated Captions**: Automatically generate creative post captions using AI with a single click.
---

🛠 Requirements
---
pip install -r requirements.txt



## 🚀 How to Run

To get started with the Post Scheduler application, follow the steps below:

---

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/postpilot.git
cd postpilot
```

---

### 2️⃣ Install Dependencies

Ensure you Install all required packages:

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install customtkinter pillow tkcalendar python-dotenv requests
```

---

### 3️⃣ Set Up Environment Variables

Create a `.env` file in the project root to securely store your API keys:

```env
FACEBOOK_API_KEY=""
TOGETHER_API_KEY=""
```

---

### 4️⃣ Facebook Graph API Setup

- Visit [https://developers.facebook.com](https://developers.facebook.com) and sign in.
- Create a developer app and **connect your Facebook Page**.
- Generate a **short-lived access token** for testing (valid for 1 hour).
- Add Required Permissions: When generating your access token, request these permissions:
pages_manage_cta
pages_show_list
pages_messaging
page_events
pages_read_engagement
pages_manage_metadata
pages_read_user_content
pages_manage_posts
pages_manage_engagement
![image](https://github.com/user-attachments/assets/c4ca4ecb-0f34-4f97-b888-8a7f6575d48f)

- Visit the **[Graph API Explorer](https://developers.facebook.com/tools/explorer/)**, paste your token, and submit.
- You'll see your **Page Name and Page ID** listed under the response.
  - **Copy your `Page ID`.** You will need this in the next step.
- Add your token to `.env` under `FACEBOOK_API_KEY`.

---

### 5️⃣ Update `page_id` in `api_client.py`

After copying your Page ID:

- Open `api_client.py`.
- Press `Ctrl + F` and search for `page_id`.
- Replace the default or placeholder value with **your actual Page ID** wherever it appears in the file.

This step ensures the app correctly connects and posts to your Facebook page.

---

### 6️⃣ Together AI Setup

- Go to [https://platform.together.xyz](https://platform.together.xyz) and create an account.
- Generate an API key under your account dashboard.
- Add this key to your `.env` file as:

```env
TOGETHER_API_KEY=your_generated_key_here
```

- The AI engine in this app uses the following model:
  
```python
model = "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8"
```

Make sure this model is used when sending requests to the Together API.

---

### 7️⃣ Launch the App

Once everything is set:

```bash
python main.py
```

✅ The GUI will open. You can now:
- Schedule posts
- Attach media
- View scheduled and posted content
- Simulate engagement data


✏️ How to Use
---
1. Click on "Create Post".
2.Select your platform (Facebook, Twitter, etc.).
3.Enter your content.
4.(Optional) Click the "AI ✨" button to generate a caption using AI.
5.Pick a date and time.
6.(Optional) Attach media.
7.Click "Schedule Post" to save.
You can later:
See all scheduled posts via "Scheduled Posts".
Review past posts under "Post History".


✨ Author
---
Developed with ❤️ by Faithfulness Issjude and Ahmad Ibrahim


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
