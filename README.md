# 🌐 Universal Web Scraper

A powerful and flexible Python-based web scraper that supports scraping **Instagram profiles** and **generic websites** with structured outputs and categorized downloads.

---

## 🚀 Features

### 🔹 Instagram Scraper
- Uses **Instaloader** and **Playwright** to scrape:
  - Public profile info (bio, followers, etc.)
  - Profile picture
  - All posts, reels, and tagged media links
  - Downloads selected media by type

### 🔹 Generic Website Scraper
- Scrapes any website's:
  - Title, headings, and full text
  - All links
  - All images

---

## 📁 Project Structure

```

.
├── config/
│   └── config.py
├── core/
│   ├── browser.py
│   ├── cookies.py
│   ├── file\_manager.py
│   └── proxies.py
├── scrapers/
│   ├── instagram.py
│   └── generic.py
├── utils/
│   └── helpers.py
├── downloads/
│   └── \[All scraped data stored here]
├── main.py
└── README.md

````

---

## ⚙️ Requirements

- Python 3.8+
- Install dependencies:

```bash
pip install -r requirements.txt
````

Make sure to install `playwright` and install its browser binaries:

```bash
pip install playwright
playwright install
```

---

## 🔐 Environment Variables (Optional)

Set up a `.env` file or export environment variables:

```env
IG_USERNAME=your_ig_username
IG_PASSWORD=your_ig_password
PROXY_URL=http://user:pass@host:port   # optional
```

---

## 📦 Usage

Run the program using `main.py` via command-line.

### 1. Instagram Scraper

```bash
python main.py instagram <username>
```

* Scrapes user profile data and downloads selected posts/reels.
* Output stored under:

```
downloads/instagram/instagram/<username>/
```

### 2. Generic Website Scraper

```bash
python main.py generic <url>
```

* Scrapes text, links, and images.
* Output stored under:

```
downloads/generic/<domain>/
```

---

## 🔍 How It Works (Instagram)

1. Logs in with your credentials (only once; saves session cookies).
2. Scrapes:

   * Bio, followers, following, external links.
   * Media links from Posts, Reels, and Tagged sections.
3. Saves all links in a CSV: `all_links.csv`.
4. Downloads selected number of media items from each category.

---

## 📂 Output Example

For `instagram userid`:

```
downloads/
└── instagram/
    └── instagram/
        └── userid/
            ├── text/
            │   ├── profile_info.txt
            │   └── all_links.csv
            ├── images/
            ├── videos/
            └── post/
```

---

## 🛡️ Notes

* Media download counts are configured in `main.py` via:

```python
{
    "post": 2,
    "reel": 2,
    "tagged": 0
}
```

* If you want more/less downloads, change the numbers above.
* Reels go to the `videos/` folder.

---

🛡️ Disclaimer

This project is for educational and personal use only. Use responsibly and comply with all relevant platform policies and terms of service.