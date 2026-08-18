# Kindle RSS Newspaper

A Python-based personal RSS newspaper generator for Amazon Kindle.

The project collects articles from configurable RSS feeds, extracts and cleans the article content, generates a Kindle-friendly EPUB file, and automatically sends it to a Kindle device using Amazon's **Send to Kindle** email service.

The entire workflow can also be scheduled to run automatically every morning using:

* `cron` on Linux
* `launchd` on macOS
* Windows Task Scheduler on Windows

The final goal is simple:

```text
RSS Feeds
    ↓
Article Extraction
    ↓
Content Cleaning
    ↓
EPUB Generation
    ↓
Send to Kindle
    ↓
Automatic Daily Delivery
```

---

## Features

* RSS / Atom feed parsing
* Multiple configurable news sources
* Article categorization
* Full article extraction
* RSS summary fallback when full extraction fails
* HTML cleaning and normalization
* Duplicate article removal
* Kindle-friendly EPUB generation
* Custom CSS styling
* Table of contents generation
* Automatic EPUB delivery using SMTP
* Amazon Send to Kindle integration
* Environment-based credential management
* Logging
* Daily automation support on Linux, macOS and Windows

---

# Architecture

The project follows a modular structure where each component has a specific responsibility.

```text
Kindle_RSS/
│
├── config/
│   └── feeds.yaml
│
├── output/
│   └── generated EPUB files
│
├── logs/
│   ├── launchd.log
│   └── launchd_error.log
│
├── src/
│   ├── __init__.py
│   ├── feed_reader.py
│   ├── article_extractor.py
│   ├── epub_builder.py
│   ├── kindle_sender.py
│   └── utils.py
│
├── templates/
│   └── article.css
│
├── tests/
│   ├── test_feed.py
│   ├── test_extractor.py
│   └── test_kindle_sender.py
│
├── .env
├── .env.example
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
```

---

# Workflow

The complete workflow is:

```text
config/feeds.yaml
        │
        ▼
   feed_reader.py
        │
        ▼
   RSS / Atom feeds
        │
        ▼
 normalized articles
        │
        ▼
 remove_duplicates()
        │
        ▼
 article_extractor.py
        │
        ├── Trafilatura
        └── BeautifulSoup
        │
        ▼
 cleaned article content
        │
        ▼
   epub_builder.py
        │
        ▼
 Daily Newspaper EPUB
        │
        ▼
  kindle_sender.py
        │
        ▼
      SMTP
        │
        ▼
 Amazon Send to Kindle
        │
        ▼
      Kindle
```

---

# Requirements

Recommended Python version:

```text
Python 3.11+
```

The project has been tested with:

```text
Python 3.12
```

Main Python dependencies:

```text
feedparser
requests
beautifulsoup4
trafilatura
EbookLib
PyYAML
python-dotenv
Pillow
```

---

# Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/Kindle_RSS.git
```

Enter the project directory:

```bash
cd Kindle_RSS
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate it.

### Linux / macOS

```bash
source venv/bin/activate
```

### Windows

```powershell
venv\Scripts\activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

---

# RSS Feed Configuration

RSS sources are configured inside:

```text
config/feeds.yaml
```

Example:

```yaml
newspaper:
  title: "Dario Daily News"
  language: "it"
  max_articles_per_feed: 5
  include_images: false
  send_to_kindle: true

feeds:

  - name: "Python Blog"
    url: "https://blog.python.org/feeds/posts/default"
    category: "Python"

  - name: "Linux News"
    url: "RSS_FEED_URL"
    category: "Linux"

  - name: "Cyber Security"
    url: "RSS_FEED_URL"
    category: "Cyber Security"
```

Each feed supports:

```yaml
name:
url:
category:
```

A feed can also override the global article limit:

```yaml
max_articles: 10
```

For example:

```yaml
- name: "Security News"
  url: "RSS_FEED_URL"
  category: "Cyber Security"
  max_articles: 10
```

---

# Newspaper Configuration

The main newspaper settings are located in:

```yaml
newspaper:
  title: "Dario Daily News"
  language: "it"
  max_articles_per_feed: 5
  include_images: false
  send_to_kindle: true
