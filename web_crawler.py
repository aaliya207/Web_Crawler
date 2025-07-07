import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os

class WebCrawler:
    def __init__(self, base_url, save_content=False, max_pages=100, log_callback=None):
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.visited = set()
        self.save_content = save_content
        self.max_pages = max_pages
        self.count = 0
        self.log = log_callback or print

    def crawl(self, url):
        if url in self.visited or self.count >= self.max_pages:
            return
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            if response.status_code != 200 or 'text/html' not in response.headers.get('Content-Type', ''):
                return
        except Exception as e:
            self.log(f"[Error] {url} -> {e}")
            return

        self.visited.add(url)
        self.count += 1
        self.log(f"[{self.count}] Crawling: {url}")

        if self.save_content:
            self.save_page(url, response.text)

        soup = BeautifulSoup(response.text, "html.parser")
        for link_tag in soup.find_all("a", href=True):
            href = link_tag["href"]
            full_url = urljoin(url, href)
            if self.is_internal(full_url):
                self.crawl(full_url)

    def is_internal(self, url):
        return urlparse(url).netloc == self.domain

    def save_page(self, url, html):
        path = urlparse(url).path.strip("/")
        if not path:
            path = "index"
        filename = f"pages/{path.replace('/', '_')}.html"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)


class CrawlerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Web Crawler")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#02C9FF")

        # Style for rounded button
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Rounded.TButton",
                        padding=6,
                        relief="flat",
                        background="#ffffff",
                        foreground="#000000",
                        font=("Segoe UI", 10, "bold"))
        style.map("Rounded.TButton", background=[('active', '#e0e0e0')])

        # Custom label style
        style.configure("Custom.TLabel",
                        background="#02C9FF",
                        foreground="white",
                        font=("Segoe UI", 10, "bold"))

        # Custom checkbutton style
        style.configure("Custom.TCheckbutton",
                        background="#02C9FF",
                        foreground="white",
                        font=("Segoe UI", 10, "bold"))

        # URL Label
        ttk.Label(root, text="Enter URL:", style="Custom.TLabel").pack(pady=(15, 5))

        # URL Entry
        self.url_entry = ttk.Entry(root, width=72, font=("Segoe UI", 10))
        self.url_entry.pack(pady=5, ipady=4)

        # Save Page Checkbox
        self.save_var = tk.BooleanVar()
        ttk.Checkbutton(root, text="Save Page Content", variable=self.save_var,
                        style="Custom.TCheckbutton").pack(pady=5)

        # Start Button
        self.start_button = ttk.Button(root, text="Start Crawl", command=self.start_crawl, style="Rounded.TButton")
        self.start_button.pack(pady=10)

        # Log Label
        ttk.Label(root, text="Crawl Log:", style="Custom.TLabel").pack(pady=(10, 2))

        # Log Box
        self.log_box = scrolledtext.ScrolledText(root, height=17, width=72, font=("Consolas", 9))
        self.log_box.pack(padx=10, pady=5)

    def log(self, message):
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.see(tk.END)

    def start_crawl(self):
        url = self.url_entry.get().strip()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url

        self.log_box.delete(1.0, tk.END)
        self.log(f"🚀 Starting crawl for: {url}")
        self.start_button.config(state=tk.DISABLED)

        threading.Thread(target=self.run_crawler, args=(url,), daemon=True).start()

    def run_crawler(self, url):
        crawler = WebCrawler(url, save_content=self.save_var.get(), log_callback=self.log)
        crawler.crawl(url)
        self.log(f"\n✅ Done. Links crawled: {len(crawler.visited)}")
        self.start_button.config(state=tk.NORMAL)


if __name__ == "__main__":
    root = tk.Tk()
    app = CrawlerApp(root)
    root.mainloop()
