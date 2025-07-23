import tkinter as tk
from tkinter import messagebox
from modules.youtube_scraper import scrape_youtube_comments
from modules.insta_scraper import scrape_instagram_comments

def start_scraping():
    url = url_entry.get().strip()
    if not url:
        messagebox.showerror("Error", "Please enter a URL.")
        return

    try:
        if "youtube.com" in url or "youtu.be" in url:
            scrape_youtube_comments(url)
            messagebox.showinfo("Success", "YouTube comments scraped successfully!")
        elif "instagram.com" in url:
            scrape_instagram_comments(url)
            messagebox.showinfo("Success", "Instagram comments scraped successfully!")
        else:
            messagebox.showerror("Error", "Invalid or unsupported URL.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI setup
root = tk.Tk()
root.title("Comment Scraper - YouTube & Instagram")
root.geometry("500x180")
root.resizable(False, False)

tk.Label(root, text="Paste YouTube or Instagram post URL:", font=("Arial", 12)).pack(pady=10)
url_entry = tk.Entry(root, width=60)
url_entry.pack(pady=5)
tk.Button(root, text="Scrape Comments", command=start_scraping, bg="blue", fg="white", font=("Arial", 11)).pack(pady=10)

root.mainloop()
