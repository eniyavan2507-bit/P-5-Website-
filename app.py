"""
Quotes Explorer - Flask Web Application
Topic: Data Science Practicum P-5 (Website)
Dataset: Quotes to Scrape (http://quotes.toscrape.com/)
"""

import os
import json
import random
from flask import Flask, render_template, jsonify, request, send_file
from scraper import run_scraper, DATA_DIR

app = Flask(__name__)

JSON_PATH = os.path.join(DATA_DIR, "quotes.json")
CSV_PATH = os.path.join(DATA_DIR, "quotes.csv")


def load_quotes():
    """Load quotes from JSON file; scrape if missing."""
    if not os.path.exists(JSON_PATH):
        run_scraper()
    
    if os.path.exists(JSON_PATH):
        try:
            with open(JSON_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[!] Error loading JSON: {e}")
            return []
    return []


@app.route("/")
def index():
    """Render home page."""
    return render_template("index.html")


@app.route("/api/quotes")
def get_quotes():
    """API endpoint to get quotes with filtering, search, sorting, and pagination."""
    quotes = load_quotes()
    
    query = request.args.get("search", "").strip().lower()
    tag = request.args.get("tag", "").strip().lower()
    author = request.args.get("author", "").strip()
    sort_by = request.args.get("sort", "default")
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 12))

    filtered = quotes

    # Text search
    if query:
        filtered = [
            q for q in filtered
            if query in q["quote"].lower() or query in q["author"].lower() or any(query in t.lower() for t in q.get("tags", []))
        ]

    # Tag filter
    if tag:
        filtered = [
            q for q in filtered
            if any(t.lower() == tag for t in q.get("tags", []))
        ]

    # Author filter
    if author:
        filtered = [
            q for q in filtered
            if q["author"].lower() == author.lower()
        ]

    # Sorting
    if sort_by == "length_asc":
        filtered.sort(key=lambda x: x["length"])
    elif sort_by == "length_desc":
        filtered.sort(key=lambda x: x["length"], reverse=True)
    elif sort_by == "author":
        filtered.sort(key=lambda x: x["author"])

    total = len(filtered)
    start = (page - 1) * limit
    end = start + limit
    paginated = filtered[start:end]

    return jsonify({
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit if limit > 0 else 1,
        "quotes": paginated
    })


@app.route("/api/analytics")
def get_analytics():
    """Compute and return statistical insights for the quotes dataset."""
    quotes = load_quotes()
    if not quotes:
        return jsonify({"error": "No data available"}), 404

    total_quotes = len(quotes)
    authors = set(q["author"] for q in quotes)
    
    # Tag aggregation
    tag_counts = {}
    for q in quotes:
        for t in q.get("tags", []):
            tag_counts[t] = tag_counts.get(t, 0) + 1
    
    sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)

    # Author aggregation
    author_counts = {}
    for q in quotes:
        author_counts[q["author"]] = author_counts.get(q["author"], 0) + 1
    
    sorted_authors = sorted(author_counts.items(), key=lambda x: x[1], reverse=True)

    # Length distribution
    lengths = [q["length"] for q in quotes]
    avg_length = round(sum(lengths) / len(lengths), 1) if lengths else 0

    short_quotes = sum(1 for l in lengths if l < 80)
    medium_quotes = sum(1 for l in lengths if 80 <= l <= 160)
    long_quotes = sum(1 for l in lengths if l > 160)

    return jsonify({
        "total_quotes": total_quotes,
        "unique_authors": len(authors),
        "unique_tags": len(tag_counts),
        "avg_length": avg_length,
        "top_authors": [{"author": a, "count": c} for a, c in sorted_authors[:10]],
        "top_tags": [{"tag": t, "count": c} for t, c in sorted_tags[:12]],
        "all_authors": sorted(list(authors)),
        "all_tags": [t[0] for t in sorted_tags],
        "length_distribution": {
            "Short (<80 chars)": short_quotes,
            "Medium (80-160 chars)": medium_quotes,
            "Long (>160 chars)": long_quotes
        }
    })


@app.route("/api/random")
def get_random():
    """Fetch a single random quote."""
    quotes = load_quotes()
    if not quotes:
        return jsonify({"error": "No quotes found"}), 404
    return jsonify(random.choice(quotes))


@app.route("/api/scrape", methods=["POST"])
def trigger_scrape():
    """Trigger the scraper dynamically from the dashboard."""
    try:
        pages = int(request.json.get("pages", 10)) if request.is_json else 10
        quotes = run_scraper(max_pages=pages)
        return jsonify({"success": True, "count": len(quotes)})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/download/csv")
def download_csv():
    """Download quotes dataset in CSV format."""
    if not os.path.exists(CSV_PATH):
        run_scraper()
    return send_file(
        CSV_PATH,
        as_attachment=True,
        download_name="quotes_dataset.csv",
        mimetype="text/csv"
    )


@app.route("/download/json")
def download_json():
    """Download quotes dataset in JSON format."""
    if not os.path.exists(JSON_PATH):
        run_scraper()
    return send_file(
        JSON_PATH,
        as_attachment=True,
        download_name="quotes_dataset.json",
        mimetype="application/json"
    )


if __name__ == "__main__":
    print("[*] Starting Quotes to Scrape Web Application on http://127.0.0.1:5000 ...")
    app.run(debug=True, host="127.0.0.1", port=5000)