```

### `title`

Defines the EPUB title and output filename.

For example:

```yaml
title: "Dario Daily News"
```

will generate something similar to:

```text
Dario_Daily_News_2026-08-18.epub
```

### `max_articles_per_feed`

Defines the default maximum number of articles collected from each RSS feed.

### `send_to_kindle`

Enable automatic Kindle delivery:

```yaml
send_to_kindle: true
```

Disable it during development:

```yaml
send_to_kindle: false
```

---

# RSS Parsing

RSS and Atom feeds are parsed using:

```text
feedparser
```

The feed reader normalizes each article into a common internal structure:

```python
{
    "source": "...",
    "category": "...",
    "title": "...",
    "url": "...",
    "published": "...",
    "summary": "..."
}
```

This allows the rest of the application to work independently from the original feed format.

---

# Article Extraction

Full article extraction is performed using:

```text
Trafilatura
```

The extractor downloads the original webpage and attempts to retrieve the main article content.

The workflow is:

```text
Article URL
    ↓
Download HTML
    ↓
Trafilatura
    ↓
Main content extraction
    ↓
BeautifulSoup
    ↓
HTML cleaning
```

Unnecessary HTML elements such as the following are removed:

```text
script
style
iframe
video
audio
form
button
noscript
```

If full article extraction fails, the application automatically falls back to the RSS summary.

```text
Full extraction successful
        ↓
full_article

Full extraction failed
        ↓
rss_summary
```

This ensures that a single inaccessible website does not break the entire newspaper generation process.

---

# Duplicate Removal

Duplicate articles are detected using normalized URLs.

Tracking parameters and fragments are removed before comparison.

For example:

```text
https://example.com/article?id=123&utm_source=twitter
```

can be normalized before duplicate detection.

This prevents the same article from appearing multiple times in the same edition.

---

# EPUB Generation

EPUB files are generated using:

```text
EbookLib
```

The generated newspaper contains:

```text
Front Page
│
├── Newspaper title
├── Edition date
└── Article count

Table of Contents
│
├── Article 1
├── Article 2
├── Article 3
└── ...

Articles
│
├── Category
├── Title
├── Source
├── Publication date
├── Article content
└── Original article link
```

The output is written to:

```text
output/
```

For example:

```text
output/Dario_Daily_News_2026-08-18.epub
```

---

# Kindle Styling

The EPUB appearance is controlled by:

```text
templates/article.css
```

The CSS is intentionally kept simple to maximize compatibility with Kindle e-ink devices.

Typical styling includes:

* serif fonts
* responsive images
* article metadata
* category labels
* newspaper-style headings
* readable margins
* justified paragraphs
* Kindle-friendly spacing
* minimal layout complexity

Modern browser-specific CSS such as complex grids or interactive layouts is intentionally avoided.

---

# Environment Variables

Sensitive information is stored inside:

```text
.env
```

Example:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587

SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

KINDLE_EMAIL=your-kindle-address@kindle.com
```

Never commit the real `.env` file.

The repository should contain:

```text
.env.example
```

with placeholder values:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587

SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password

KINDLE_EMAIL=your_kindle_address@kindle.com
```

---

# Gmail App Password

When using Gmail SMTP, the normal Google account password should not be stored in the application.

A Google **App Password** should be used instead.

Typical setup:

```text
Google Account
    ↓
Security
    ↓
2-Step Verification
    ↓
App Passwords
    ↓
Create "Kindle RSS"
```

The generated App Password is then placed inside:

```env
SMTP_PASSWORD=your_app_password
```

---

# Amazon Send to Kindle

Every Kindle device can have a personal Send to Kindle email address.

It usually has the following format:

```text
your-name@kindle.com
```

The sending email address must also be added to Amazon's approved personal document email list.

The delivery workflow becomes:

```text
Python
    ↓
SMTP
    ↓
your-email@gmail.com
    ↓
your-kindle-address@kindle.com
    ↓
Amazon
    ↓
