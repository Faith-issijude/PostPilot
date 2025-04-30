import customtkinter as ctk
from tkinter import messagebox, filedialog
from core.post import Post, SUPPORTED_PLATFORMS, save_post
from core.logger import HistoryLogger
from threading import Thread
from core.scheduler import Scheduler
from tkcalendar import Calendar
from datetime import datetime
from pathlib import Path
import time
import random
from dotenv import load_dotenv
import os
import json
from together import Together  # Add this import



# Load environment variables
load_dotenv()

class SchedulerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("📅 Social Media Scheduler")
        self.attributes('-fullscreen', True)
        self.bind("<Escape>", lambda e: self.attributes('-fullscreen', False))
        self.resizable(True, True)
    
        # Layout Frames
        self.sidebar_frame = ctk.CTkFrame(self, width=150)
        self.sidebar_frame.pack(side="left", fill="y")

        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Sidebar Navigation
        ctk.CTkLabel(self.sidebar_frame, text="Navigation", font=("Arial", 16, "bold")).pack(pady=10)

        self.schedule_btn = ctk.CTkButton(self.sidebar_frame, text="📝 Schedule Post", command=self.show_schedule_post)
        self.schedule_btn.pack(pady=10)

        self.view_scheduled_btn = ctk.CTkButton(self.sidebar_frame, text="📋 View Scheduled", command=self.show_scheduled_posts)
        self.view_scheduled_btn.pack(pady=10)

        self.view_history_btn = ctk.CTkButton(self.sidebar_frame, text="📚 Post History", command=self.show_post_history)
        self.view_history_btn.pack(pady=10)

        # Initialize Together client
        self.together_client = Together(api_key=os.getenv('TOGETHER_API_KEY'))

        # Default screen
        self.show_schedule_post()
        # Start the scheduler in a background thread
        # This will run the Scheduler class in a separate thread
        self.start_scheduler()
        
    def start_scheduler(self):
        """Run scheduler in a background thread"""
        
        def run_scheduler():
            scheduler = Scheduler()
            scheduler.run()
        # Start in daemon thread (will exit when main does)
        Thread(target= run_scheduler, daemon=True).start()
        print("🔹 Background scheduler started")

        
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_schedule_post(self):
        self.clear_content()

        ctk.CTkLabel(self.content_frame, text="📝 Schedule a New Post", font=("Arial", 18)).pack(pady=10)

        # Platform selection
        platform_label = ctk.CTkLabel(self.content_frame, text="Choose Platform:", font=("Arial", 14))
        platform_label.pack(pady=(10, 5))

        self.selected_platform = ctk.StringVar(value=SUPPORTED_PLATFORMS[0])
        self.platform_dropdown = ctk.CTkOptionMenu(self.content_frame, values=SUPPORTED_PLATFORMS, variable=self.selected_platform)
        self.platform_dropdown.pack(pady=5)

        # Post Content
        content_label = ctk.CTkLabel(self.content_frame, text="Post Content:", font=("Arial", 14))
        content_label.pack(pady=(10, 5))

        self.post_content_textbox = ctk.CTkTextbox(self.content_frame, height=100, width=500)
        self.post_content_textbox.pack(pady=5)
        

         #new code begins
         # AI Assistant Button (floating)
        self.ai_button = ctk.CTkButton(
            self.content_frame,
            text="✨ AI",
            width=30,
            height=30,
            command=self.activate_ai_assistant
        )
        self.ai_button.place_forget()  # Hide initially

        # Bind mouse entry to show AI button near cursor
        self.post_content_textbox.bind("<FocusIn>", self.show_ai_button)
        self.post_content_textbox.bind("<FocusOut>", self.hide_ai_button)
           #new code ends
           
            # Media Upload Section
        self.media_file_path = None

        self.upload_button = ctk.CTkButton(self.content_frame, text="📎 Upload Media", command=self.upload_media)
        self.upload_button.pack(pady=10)

        self.media_status_label = ctk.CTkLabel(self.content_frame, text="No media selected", font=("Arial", 12), text_color="gray")
        self.media_status_label.pack(pady=(0, 10))

        # Date & time input
        calendar_label = ctk.CTkLabel(self.content_frame, text="Pick a date:", font=("Arial", 14))
        calendar_label.pack(pady=(10, 5))

        self.post_date_picker = Calendar(self.content_frame, selectmode='day', date_pattern='yyyy-mm-dd')
        self.post_date_picker.pack(pady=5)

        time_label = ctk.CTkLabel(self.content_frame, text="Enter Time (HH:MM):", font=("Arial", 14))
        time_label.pack(pady=(10, 5))

        self.time_entry = ctk.CTkEntry(self.content_frame, width=200)
        self.time_entry.pack(pady=5)

        submit_button = ctk.CTkButton(self.content_frame, text="📤 Schedule Post", command=self.schedule_post)
        submit_button.pack(pady=20)

        # new function begins
    def show_ai_button(self, event):
        # Position button near cursor (top-right of textbox)
        x = self.post_content_textbox.winfo_x() + self.post_content_textbox.winfo_width() - 40
        y = self.post_content_textbox.winfo_y() - 30
        self.ai_button.place(x=x, y=y)

    def hide_ai_button(self, event):
        self.ai_button.place_forget()

    def activate_ai_assistant(self):
        # Create popup window
        popup = ctk.CTkToplevel(self)
        popup.title("AI Caption Assistant")
        popup.geometry("400x200")
        

        # Force popup to appear in front
        popup.attributes('-topmost', True)  # Critical fix
        popup.focus_force()

        # Prompt user
        ctk.CTkLabel(popup, text="please tell us what your post is about").pack(pady=10)
        self.ai_prompt_entry = ctk.CTkEntry(popup, width=300)
        self.ai_prompt_entry.pack(pady=5)
        
        # Generate button
        ctk.CTkButton(
            popup,
            text="Generate Caption",
            command=self.generate_ai_caption
        ).pack(pady=10)

    def generate_ai_caption(self):
        try: 
            user_input = self.ai_prompt_entry.get().strip()
            if not user_input:
                return
            
            # Use Together AI's native API
            response = self.together_client.chat.completions.create(
                model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",  # You can change this model
                messages=[
                   {
                    "role": "system", 
                    "content": "You're a vibrant, funny, and sweet social media AI assistant crafting ONE perfect caption. Rules:\n"
                              "1. Serve MAIN CHARACTER ENERGY 🎬✨\n"
                              "2. Must include:\n"
                              "   - 1 banger opening line\n"
                              "   - 1 sweet/funny follow-up\n"
                              "   - 3-5 🔥 emojis (mix of celebratory & thematic)\n"
                              "3. VIBES: Equal parts:\n"
                              "   - 🍭 Sweet\n"
                              "   - 😂 Self-aware humor\n"
                              "   - ✨ Sparkly confidence"
                },
                {
                    "role": "user",
                    "content": f"My post vibe: {user_input}\n"
                              "Hit me with that PERFECT caption energy!"
                }
                ],
                max_tokens=100,
                temperature=0.7,

            )
            
            caption = response.choices[0].message.content.strip()

        except Exception as e:
            print(f"Together AI Error: {e}")
            # Fallback remains the same
            mock_captions = [
                f"Enjoying {user_input}! 🌟",
                f"Just posted about {user_input}",
                f"Can't get enough of {user_input}!"
            ]
            caption = random.choice(mock_captions)
           
        # Insert into post content (unchanged)
        self.post_content_textbox.delete("1.0", "end")
        self.post_content_textbox.insert("1.0", caption)

        # Close the popup
        self.ai_prompt_entry.master.destroy()

    


    def upload_media(self):
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Media Files", "*.jpg *.jpeg *.png *.gif *.mp4 *.mov *.avi"),
                ("All Files", "*.*")
            ]
        )
        if file_path:
            self.media_file_path = file_path
            file_name = os.path.basename(file_path)
            self.media_status_label.configure(text=f"Selected: {file_name}")

    def show_scheduled_posts(self):
        self.clear_content()

        ctk.CTkLabel(self.content_frame, text="📋 Scheduled Posts", font=("Arial", 18)).pack(pady=10)

        file_path = Path("data/scheduled_posts.json")
        if not file_path.exists():
            ctk.CTkLabel(self.content_frame, text="No scheduled posts found.").pack(pady=20)
            return

        with open(file_path, 'r') as f:
            try:
                posts = json.load(f)
            except json.JSONDecodeError:
                posts = []

        if not posts:
            ctk.CTkLabel(self.content_frame, text="No scheduled posts found.").pack(pady=20)
            return

        
        # Scrollable Frame
        scrollable_frame = ctk.CTkScrollableFrame(self.content_frame, width=800, height=400)
        scrollable_frame.pack(pady=10)




        # Headers
        headers = ["S/N", "Platform", "Post", "Scheduled Time", "Media"]
        column_widths = [50, 100, 200, 150, 150] 

        for idx, (title, width) in enumerate(zip(headers, column_widths)):
            ctk.CTkLabel(scrollable_frame, text=title, font=("Arial", 14, "bold"), width=width).grid(row=0, column=idx, padx=10, pady=5)

            # Populate table
        for i, post in enumerate(posts, start=1):
            platform = post.get("platform", "N/A")
            content = post.get("content", "")
            schedule_time = post.get("schedule_time", "N/A")
            media = post.get("media_path", "")

            ctk.CTkLabel(scrollable_frame, text=str(i), width=50).grid(row=i, column=0, padx=10, pady=5)
            ctk.CTkLabel(scrollable_frame, text=platform, width=150).grid(row=i, column=1, padx=10, pady=5)
            ctk.CTkLabel(scrollable_frame, text=content, wraplength=200, width=200, anchor="center", justify="center").grid(row=i, column=2, padx=10, pady=5)
            ctk.CTkLabel(scrollable_frame, text=schedule_time, width=150).grid(row=i, column=3, padx=10, pady=5)

            # Adjust media column to column 4
            if media and media.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                try:
                    from PIL import Image, ImageTk
                    image = Image.open(media)
                    image.thumbnail((100, 100))
                    photo = ctk.CTkImage(light_image=image, size=image.size)
                    ctk.CTkLabel(scrollable_frame, image=photo, text="").grid(row=i, column=4, padx=10, pady=5)
                except Exception as e:
                    ctk.CTkLabel(scrollable_frame, text="Image Error").grid(row=i, column=4, padx=10, pady=5)
            else:
                ctk.CTkLabel(scrollable_frame, text="No Media").grid(row=i, column=4, padx=10, pady=5)
            
    
        # Create Post Button (bottom left)
        create_post_btn = ctk.CTkButton(self.content_frame, text="➕ Create New Post", command=self.show_schedule_post)
        create_post_btn.pack(pady=20, anchor="w", padx=40)

       
   
    def show_post_history(self):
        """Displays history with mock success indicators"""
        self.clear_content()
        
        # Header
        ctk.CTkLabel(self.content_frame, 
                    text="📚 Post History ", 
                    font=("Arial", 18)).pack(pady=10)
         
        # Load history using YOUR existing logger class
        logger = HistoryLogger()
        history = logger._load_history()
        
        # Display area
        scroll_frame = ctk.CTkScrollableFrame(self.content_frame, width=800, height=600)
        scroll_frame.pack(fill="both", expand=True)
        
        if not history:
            ctk.CTkLabel(scroll_frame, text="No posts yet!").pack()
            return
        
        for post in history:
            # post container
            # Green success frame for every entry
            post_frame = ctk.CTkFrame(scroll_frame, border_color="green", border_width=2)
            post_frame.pack(fill="x", pady=5, padx=10)
            
            # Header with platform and time
            header = f"✅ {post['platform']} • {post['timestamp']}"
            ctk.CTkLabel(post_frame, 
                        text=header, 
                        font=("Arial", 14, "bold")).pack(anchor="w")
            
            # Post content
            ctk.CTkLabel(post_frame, 
                        text=post["content"], 
                        wraplength=750).pack(anchor="w")
            
            
           
            # Mock engagement metrics
            engagement = post.get("engagement", {})
            metrics = f"👍 {engagement.get('likes', 0)} • 🔄 {engagement.get('shares', 0)} • 💬 {engagement.get('comments', 0)}"
            ctk.CTkLabel(post_frame, 
                        text=metrics, 
                        font=("Arial", 12)).pack(anchor="w")
            
    def schedule_post(self):
        platform = self.selected_platform.get()
        content = self.post_content_textbox.get("1.0", "end").strip()

        selected_date = self.post_date_picker.get_date()
        input_time = self.time_entry.get().strip()
        full_schedule_time = f"{selected_date} {input_time}"

        try:
            post = Post(platform, content, full_schedule_time, self.media_file_path)

            if not post.is_valid():
                messagebox.showerror("Error", "❌ Invalid post. Check content and date/time format.")
                return

            save_post(post)
            messagebox.showinfo("Success", "✅ Post scheduled successfully!")
            self.reset_post_form()
        except Exception as e:
            messagebox.showerror("Error", f"❌ Failed to schedule post: {str(e)}")
    def reset_post_form(self):
        self.selected_platform.set(SUPPORTED_PLATFORMS[0])
        self.post_content_textbox.delete("1.0", "end")
        self.media_file_path = None
        self.media_status_label.configure(text="No media selected")
        self.post_date_picker.selection_set(datetime.now().date())
        self.time_entry.delete(0, "end")

if __name__ == "__main__":
    app = SchedulerApp()
    app.mainloop()
