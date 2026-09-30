"""
Build a single self-contained standalone.html file with embedded data and styles.
Can be opened directly by double-clicking in any browser without running a server.
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "data", "quotes.json")
CSS_PATH = os.path.join(BASE_DIR, "static", "style.css")
STANDALONE_PATH = os.path.join(BASE_DIR, "standalone.html")

with open(JSON_PATH, "r", encoding="utf-8") as f:
    quotes_data = json.load(f)

with open(CSS_PATH, "r", encoding="utf-8") as f:
    css_content = f.read()

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quotes Explorer - Data Science Practicum</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Playfair+Display:ital,wght@0,600;0,700;1,600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
{css_content}
    </style>
</head>
<body>
    <header class="navbar">
        <div class="nav-container">
            <div class="brand">
                <i class="fa-solid fa-quote-left brand-icon"></i>
                <div class="brand-text">
                    <span class="brand-title">QuotesData<span class="accent">.io</span></span>
                    <span class="brand-subtitle">Data Science Practicum P-5</span>
                </div>
            </div>
            
            <nav class="nav-menu">
                <button class="nav-link active" data-tab="explorer"><i class="fa-solid fa-compass"></i> Quote Explorer</button>
                <button class="nav-link" data-tab="analytics"><i class="fa-solid fa-chart-pie"></i> Visualizations</button>
                <button class="nav-link" data-tab="dataset"><i class="fa-solid fa-database"></i> Dataset & Viva</button>
            </nav>

            <div class="nav-actions">
                <button id="random-btn" class="btn btn-outline" title="Inspire Me!">
                    <i class="fa-solid fa-dice"></i> Random Quote
                </button>
                <button id="download-csv-btn" class="btn btn-primary">
                    <i class="fa-solid fa-download"></i> Get CSV
                </button>
            </div>
        </div>
    </header>

    <main class="main-container">
        <section class="hero-section">
            <div class="hero-header">
                <h1>Web Scraped Quotes <span class="gradient-text">Data Science Explorer</span></h1>
                <p>Dataset mined from <a href="http://quotes.toscrape.com" target="_blank" rel="noopener">quotes.toscrape.com</a> using Python, BeautifulSoup & Requests.</p>
            </div>

            <div class="kpi-grid">
                <div class="kpi-card">
                    <div class="kpi-icon icon-blue"><i class="fa-solid fa-quote-right"></i></div>
                    <div class="kpi-info">
                        <span class="kpi-label">Total Quotes</span>
                        <h3 id="stat-total-quotes" class="kpi-value">--</h3>
                    </div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-icon icon-purple"><i class="fa-solid fa-feather"></i></div>
                    <div class="kpi-info">
                        <span class="kpi-label">Unique Authors</span>
                        <h3 id="stat-authors" class="kpi-value">--</h3>
                    </div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-icon icon-green"><i class="fa-solid fa-tags"></i></div>
                    <div class="kpi-info">
                        <span class="kpi-label">Unique Tags</span>
                        <h3 id="stat-tags" class="kpi-value">--</h3>
                    </div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-icon icon-orange"><i class="fa-solid fa-ruler-horizontal"></i></div>
                    <div class="kpi-info">
                        <span class="kpi-label">Avg Character Length</span>
                        <h3 id="stat-avg-length" class="kpi-value">--</h3>
                    </div>
                </div>
            </div>
        </section>

        <!-- TAB 1: QUOTE EXPLORER -->
        <section id="tab-explorer" class="tab-pane active">
            <div class="filter-card">
                <div class="search-row">
                    <div class="search-box">
                        <i class="fa-solid fa-magnifying-glass"></i>
                        <input type="text" id="search-input" placeholder="Search quotes by keyword, theme, or author...">
                        <button id="clear-search-btn" class="clear-btn" style="display:none;"><i class="fa-solid fa-xmark"></i></button>
                    </div>

                    <div class="filter-controls">
                        <div class="select-wrapper">
                            <i class="fa-solid fa-user-pen select-icon"></i>
                            <select id="author-select">
                                <option value="">All Authors</option>
                            </select>
                        </div>

                        <div class="select-wrapper">
                            <i class="fa-solid fa-arrow-down-short-wide select-icon"></i>
                            <select id="sort-select">
                                <option value="default">Default Order</option>
                                <option value="length_asc">Shortest First</option>
                                <option value="length_desc">Longest First</option>
                                <option value="author">Author (A-Z)</option>
                            </select>
                        </div>
                    </div>
                </div>

                <div class="tag-filters-container">
                    <span class="filter-label"><i class="fa-solid fa-fire"></i> Popular Topics:</span>
                    <div id="popular-tags-list" class="tag-chips">
                        <button class="tag-chip active" data-tag="">All</button>
                    </div>
                </div>
            </div>

            <div class="quotes-meta-bar">
                <span id="results-count">Showing quotes...</span>
            </div>

            <div id="quotes-grid" class="quotes-grid"></div>

            <div class="pagination-bar" id="pagination-controls">
                <button id="prev-page-btn" class="page-btn"><i class="fa-solid fa-chevron-left"></i> Previous</button>
                <span id="page-indicator" class="page-info">Page 1 of 1</span>
                <button id="next-page-btn" class="page-btn">Next <i class="fa-solid fa-chevron-right"></i></button>
            </div>
        </section>

        <!-- TAB 2: ANALYTICS -->
        <section id="tab-analytics" class="tab-pane">
            <div class="analytics-header">
                <h2>Data Science & Text Analysis Insights</h2>
                <p>Quantitative analysis and frequency distributions derived from the scraped quotes dataset.</p>
            </div>

            <div class="charts-grid">
                <div class="chart-card">
                    <div class="chart-header">
                        <h3><i class="fa-solid fa-trophy"></i> Top 10 Most Quoted Authors</h3>
                        <span class="badge">Author Frequency</span>
                    </div>
                    <div class="chart-wrapper">
                        <canvas id="authorsChart"></canvas>
                    </div>
                </div>

                <div class="chart-card">
                    <div class="chart-header">
                        <h3><i class="fa-solid fa-chart-pie"></i> Most Frequent Themes & Tags</h3>
                        <span class="badge">Topic Distribution</span>
                    </div>
                    <div class="chart-wrapper">
                        <canvas id="tagsChart"></canvas>
                    </div>
                </div>

                <div class="chart-card full-width">
                    <div class="chart-header">
                        <h3><i class="fa-solid fa-bars-staggered"></i> Quote Length Analysis (Character Distribution)</h3>
                        <span class="badge">Text Metrics</span>
                    </div>
                    <div class="chart-wrapper">
                        <canvas id="lengthChart"></canvas>
                    </div>
                </div>
            </div>
        </section>

        <!-- TAB 3: DATASET & VIVA -->
        <section id="tab-dataset" class="tab-pane">
            <div class="dataset-layout">
                <div class="dataset-actions-card">
                    <h3><i class="fa-solid fa-server"></i> Scraper Management & Export</h3>
                    <p>Scraped from <code>http://quotes.toscrape.com/</code> across 10 paginated web pages.</p>
                    
                    <div class="export-buttons-group">
                        <button id="btn-export-csv-tab" class="btn btn-outline-primary">
                            <i class="fa-solid fa-file-csv"></i> Download CSV Dataset
                        </button>
                        <button id="btn-export-json-tab" class="btn btn-outline-primary">
                            <i class="fa-solid fa-file-code"></i> Download JSON Dataset
                        </button>
                    </div>

                    <div class="schema-box">
                        <h4>Data Dictionary (Schema)</h4>
                        <ul>
                            <li><code>id</code> (Integer): Unique sequential identifier.</li>
                            <li><code>quote</code> (Text): Full textual content of the quote.</li>
                            <li><code>author</code> (String): Full name of the quote author.</li>
                            <li><code>author_url</code> (URL): Bio link extracted from page.</li>
                            <li><code>tags</code> (Array/String): Categorical classification tags.</li>
                            <li><code>length</code> (Integer): Character length of quote.</li>
                        </ul>
                    </div>
                </div>

                <div class="viva-card">
                    <h3><i class="fa-solid fa-graduation-cap"></i> Practicum Viva & Evaluation Notes</h3>
                    
                    <div class="faq-item">
                        <h4>Q1: What is Web Scraping and why is it used in Data Science?</h4>
                        <p>Web scraping is the automated extraction of unstructured or semi-structured data from websites and transforming it into clean, structured formats (like CSV or JSON) for data analysis, sentiment analysis, NLP, and machine learning models.</p>
                    </div>

                    <div class="faq-item">
                        <h4>Q2: What libraries were used in this project?</h4>
                        <p><code>requests</code>: Handles HTTP GET requests to fetch HTML documents.<br>
                        <code>BeautifulSoup</code>: Parses the HTML DOM tree using CSS selectors (<code>div.quote</code>, <code>span.text</code>, <code>small.author</code>, <code>a.tag</code>).<br>
                        <code>Flask</code>: Python web microframework providing REST API endpoints and dynamic routing.</p>
                    </div>

                    <div class="faq-item">
                        <h4>Q3: How is pagination handled in this scraper?</h4>
                        <p>The scraper detects the <code>&lt;li class="next"&gt;&lt;a&gt;</code> element on each page. If present, it resolves the relative URL with <code>urllib.parse.urljoin()</code> and iteratively crawls until no next link remains or maximum depth is reached.</p>
                    </div>

                    <div class="faq-item">
                        <h4>Q4: What are the ethical considerations of web scraping?</h4>
                        <p>Always inspect <code>robots.txt</code>, introduce politeness delays (<code>time.sleep()</code>) to avoid overloading web servers, provide identifiable <code>User-Agent</code> headers, and only scrape publicly accessible data without violating terms of service.</p>
                    </div>
                </div>
            </div>
        </section>
    </main>

    <div id="quote-modal" class="modal">
        <div class="modal-content">
            <button class="modal-close" id="modal-close-btn">&times;</button>
            <div class="modal-icon"><i class="fa-solid fa-quote-left"></i></div>
            <p id="modal-quote-text" class="modal-quote">"Loading..."</p>
            <p id="modal-quote-author" class="modal-author">— Author</p>
            <div id="modal-quote-tags" class="modal-tags"></div>
            <div class="modal-actions">
                <button id="modal-another-btn" class="btn btn-outline"><i class="fa-solid fa-shuffle"></i> Another One</button>
                <button id="modal-copy-btn" class="btn btn-primary"><i class="fa-solid fa-copy"></i> Copy Quote</button>
            </div>
        </div>
    </div>

    <div id="toast" class="toast">Quote copied to clipboard!</div>

    <script>
    const ALL_QUOTES = {json.dumps(quotes_data, ensure_ascii=False)};

    document.addEventListener("DOMContentLoaded", () => {{
        let state = {{
            currentPage: 1,
            currentTag: "",
            currentAuthor: "",
            currentSort: "default",
            searchQuery: "",
            charts: {{}}
        }};

        const quotesGrid = document.getElementById("quotes-grid");
        const searchInput = document.getElementById("search-input");
        const clearSearchBtn = document.getElementById("clear-search-btn");
        const authorSelect = document.getElementById("author-select");
        const sortSelect = document.getElementById("sort-select");
        const popularTagsList = document.getElementById("popular-tags-list");
        const resultsCount = document.getElementById("results-count");
        const prevPageBtn = document.getElementById("prev-page-btn");
        const nextPageBtn = document.getElementById("next-page-btn");
        const pageIndicator = document.getElementById("page-indicator");
        const toast = document.getElementById("toast");

        const quoteModal = document.getElementById("quote-modal");
        const randomBtn = document.getElementById("random-btn");
        const modalCloseBtn = document.getElementById("modal-close-btn");
        const modalQuoteText = document.getElementById("modal-quote-text");
        const modalQuoteAuthor = document.getElementById("modal-quote-author");
        const modalQuoteTags = document.getElementById("modal-quote-tags");
        const modalAnotherBtn = document.getElementById("modal-another-btn");
        const modalCopyBtn = document.getElementById("modal-copy-btn");

        // Tab Navigation
        const navLinks = document.querySelectorAll(".nav-link");
        const tabPanes = document.querySelectorAll(".tab-pane");

        navLinks.forEach(btn => {{
            btn.addEventListener("click", () => {{
                const targetTab = btn.getAttribute("data-tab");
                navLinks.forEach(l => l.classList.remove("active"));
                tabPanes.forEach(p => p.classList.remove("active"));

                btn.classList.add("active");
                const targetPane = document.getElementById(`tab-${{targetTab}}`);
                if (targetPane) {{
                    targetPane.classList.add("active");
                    if (targetTab === "analytics") {{
                        renderCharts();
                    }}
                }}
            }});
        }});

        computeAnalyticsAndKPIs();
        renderQuotes();
        setupEventListeners();

        function computeAnalyticsAndKPIs() {{
            const total = ALL_QUOTES.length;
            const authorsSet = new Set(ALL_QUOTES.map(q => q.author));
            const tagCounts = {{}};
            ALL_QUOTES.forEach(q => {{
                (q.tags || []).forEach(t => {{
                    tagCounts[t] = (tagCounts[t] || 0) + 1;
                }});
            }});

            const lengths = ALL_QUOTES.map(q => q.length);
            const avgLen = Math.round(lengths.reduce((a, b) => a + b, 0) / total);

            document.getElementById("stat-total-quotes").textContent = total;
            document.getElementById("stat-authors").textContent = authorsSet.size;
            document.getElementById("stat-tags").textContent = Object.keys(tagCounts).length;
            document.getElementById("stat-avg-length").textContent = `${{avgLen}} chars`;

            const sortedAuthors = Array.from(authorsSet).sort();
            sortedAuthors.forEach(a => {{
                const opt = document.createElement("option");
                opt.value = a;
                opt.textContent = a;
                authorSelect.appendChild(opt);
            }});

            const sortedTags = Object.entries(tagCounts).sort((a, b) => b[1] - a[1]);
            popularTagsList.innerHTML = '<button class="tag-chip active" data-tag="">All</button>';
            sortedTags.slice(0, 8).forEach(([tag, count]) => {{
                const chip = document.createElement("button");
                chip.className = "tag-chip";
                chip.dataset.tag = tag;
                chip.textContent = `#${{tag}} (${{count}})`;
                popularTagsList.appendChild(chip);
            }});
        }}

        function getFilteredQuotes() {{
            let filtered = [...ALL_QUOTES];
            const q = state.searchQuery.toLowerCase();
            if (q) {{
                filtered = filtered.filter(item => 
                    item.quote.toLowerCase().includes(q) ||
                    item.author.toLowerCase().includes(q) ||
                    (item.tags || []).some(t => t.toLowerCase().includes(q))
                );
            }}
            if (state.currentTag) {{
                filtered = filtered.filter(item => 
                    (item.tags || []).some(t => t.toLowerCase() === state.currentTag.toLowerCase())
                );
            }}
            if (state.currentAuthor) {{
                filtered = filtered.filter(item => 
                    item.author.toLowerCase() === state.currentAuthor.toLowerCase()
                );
            }}
            if (state.currentSort === "length_asc") {{
                filtered.sort((a, b) => a.length - b.length);
            }} else if (state.currentSort === "length_desc") {{
                filtered.sort((a, b) => b.length - a.length);
            }} else if (state.currentSort === "author") {{
                filtered.sort((a, b) => a.author.localeCompare(b.author));
            }}
            return filtered;
        }}

        function renderQuotes() {{
            const filtered = getFilteredQuotes();
            const total = filtered.length;
            const limit = 12;
            const totalPages = Math.max(1, Math.ceil(total / limit));
            if (state.currentPage > totalPages) state.currentPage = 1;

            const start = (state.currentPage - 1) * limit;
            const paginated = filtered.slice(start, start + limit);

            resultsCount.textContent = `Showing ${{total}} quote${{total === 1 ? '' : 's'}}`;
            pageIndicator.textContent = `Page ${{state.currentPage}} of ${{totalPages}}`;
            prevPageBtn.disabled = state.currentPage <= 1;
            nextPageBtn.disabled = state.currentPage >= totalPages;

            if (paginated.length === 0) {{
                quotesGrid.innerHTML = `
                    <div style="grid-column: 1 / -1; text-align: center; padding: 3.5rem; background: white; border-radius: 12px; border: 1px dashed #cbd5e1;">
                        <i class="fa-solid fa-magnifying-glass" style="font-size: 2.5rem; color: #94a3b8; margin-bottom: 1rem;"></i>
                        <h3 style="color: #334155; margin-bottom: 0.5rem;">No matching quotes found</h3>
                        <p style="color: #64748b; font-size: 0.95rem;">Try modifying your search or clearing filters.</p>
                    </div>
                `;
                return;
            }}

            quotesGrid.innerHTML = "";
            paginated.forEach(q => {{
                const card = document.createElement("div");
                card.className = "quote-card";
                const tagPills = (q.tags || []).map(t => 
                    `<span class="badge-tag" data-tag="${{t}}">#${{t}}</span>`
                ).join("");

                card.innerHTML = `
                    <div class="card-top">
                        <div class="quote-icon"><i class="fa-solid fa-quote-left"></i></div>
                        <p class="quote-text">“${{escapeHtml(q.quote)}}”</p>
                    </div>
                    <div class="card-bottom">
                        <div class="author-info">
                            <div class="author-name">
                                <i class="fa-solid fa-pen-nib" style="color: #6366f1; font-size: 0.8rem;"></i>
                                <span>${{escapeHtml(q.author)}}</span>
                            </div>
                            ${{q.author_url ? `<a href="${{escapeHtml(q.author_url)}}" target="_blank" rel="noopener" class="author-link"><i class="fa-solid fa-arrow-up-right-from-square"></i> Bio</a>` : ''}}
                        </div>
                        ${{tagPills ? `<div class="card-tags">${{tagPills}}</div>` : ''}}
                        <div class="card-actions">
                            <button class="card-action-btn copy-btn" data-quote="${{escapeHtml(q.quote)}}" data-author="${{escapeHtml(q.author)}}">
                                <i class="fa-regular fa-copy"></i> Copy
                            </button>
                        </div>
                    </div>
                `;
                quotesGrid.appendChild(card);
            }});

            quotesGrid.querySelectorAll(".badge-tag").forEach(tagElem => {{
                tagElem.addEventListener("click", () => selectTag(tagElem.dataset.tag));
            }});

            quotesGrid.querySelectorAll(".copy-btn").forEach(btn => {{
                btn.addEventListener("click", () => {{
                    copyToClipboard(`"${{btn.dataset.quote}}" — ${{btn.dataset.author}}`);
                }});
            }});
        }}

        function renderCharts() {{
            if (!window.Chart) return;
            const authorCounts = {{}};
            ALL_QUOTES.forEach(q => {{ authorCounts[q.author] = (authorCounts[q.author] || 0) + 1; }});
            const topAuthors = Object.entries(authorCounts).sort((a, b) => b[1] - a[1]).slice(0, 10);

            const ctxAuthors = document.getElementById("authorsChart");
            if (ctxAuthors) {{
                if (state.charts.authors) state.charts.authors.destroy();
                state.charts.authors = new Chart(ctxAuthors, {{
                    type: "bar",
                    data: {{
                        labels: topAuthors.map(a => a[0]),
                        datasets: [{{
                            data: topAuthors.map(a => a[1]),
                            backgroundColor: "rgba(99, 102, 241, 0.8)",
                            borderColor: "rgba(99, 102, 241, 1)",
                            borderRadius: 6,
                            borderWidth: 1
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        indexAxis: "y",
                        plugins: {{ legend: {{ display: false }} }},
                        scales: {{ x: {{ beginAtZero: true, ticks: {{ stepSize: 1 }} }} }}
                    }}
                }});
            }}

            const tagCounts = {{}};
            ALL_QUOTES.forEach(q => {{ (q.tags || []).forEach(t => {{ tagCounts[t] = (tagCounts[t] || 0) + 1; }}); }});
            const topTags = Object.entries(tagCounts).sort((a, b) => b[1] - a[1]).slice(0, 10);

            const ctxTags = document.getElementById("tagsChart");
            if (ctxTags) {{
                if (state.charts.tags) state.charts.tags.destroy();
                const palette = ["#6366f1", "#ec4899", "#8b5cf6", "#10b981", "#f59e0b", "#3b82f6", "#14b8a6", "#f43f5e", "#64748b", "#a855f7"];
                state.charts.tags = new Chart(ctxTags, {{
                    type: "doughnut",
                    data: {{
                        labels: topTags.map(t => `#${{t[0]}}`),
                        datasets: [{{
                            data: topTags.map(t => t[1]),
                            backgroundColor: palette.slice(0, topTags.length),
                            borderWidth: 2,
                            borderColor: "#ffffff"
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{ legend: {{ position: "right", labels: {{ boxWidth: 12, font: {{ size: 11 }} }} }} }}
                    }}
                }});
            }}

            const lengths = ALL_QUOTES.map(q => q.length);
            const shortQ = lengths.filter(l => l < 80).length;
            const medQ = lengths.filter(l => l >= 80 && l <= 160).length;
            const longQ = lengths.filter(l => l > 160).length;

            const ctxLen = document.getElementById("lengthChart");
            if (ctxLen) {{
                if (state.charts.length) state.charts.length.destroy();
                state.charts.length = new Chart(ctxLen, {{
                    type: "bar",
                    data: {{
                        labels: ["Short (<80 chars)", "Medium (80-160 chars)", "Long (>160 chars)"],
                        datasets: [{{
                            data: [shortQ, medQ, longQ],
                            backgroundColor: ["rgba(16, 185, 129, 0.75)", "rgba(59, 130, 246, 0.75)", "rgba(236, 72, 153, 0.75)"],
                            borderRadius: 8,
                            borderWidth: 1
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{ legend: {{ display: false }} }},
                        scales: {{ y: {{ beginAtZero: true, ticks: {{ stepSize: 5 }} }} }}
                    }}
                }});
            }}
        }}

        function setupEventListeners() {{
            let timer;
            searchInput.addEventListener("input", (e) => {{
                clearTimeout(timer);
                const val = e.target.value.trim();
                clearSearchBtn.style.display = val ? "block" : "none";
                timer = setTimeout(() => {{
                    state.searchQuery = val;
                    state.currentPage = 1;
                    renderQuotes();
                }}, 200);
            }});

            clearSearchBtn.addEventListener("click", () => {{
                searchInput.value = "";
                clearSearchBtn.style.display = "none";
                state.searchQuery = "";
                state.currentPage = 1;
                renderQuotes();
            }});

            authorSelect.addEventListener("change", (e) => {{
                state.currentAuthor = e.target.value;
                state.currentPage = 1;
                renderQuotes();
            }});

            sortSelect.addEventListener("change", (e) => {{
                state.currentSort = e.target.value;
                state.currentPage = 1;
                renderQuotes();
            }});

            popularTagsList.addEventListener("click", (e) => {{
                const chip = e.target.closest(".tag-chip");
                if (!chip) return;
                selectTag(chip.dataset.tag || "");
            }});

            prevPageBtn.addEventListener("click", () => {{
                if (state.currentPage > 1) {{
                    state.currentPage--;
                    renderQuotes();
                    window.scrollTo({{ top: 350, behavior: "smooth" }});
                }}
            }});

            nextPageBtn.addEventListener("click", () => {{
                state.currentPage++;
                renderQuotes();
                window.scrollTo({{ top: 350, behavior: "smooth" }});
            }});

            randomBtn.addEventListener("click", () => {{
                quoteModal.classList.add("show");
                showRandomModalQuote();
            }});

            modalCloseBtn.addEventListener("click", () => quoteModal.classList.remove("show"));
            window.addEventListener("click", (e) => {{ if (e.target === quoteModal) quoteModal.classList.remove("show"); }});
            modalAnotherBtn.addEventListener("click", showRandomModalQuote);
            modalCopyBtn.addEventListener("click", () => {{
                copyToClipboard(`${{modalQuoteText.textContent}} ${{modalQuoteAuthor.textContent}}`);
            }});

            function triggerDownload(content, filename, mimeType) {{
                const blob = new Blob([content], {{ type: mimeType }});
                const url = URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url;
                a.download = filename;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            }}

            function exportCSV() {{
                const header = ["id", "quote", "author", "author_url", "tags_string", "length"];
                const rows = ALL_QUOTES.map(q => [
                    q.id,
                    '"' + q.quote.replace(/"/g, '""') + '"',
                    '"' + q.author.replace(/"/g, '""') + '"',
                    q.author_url,
                    '"' + (q.tags_string || (q.tags || []).join(", ")) + '"',
                    q.length
                ]);
                const csvString = [header.join(","), ...rows.map(r => r.join(","))].join("\\n");
                triggerDownload(csvString, "quotes_dataset.csv", "text/csv;charset=utf-8;");
                showToast("CSV downloaded!");
            }}

            document.getElementById("download-csv-btn").addEventListener("click", exportCSV);
            const tabCsvBtn = document.getElementById("btn-export-csv-tab");
            if (tabCsvBtn) tabCsvBtn.addEventListener("click", exportCSV);

            const tabJsonBtn = document.getElementById("btn-export-json-tab");
            if (tabJsonBtn) tabJsonBtn.addEventListener("click", () => {{
                triggerDownload(JSON.stringify(ALL_QUOTES, null, 2), "quotes_dataset.json", "application/json");
                showToast("JSON downloaded!");
            }});
        }}

        function showRandomModalQuote() {{
            const randomQuote = ALL_QUOTES[Math.floor(Math.random() * ALL_QUOTES.length)];
            modalQuoteText.textContent = `“${{randomQuote.quote}}”`;
            modalQuoteAuthor.textContent = `— ${{randomQuote.author}}`;
            modalQuoteTags.innerHTML = (randomQuote.tags || []).map(t => `<span class="badge-tag">#${{t}}</span>`).join("");
        }}

        function selectTag(tag) {{
            state.currentTag = tag;
            state.currentPage = 1;
            popularTagsList.querySelectorAll(".tag-chip").forEach(c => {{
                if (c.dataset.tag === tag) c.classList.add("active");
                else c.classList.remove("active");
            }});
            renderQuotes();
        }}

        function copyToClipboard(text) {{
            navigator.clipboard.writeText(text).then(() => showToast("Quote copied to clipboard!"));
        }}

        function showToast(msg) {{
            toast.textContent = msg;
            toast.classList.add("show");
            setTimeout(() => toast.classList.remove("show"), 2500);
        }}

        function escapeHtml(str) {{
            if (!str) return "";
            return str
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;")
                .replace(/'/g, "&#039;");
        }}
    }});
    </script>
</body>
</html>
"""

with open(STANDALONE_PATH, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"[OK] Successfully built {STANDALONE_PATH} ({len(html_content)} bytes)")