Kindle
```

---

# Automatic Kindle Delivery

The module:

```text
src/kindle_sender.py
```

uses Python's standard SMTP libraries to attach the generated EPUB and send it to the Kindle email address.

The complete automatic workflow is therefore:

```text
python main.py
    ↓
Read RSS feeds
    ↓
Extract articles
    ↓
Clean content
    ↓
Generate EPUB
    ↓
Send EPUB through SMTP
    ↓
Amazon Send to Kindle
    ↓
Kindle
```

---

# Running the Project

Run:

```bash
python main.py
```

If automatic delivery is enabled:

```yaml
send_to_kindle: true
```

the newspaper will be generated and automatically delivered to the Kindle.

If delivery is disabled:

```yaml
send_to_kindle: false
```

only the EPUB will be generated.

---

# Testing

Feed reader:

```bash
python -m tests.test_feed
```

Article extraction:

```bash
python -m tests.test_extractor
```

Kindle delivery:

```bash
python -m tests.test_kindle_sender
```

---

# Logs

Application execution can be monitored using log files.

When using the macOS `launchd` configuration described below:

```text
logs/launchd.log
logs/launchd_error.log
```

Standard output:

```bash
cat logs/launchd.log
```

Standard error:

```bash
cat logs/launchd_error.log
```

---

# Final Step: Daily Automation

The final step is to schedule the entire workflow so that the newspaper is generated and delivered automatically every day.

The operating system determines which scheduler should be used.

```text
Linux
    ↓
cron / systemd timer

macOS
    ↓
launchd

Windows
    ↓
Task Scheduler
```

---

# Linux Automation with cron

On Linux, the simplest solution is `cron`.

Find the absolute Python path:

```bash
which python
```

For a virtual environment it may look like:

```text
/home/user/Kindle_RSS/venv/bin/python
```

Edit the user's crontab:

```bash
crontab -e
```

Example: execute every morning at 07:00:

```cron
0 7 * * * cd /home/user/Kindle_RSS && /home/user/Kindle_RSS/venv/bin/python main.py >> logs/cron.log 2>&1
```

Workflow:

```text
07:00
  ↓
cron
  ↓
venv/bin/python
  ↓
main.py
  ↓
EPUB
  ↓
Kindle
```

For more advanced Linux installations, a `systemd timer` can be used instead of cron.

---

# macOS Automation with launchd

On macOS, the recommended solution is:

```text
launchd
```

Create:

```text
~/Library/LaunchAgents/com.dario.kindle-rss.plist
```

Example:

```xml
<?xml version="1.0" encoding="UTF-8"?>

<!DOCTYPE plist PUBLIC
"-//Apple//DTD PLIST 1.0//EN"
"http://www.apple.com/DTDs/PropertyList-1.0.dtd">

<plist version="1.0">

<dict>

    <key>Label</key>
    <string>com.dario.kindle-rss</string>

    <key>ProgramArguments</key>
    <array>
        <string>/Users/dario/Dev/Kindle_RSS/venv/bin/python</string>
        <string>/Users/dario/Dev/Kindle_RSS/main.py</string>
    </array>

    <key>WorkingDirectory</key>
    <string>/Users/dario/Dev/Kindle_RSS</string>

    <key>StartCalendarInterval</key>
    <dict>

        <key>Hour</key>
        <integer>7</integer>

        <key>Minute</key>
        <integer>0</integer>

    </dict>

    <key>StandardOutPath</key>
    <string>/Users/dario/Dev/Kindle_RSS/logs/launchd.log</string>

    <key>StandardErrorPath</key>
    <string>/Users/dario/Dev/Kindle_RSS/logs/launchd_error.log</string>

</dict>

