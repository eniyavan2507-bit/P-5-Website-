/**
 * Quotes Explorer - Frontend Application Script
 * Data Science Practicum P-5
 */

document.addEventListener("DOMContentLoaded", () => {
    // State management
    let state = {
        currentPage: 1,
        currentTag: "",
        currentAuthor: "",
        currentSort: "default",
        searchQuery: "",
        analyticsData: null,
        charts: {}
    };

    // DOM Elements
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

    // Modal Elements
    const quoteModal = document.getElementById("quote-modal");
    const randomBtn = document.getElementById("random-btn");
    const modalCloseBtn = document.getElementById("modal-close-btn");
    const modalQuoteText = document.getElementById("modal-quote-text");
    const modalQuoteAuthor = document.getElementById("modal-quote-author");
    const modalQuoteTags = document.getElementById("modal-quote-tags");
    const modalAnotherBtn = document.getElementById("modal-another-btn");
    const modalCopyBtn = document.getElementById("modal-copy-btn");

    // Scraper Elements
    const runScraperBtn = document.getElementById("run-scraper-btn");
    const scrapeStatus = document.getElementById("scrape-status");

    // Tab Navigation
    const navLinks = document.querySelectorAll(".nav-link");
    const tabPanes = document.querySelectorAll(".tab-pane");

    navLinks.forEach(btn => {
        btn.addEventListener("click", () => {
            const targetTab = btn.getAttribute("data-tab");
            navLinks.forEach(l => l.classList.remove("active"));
            tabPanes.forEach(p => p.classList.remove("active"));

            btn.classList.add("active");
            const targetPane = document.getElementById(`tab-${targetTab}`);
            if (targetPane) {
                targetPane.classList.add("active");
                if (targetTab === "analytics" && state.analyticsData) {
                    renderCharts(state.analyticsData);
                }
            }
        });
    });

    // Initialize application
    init();

    async function init() {
        await loadAnalytics();
        loadQuotes();
        setupEventListeners();
    }

    // -------------------------------------------------------------
    // Fetch and Load Analytics & KPIs
    // -------------------------------------------------------------
    async function loadAnalytics() {
        try {
            const res = await fetch("/api/analytics");
            if (!res.ok) throw new Error("Failed to load analytics");
            const data = await res.json();
            state.analyticsData = data;

            // Populate KPIs
            document.getElementById("stat-total-quotes").textContent = data.total_quotes || 0;
            document.getElementById("stat-authors").textContent = data.unique_authors || 0;
            document.getElementById("stat-tags").textContent = data.unique_tags || 0;
            document.getElementById("stat-avg-length").textContent = `${data.avg_length || 0} chars`;

            // Populate Authors Dropdown
            authorSelect.innerHTML = '<option value="">All Authors</option>';
            if (data.all_authors) {
                data.all_authors.forEach(auth => {
                    const opt = document.createElement("option");
                    opt.value = auth;
                    opt.textContent = auth;
                    authorSelect.appendChild(opt);
                });
            }

            // Populate Popular Tag Chips
            if (data.top_tags) {
                popularTagsList.innerHTML = '<button class="tag-chip active" data-tag="">All</button>';
                data.top_tags.slice(0, 8).forEach(item => {
                    const chip = document.createElement("button");
                    chip.className = "tag-chip";
                    chip.dataset.tag = item.tag;
                    chip.textContent = `#${item.tag} (${item.count})`;
                    popularTagsList.appendChild(chip);
                });
            }
        } catch (err) {
            console.error("Error loading analytics:", err);
        }
    }

    // -------------------------------------------------------------
    // Fetch and Render Quotes
    // -------------------------------------------------------------
    async function loadQuotes() {
        quotesGrid.innerHTML = `
            <div class="loading-state" style="grid-column: 1 / -1; text-align: center; padding: 3rem; color: #64748b;">
                <i class="fa-solid fa-spinner fa-spin" style="font-size: 2rem; margin-bottom: 0.5rem;"></i>
                <p>Loading quotes...</p>
            </div>
        `;

        try {
            const params = new URLSearchParams({
                search: state.searchQuery,
                tag: state.currentTag,
                author: state.currentAuthor,
                sort: state.currentSort,
                page: state.currentPage,
                limit: 12
            });

            const res = await fetch(`/api/quotes?${params.toString()}`);
            if (!res.ok) throw new Error("Failed to fetch quotes");
            const data = await res.json();

            renderQuotes(data.quotes);
            updatePagination(data.total, data.page, data.total_pages);
        } catch (err) {
            console.error("Error loading quotes:", err);
            quotesGrid.innerHTML = `
                <div style="grid-column: 1 / -1; text-align: center; padding: 2rem; color: #ef4444;">
                    <i class="fa-solid fa-triangle-exclamation" style="font-size: 2rem; margin-bottom: 0.5rem;"></i>
                    <p>Failed to load quotes. Please try refreshing.</p>
                </div>
            `;
        }
    }

    function renderQuotes(quotes) {
        if (!quotes || quotes.length === 0) {
            quotesGrid.innerHTML = `
                <div style="grid-column: 1 / -1; text-align: center; padding: 3.5rem; background: white; border-radius: 12px; border: 1px dashed #cbd5e1;">
                    <i class="fa-solid fa-magnifying-glass" style="font-size: 2.5rem; color: #94a3b8; margin-bottom: 1rem;"></i>
                    <h3 style="color: #334155; margin-bottom: 0.5rem;">No matching quotes found</h3>
                    <p style="color: #64748b; font-size: 0.95rem;">Try modifying your search query or removing active filters.</p>
                </div>
            `;
            return;
        }

        quotesGrid.innerHTML = "";
        quotes.forEach(q => {
            const card = document.createElement("div");
            card.className = "quote-card";

            const tagPills = (q.tags || []).map(t => 
                `<span class="badge-tag" data-tag="${escapeHtml(t)}">#${escapeHtml(t)}</span>`
            ).join("");

            card.innerHTML = `
                <div class="card-top">
                    <div class="quote-icon"><i class="fa-solid fa-quote-left"></i></div>
                    <p class="quote-text">“${escapeHtml(q.quote)}”</p>
                </div>
                <div class="card-bottom">
                    <div class="author-info">
                        <div class="author-name">
                            <i class="fa-solid fa-pen-nib" style="color: #6366f1; font-size: 0.8rem;"></i>
                            <span>${escapeHtml(q.author)}</span>
                        </div>
                        ${q.author_url ? `<a href="${escapeHtml(q.author_url)}" target="_blank" rel="noopener" class="author-link"><i class="fa-solid fa-arrow-up-right-from-square"></i> Bio</a>` : ''}
                    </div>
                    ${tagPills ? `<div class="card-tags">${tagPills}</div>` : ''}
                    <div class="card-actions">
                        <button class="card-action-btn copy-btn" data-quote="${escapeHtml(q.quote)}" data-author="${escapeHtml(q.author)}">
                            <i class="fa-regular fa-copy"></i> Copy
                        </button>
                    </div>
                </div>
            `;
            quotesGrid.appendChild(card);
        });

        // Add event listeners for tag clicks in cards
        quotesGrid.querySelectorAll(".badge-tag").forEach(tagElem => {
            tagElem.addEventListener("click", () => {
                selectTag(tagElem.dataset.tag);
            });
        });

        // Add copy event listeners
        quotesGrid.querySelectorAll(".copy-btn").forEach(btn => {
            btn.addEventListener("click", () => {
                const quote = btn.dataset.quote;
                const author = btn.dataset.author;
                copyToClipboard(`"${quote}" — ${author}`);
            });
        });
    }

    function updatePagination(total, page, totalPages) {
        resultsCount.textContent = `Showing ${total} quote${total === 1 ? '' : 's'}`;
        pageIndicator.textContent = `Page ${page} of ${Math.max(1, totalPages)}`;

        prevPageBtn.disabled = page <= 1;
        nextPageBtn.disabled = page >= totalPages;
    }

    // -------------------------------------------------------------
    // Charts with Chart.js
    // -------------------------------------------------------------
    function renderCharts(data) {
        if (!window.Chart || !data) return;

        // 1. Authors Chart
        const ctxAuthors = document.getElementById("authorsChart");
        if (ctxAuthors) {
            if (state.charts.authors) state.charts.authors.destroy();

            const authorLabels = (data.top_authors || []).map(a => a.author);
            const authorCounts = (data.top_authors || []).map(a => a.count);

            state.charts.authors = new Chart(ctxAuthors, {
                type: "bar",
                data: {
                    labels: authorLabels,
                    datasets: [{
                        label: "Number of Quotes",
                        data: authorCounts,
                        backgroundColor: "rgba(99, 102, 241, 0.8)",
                        borderColor: "rgba(99, 102, 241, 1)",
                        borderRadius: 6,
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    indexAxis: "y",
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        x: {
                            beginAtZero: true,
                            ticks: { stepSize: 1 }
                        }
                    }
                }
            });
        }

        // 2. Tags Chart
        const ctxTags = document.getElementById("tagsChart");
        if (ctxTags) {
            if (state.charts.tags) state.charts.tags.destroy();

            const tagLabels = (data.top_tags || []).map(t => `#${t.tag}`);
            const tagCounts = (data.top_tags || []).map(t => t.count);

            const palette = [
                "#6366f1", "#ec4899", "#8b5cf6", "#10b981", "#f59e0b",
                "#3b82f6", "#14b8a6", "#f43f5e", "#64748b", "#a855f7"
            ];

            state.charts.tags = new Chart(ctxTags, {
                type: "doughnut",
                data: {
                    labels: tagLabels,
                    datasets: [{
                        data: tagCounts,
                        backgroundColor: palette.slice(0, tagLabels.length),
                        borderWidth: 2,
                        borderColor: "#ffffff"
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: "right",
                            labels: { boxWidth: 12, font: { size: 11 } }
                        }
                    }
                }
            });
        }

        // 3. Length Distribution Chart
        const ctxLength = document.getElementById("lengthChart");
        if (ctxLength) {
            if (state.charts.length) state.charts.length.destroy();

            const lengthDist = data.length_distribution || {};
            const distLabels = Object.keys(lengthDist);
            const distCounts = Object.values(lengthDist);

            state.charts.length = new Chart(ctxLength, {
                type: "bar",
                data: {
                    labels: distLabels,
                    datasets: [{
                        label: "Quotes Count",
                        data: distCounts,
                        backgroundColor: [
                            "rgba(16, 185, 129, 0.75)",
                            "rgba(59, 130, 246, 0.75)",
                            "rgba(236, 72, 153, 0.75)"
                        ],
                        borderRadius: 8,
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: { stepSize: 5 }
                        }
                    }
                }
            });
        }
    }

    // -------------------------------------------------------------
    // Event Listeners & Interaction
    // -------------------------------------------------------------
    function setupEventListeners() {
        // Search Input (Debounced)
        let debounceTimer;
        searchInput.addEventListener("input", (e) => {
            clearTimeout(debounceTimer);
            const val = e.target.value.trim();
            clearSearchBtn.style.display = val ? "block" : "none";
            debounceTimer = setTimeout(() => {
                state.searchQuery = val;
                state.currentPage = 1;
                loadQuotes();
            }, 300);
        });

        clearSearchBtn.addEventListener("click", () => {
            searchInput.value = "";
            clearSearchBtn.style.display = "none";
            state.searchQuery = "";
            state.currentPage = 1;
            loadQuotes();
        });

        // Author Select
        authorSelect.addEventListener("change", (e) => {
            state.currentAuthor = e.target.value;
            state.currentPage = 1;
            loadQuotes();
        });

        // Sort Select
        sortSelect.addEventListener("change", (e) => {
            state.currentSort = e.target.value;
            state.currentPage = 1;
            loadQuotes();
        });

        // Tag Chip Clicks
        popularTagsList.addEventListener("click", (e) => {
            const chip = e.target.closest(".tag-chip");
            if (!chip) return;
            selectTag(chip.dataset.tag || "");
        });

        // Pagination
        prevPageBtn.addEventListener("click", () => {
            if (state.currentPage > 1) {
                state.currentPage--;
                loadQuotes();
                window.scrollTo({ top: 350, behavior: "smooth" });
            }
        });

        nextPageBtn.addEventListener("click", () => {
            state.currentPage++;
            loadQuotes();
            window.scrollTo({ top: 350, behavior: "smooth" });
        });

        // Random Quote Modal
        randomBtn.addEventListener("click", openRandomQuoteModal);
        modalCloseBtn.addEventListener("click", closeRandomQuoteModal);
        window.addEventListener("click", (e) => {
            if (e.target === quoteModal) closeRandomQuoteModal();
        });
        modalAnotherBtn.addEventListener("click", fetchRandomQuote);
        modalCopyBtn.addEventListener("click", () => {
            const text = modalQuoteText.textContent;
            const author = modalQuoteAuthor.textContent;
            copyToClipboard(`${text} ${author}`);
        });

        // Run Scraper Button
        runScraperBtn.addEventListener("click", async () => {
            runScraperBtn.disabled = true;
            runScraperBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Scraping in progress...';
            scrapeStatus.textContent = "Connecting to quotes.toscrape.com...";

            try {
                const res = await fetch("/api/scrape", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ pages: 10 })
                });
                const result = await res.json();
                if (result.success) {
                    scrapeStatus.textContent = `Scrape complete! Extracted ${result.count} quotes.`;
                    showToast(`Scraped ${result.count} quotes successfully!`);
                    await loadAnalytics();
                    loadQuotes();
                } else {
                    scrapeStatus.textContent = `Error: ${result.error}`;
                }
            } catch (err) {
                scrapeStatus.textContent = "Network error during scraping.";
            } finally {
                runScraperBtn.disabled = false;
                runScraperBtn.innerHTML = '<i class="fa-solid fa-rotate"></i> Re-Scrape Website Now';
            }
        });
    }

    function selectTag(tag) {
        state.currentTag = tag;
        state.currentPage = 1;

        // Update active chip UI
        popularTagsList.querySelectorAll(".tag-chip").forEach(c => {
            if (c.dataset.tag === tag) {
                c.classList.add("active");
            } else {
                c.classList.remove("active");
            }
        });

        loadQuotes();
    }

    // -------------------------------------------------------------
    // Random Quote Helpers
    // -------------------------------------------------------------
    async function openRandomQuoteModal() {
        quoteModal.classList.add("show");
        await fetchRandomQuote();
    }

    function closeRandomQuoteModal() {
        quoteModal.classList.remove("show");
    }

    async function fetchRandomQuote() {
        modalQuoteText.textContent = "Fetching wisdom...";
        modalQuoteAuthor.textContent = "";
        modalQuoteTags.innerHTML = "";

        try {
            const res = await fetch("/api/random");
            const q = await res.json();
            modalQuoteText.textContent = `“${q.quote}”`;
            modalQuoteAuthor.textContent = `— ${q.author}`;
            modalQuoteTags.innerHTML = (q.tags || []).map(t => 
                `<span class="badge-tag">#${escapeHtml(t)}</span>`
            ).join("");
        } catch (err) {
            modalQuoteText.textContent = "Could not fetch a quote right now.";
        }
    }

    // -------------------------------------------------------------
    // Clipboard & Toast Utilities
    // -------------------------------------------------------------
    function copyToClipboard(text) {
        navigator.clipboard.writeText(text).then(() => {
            showToast("Copied to clipboard!");
        }).catch(() => {
            showToast("Failed to copy");
        });
    }

    function showToast(msg) {
        toast.textContent = msg;
        toast.classList.add("show");
        setTimeout(() => {
            toast.classList.remove("show");
        }, 2500);
    }

    function escapeHtml(str) {
        if (!str) return "";
        return str
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
});
