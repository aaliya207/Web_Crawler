# Simple Web Crawler GUI (Python)

A beginner-friendly web crawler with a basic graphical interface using `tkinter`. This tool is intended for educational or personal use and demonstrates how a crawler works internally without relying on external libraries beyond the essentials.

## Features

- 🖥️ GUI with `tkinter`
- 🌐 Crawl internal links within a given domain
- 💾 Option to save crawled page HTML content
- 📜 Scrollable log window to monitor crawl progress
- 🔒 Prevents over-crawling with a page limit (default: 100)

## Requirements

- Python 3.x
- Libraries:
  - `requests`
  - `beautifulsoup4`

You can install the required libraries using:

```bash
pip install requests beautifulsoup4
