import tkinter as tk
from tkinter import ttk, messagebox
import threading
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.parse import urljoin


def fetch_page(url, retries=3):
    headers = {"User-Agent": "Mozilla/5.0"}

    for _ in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except:
            time.sleep(2)
    return None


def parse_hackernews(soup, base_url, keyword):
    items = soup.select('.titleline > a')
    return extract_items(items, base_url, keyword, "Hacker News")

def parse_bbc(soup, base_url, keyword):
    items = soup.select('h2 a')
    return extract_items(items, base_url, keyword, "BBC")

def parse_cnn(soup, base_url, keyword):
    items = soup.select('h3 a')
    return extract_items(items, base_url, keyword, "CNN")

def extract_items(items, base_url, keyword, source):
    articles = []
    for item in items:
        title = item.get_text(strip=True)
        link = urljoin(base_url, item.get('href'))

        if not title:
            continue

        if keyword and keyword.lower() not in title.lower():
            continue

        articles.append({
            "title": title,
            "link": link,
            "source": source
        })
    return articles

def parse_headlines(html, url, keyword):
    soup = BeautifulSoup(html, 'html.parser')

    if "ycombinator" in url:
        return parse_hackernews(soup, url, keyword)
    elif "bbc" in url:
        return parse_bbc(soup, url, keyword)
    elif "cnn" in url:
        return parse_cnn(soup, url, keyword)
    else:
        return []


def save_data(data, output):
    df = pd.DataFrame(data)
    df.to_csv(output + ".csv", index=False)
    df.to_json(output + ".json", orient="records", indent=4)


def run_scraper():
    url = url_entry.get()
    keyword = keyword_entry.get()
    output = output_entry.get()

    if not url:
        messagebox.showerror("Error", "Please enter a URL")
        return

    result_box.delete(1.0, tk.END)
    result_box.insert(tk.END, "Fetching...\n")

    html = fetch_page(url)
    if not html:
        result_box.insert(tk.END, "Failed to fetch page.\n")
        return

    time.sleep(1)

    data = parse_headlines(html, url, keyword)

    if not data:
        result_box.insert(tk.END, "No results found or unsupported site.\n")
        return

    save_data(data, output)

    result_box.insert(tk.END, f"\nScraped {len(data)} headlines:\n\n")

    for item in data[:10]:  
        result_box.insert(tk.END, f"• {item['title']}\n")

    result_box.insert(tk.END, f"\nSaved to {output}.csv & {output}.json\n")

def start_scraping():
    threading.Thread(target=run_scraper).start()


root = tk.Tk()
root.title("Multi-Site News Scraper")
root.geometry("700x500")


title_label = ttk.Label(root, text="News Scraper", font=("Arial", 18))
title_label.pack(pady=10)


url_entry = ttk.Entry(root, width=80)
url_entry.insert(0, "https://news.ycombinator.com")
url_entry.pack(pady=5)


keyword_entry = ttk.Entry(root, width=40)
keyword_entry.insert(0, "AI")
keyword_entry.pack(pady=5)


output_entry = ttk.Entry(root, width=40)
output_entry.insert(0, "output/news")
output_entry.pack(pady=5)


scrape_button = ttk.Button(root, text="Scrape Headlines", command=start_scraping)
scrape_button.pack(pady=10)


result_box = tk.Text(root, height=15)
result_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)


root.mainloop()