"""
Quotes to Scrape - Data Science Practicum Web Scraper
Author: Practicum Student
Topic: Scraping quotes, authors, and tags from http://quotes.toscrape.com/
"""

import os
import json
import csv
import time
from urllib.parse import urljoin

try:
    import requests
    from bs4 import BeautifulSoup
    USE_BS4 = True
except ImportError:
    import urllib.request
    from html.parser import HTMLParser
    USE_BS4 = False

BASE_URL = "http://quotes.toscrape.com"
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def scrape_with_bs4(max_pages=10):
    quotes_data = []
    current_url = BASE_URL
    page_num = 1

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) QuotesPracticumScraper/1.0"
    }

    print(f"[*] Starting scraper using requests & BeautifulSoup...")

    while current_url and page_num <= max_pages:
        print(f" -> Scraping Page {page_num}: {current_url}")
        try:
            response = requests.get(current_url, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f" [!] Received status code {response.status_code}. Stopping.")
                break
        except Exception as e:
            print(f" [!] Error fetching {current_url}: {e}")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        quote_elements = soup.find_all("div", class_="quote")

        for elem in quote_elements:
            # Extract quote text
            text_elem = elem.find("span", class_="text")
            quote_text = text_elem.get_text(strip=True) if text_elem else ""
            if quote_text.startswith("“") and quote_text.endswith("”"):
                clean_text = quote_text[1:-1]
            elif quote_text.startswith('"') and quote_text.endswith('"'):
                clean_text = quote_text[1:-1]
            else:
                clean_text = quote_text

            # Extract author
            author_elem = elem.find("small", class_="author")
            author_name = author_elem.get_text(strip=True) if author_elem else "Unknown"

            # Extract author bio link
            author_link_elem = elem.find("a", href=True)
            author_url = urljoin(BASE_URL, author_link_elem["href"]) if author_link_elem else ""

            # Extract tags
            tag_elements = elem.find_all("a", class_="tag")
            tags = [t.get_text(strip=True) for t in tag_elements]

            quote_item = {
                "id": len(quotes_data) + 1,
                "quote": clean_text,
                "author": author_name,
                "author_url": author_url,
                "tags": tags,
                "tags_string": ", ".join(tags),
                "length": len(clean_text)
            }
            quotes_data.append(quote_item)

        # Check for next page
        next_button = soup.find("li", class_="next")
        if next_button and next_button.find("a"):
            next_href = next_button.find("a")["href"]
            current_url = urljoin(BASE_URL, next_href)
            page_num += 1
            time.sleep(0.2)  # Polite crawling delay
        else:
            current_url = None

    return quotes_data


def save_dataset(quotes_data):
    os.makedirs(DATA_DIR, exist_ok=True)
    json_path = os.path.join(DATA_DIR, "quotes.json")
    csv_path = os.path.join(DATA_DIR, "quotes.csv")

    # Save JSON
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(quotes_data, f, indent=2, ensure_ascii=False)
    print(f"[OK] Saved {len(quotes_data)} quotes to {json_path}")

    # Save CSV
    fieldnames = ["id", "quote", "author", "author_url", "tags_string", "length"]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for q in quotes_data:
            writer.writerow(q)
    print(f"[OK] Saved {len(quotes_data)} quotes to {csv_path}")


def analyze_dataset(quotes_data):
    total = len(quotes_data)
    authors = set(q["author"] for q in quotes_data)
    all_tags = []
    for q in quotes_data:
        all_tags.extend(q.get("tags", []))

    tag_counts = {}
    for tag in all_tags:
        tag_counts[tag] = tag_counts.get(tag, 0) + 1
    top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:5]

    author_counts = {}
    for q in quotes_data:
        author_counts[q["author"]] = author_counts.get(q["author"], 0) + 1
    top_authors = sorted(author_counts.items(), key=lambda x: x[1], reverse=True)[:5]

    print("\n" + "="*50)
    print("        QUOTES DATASET SUMMARY REPORT")
    print("="*50)
    print(f"Total Quotes Scraped : {total}")
    print(f"Unique Authors       : {len(authors)}")
    print(f"Unique Tags          : {len(tag_counts)}")
    print(f"Top 5 Authors        : {', '.join([f'{a} ({c})' for a, c in top_authors])}")
    print(f"Top 5 Tags           : {', '.join([f'{t} ({c})' for t, c in top_tags])}")
    print("="*50 + "\n")


def run_scraper(max_pages=10):
    quotes = scrape_with_bs4(max_pages=max_pages)
    if quotes:
        save_dataset(quotes)
        analyze_dataset(quotes)
    else:
        print("[!] No quotes scraped.")
    return quotes


if __name__ == "__main__":
    run_scraper()