</plist>
```

Validate:

```bash
plutil -lint ~/Library/LaunchAgents/com.dario.kindle-rss.plist
```

Load:

```bash
launchctl bootstrap gui/$(id -u) \
~/Library/LaunchAgents/com.dario.kindle-rss.plist
```

Check:

```bash
launchctl list | grep com.dario.kindle-rss
```

Example output:

```text
-    0    com.dario.kindle-rss
```

Meaning:

```text
PID              -
Last exit code   0
Service          com.dario.kindle-rss
```

A `0` exit code means the last execution completed successfully.

Run immediately:

```bash
launchctl kickstart -k \
gui/$(id -u)/com.dario.kindle-rss
```

Show detailed information:

```bash
launchctl print \
gui/$(id -u)/com.dario.kindle-rss
```

Unload:

```bash
launchctl bootout \
gui/$(id -u)/com.dario.kindle-rss
```

Important:

```text
~/Library/LaunchAgents
```

is the per-user LaunchAgents directory.

It is different from:

```text
/Library/LaunchAgents
```

which is system-wide and normally requires administrative privileges.

For this project, the per-user directory should be used:

```text
/Users/<username>/Library/LaunchAgents
```

The LaunchAgent should be created and managed as the normal macOS user, not as `root`.

---

# Windows Automation with Task Scheduler

On Windows, the equivalent solution is **Task Scheduler**.

Open:

```text
Start
→ Task Scheduler
```

Choose:

```text
Create Basic Task
```

Example task name:

```text
Kindle RSS Newspaper
```

Select:

```text
Daily
```

and choose:

```text
07:00
```

As the program, use the Python executable inside the virtual environment:

```text
C:\Users\USERNAME\Dev\Kindle_RSS\venv\Scripts\python.exe
```

Arguments:

```text
main.py
```

Start in:

```text
C:\Users\USERNAME\Dev\Kindle_RSS
```

The final Windows workflow is:

```text
07:00
  ↓
Task Scheduler
  ↓
venv\Scripts\python.exe
  ↓
main.py
  ↓
RSS
  ↓
EPUB
  ↓
Kindle
```

---

# Cross-Platform Automation Summary

| Operating System | Scheduler      |
| ---------------- | -------------- |
| Linux            | cron           |
| Linux            | systemd timer  |
| macOS            | launchd        |
| Windows          | Task Scheduler |

Regardless of the operating system, the scheduled command is conceptually always:

```text
virtual-environment-python main.py
```

---

# Security

Never commit:

```text
.env
```

Never commit:

```text
SMTP_PASSWORD
```

Never commit:

```text
KINDLE_EMAIL
```

if you prefer to keep the Kindle address private.

Recommended `.gitignore`:

```gitignore
# Environment variables
.env

# Virtual environment
venv/
.venv/

# Python
__pycache__/
*.py[cod]

# Generated newspapers
output/
*.epub

# Logs
logs/
*.log

# macOS
.DS_Store

# IDE
.vscode/
.idea/
```

---

# Example Daily Workflow

Once automation is configured, no manual intervention is required.

```text
07:00
  │
  ▼
Operating System Scheduler
  │
  ▼
Python Virtual Environment
  │
  ▼
main.py
  │
  ├── Load feeds.yaml
  ├── Read RSS feeds
  ├── Remove duplicates
  ├── Extract articles
  ├── Clean HTML
  ├── Generate EPUB
  └── Send to Kindle
  │
  ▼
Amazon
  │
  ▼
Kindle
```

The result is a fresh personal newspaper already available on the Kindle every morning.

---

# Possible Future Improvements

Possible extensions include:

* category-based EPUB table of contents
* article history database
* avoid previously delivered articles
* daily vs weekly editions
* automatic image download
* article relevance scoring
* keyword filters
* language filters
* AI-generated summaries
* automatic arXiv paper digest
* GitHub release/news digest
* retry logic for SMTP failures
* notification when delivery fails
* Docker deployment
* Raspberry Pi deployment
* remote server deployment
* systemd service and timer
* GitHub Actions scheduling

---

# Technologies

The project currently uses:

```text
Python
Feedparser
Trafilatura
BeautifulSoup
EbookLib
PyYAML
python-dotenv
SMTP
Amazon Send to Kindle
```

Automation:

```text
Linux      → cron / systemd
macOS      → launchd
Windows    → Task Scheduler
```

---

# Project Goal

The project was created with one simple goal:

> Wake up in the morning and find a fresh, automatically generated personal newspaper already waiting on the Kindle.

```text
RSS → EPUB → Kindle → Coffee
```

Enjoy your morning reading. ☕📖
