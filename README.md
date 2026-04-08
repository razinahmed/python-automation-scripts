<div align="center">

# 🐍 Ultimate Python Automation Scripts

<img src="https://placehold.co/900x250/1e1e2e/00d4aa.png?text=Python+Automation+%7C+Scripts+%7C+Productivity" alt="Python Automation Banner" />

<br/>

**A premium collection of production-ready Python scripts designed to automate the boring parts of your digital life — from file management to web scraping to cloud backups.**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.0-43B02A?style=for-the-badge&logo=selenium&logoColor=white)](https://www.selenium.dev/)
[![AWS](https://img.shields.io/badge/AWS-S3-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)](https://aws.amazon.com/s3/)
[![License: MIT](https://img.shields.io/badge/License-MIT-00d4aa?style=for-the-badge)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge)](http://makeapullrequest.com)

[Scripts](#-the-scripts) · [Quick Start](#-quick-start) · [Scheduling](#-scheduling-automation) · [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [About](#-about)
- [The Scripts](#-the-scripts)
- [Detailed Script Descriptions](#-detailed-script-descriptions)
- [Quick Start](#-quick-start)
- [Before & After Examples](#-before--after-examples)
- [Scheduling Automation](#-scheduling-automation)
- [Configuration](#-configuration)
- [Project Structure](#-project-structure)
- [Tech Stack](#-tech-stack)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🔍 About

This repository is a growing collection of **Python automation scripts** that handle repetitive tasks so you don't have to. Each script is self-contained, well-documented, and designed with CLI arguments for flexibility. Whether you need to organize a messy desktop, monitor prices for drops, resize thousands of images, or automate cloud backups, there is a script here for you.

---

## 🚀 The Scripts

| Script | Category | Description | Complexity |
|---|---|---|:-:|
| **`clean_desktop.py`** | File System | Automatically sorts and organizes files from any directory into categorized folders based on file extensions | 🟢 Easy |
| **`bulk_image_resizer.py`** | Image Processing | Losslessly compresses and resizes thousands of images in parallel using multiple CPU cores | 🟡 Medium |
| **`scout_scraper.py`** | Web Scraping | Headless browser script that monitors URLs for price drops and sends Telegram/email alerts | 🔴 Advanced |
| **`auto_backup.py`** | System / Cloud | Zips important directories and uploads them to AWS S3 with timestamped naming | 🟡 Medium |
| **`pdf_merger.py`** | File System | Merges multiple PDF files into a single document with optional page ordering | 🟢 Easy |
| **`email_sender.py`** | Communication | Bulk email sender with HTML templates, attachments, and CSV recipient lists | 🟡 Medium |
| **`log_analyzer.py`** | DevOps | Parses server log files, extracts error patterns, and generates summary reports | 🟡 Medium |
| **`duplicate_finder.py`** | File System | Scans directories for duplicate files using SHA-256 hashing and provides cleanup options | 🟢 Easy |

---

## 📖 Detailed Script Descriptions

### 1. `clean_desktop.py` — File Organizer

Automatically categorizes files based on their extensions and moves them into organized folders.

**Extension Mapping:**

| Category | Extensions | Target Folder |
|---|---|---|
| Images | `.jpg`, `.png`, `.gif`, `.svg`, `.webp` | `Images/` |
| Documents | `.pdf`, `.docx`, `.xlsx`, `.pptx`, `.txt` | `Documents/` |
| Videos | `.mp4`, `.mkv`, `.avi`, `.mov` | `Videos/` |
| Music | `.mp3`, `.wav`, `.flac`, `.aac` | `Music/` |
| Archives | `.zip`, `.rar`, `.7z`, `.tar.gz` | `Archives/` |
| Code | `.py`, `.js`, `.ts`, `.html`, `.css` | `Code/` |

```bash
python src/clean_desktop.py --target ~/Desktop --dry-run    # Preview changes
python src/clean_desktop.py --target ~/Desktop              # Execute
```

### 2. `bulk_image_resizer.py` — Parallel Image Processing

Resizes and compresses images using all available CPU cores for maximum throughput.

```bash
# Resize all images in a folder to max 1920px width
python src/bulk_image_resizer.py --input ./photos --output ./resized --max-width 1920

# Compress with quality setting
python src/bulk_image_resizer.py --input ./photos --output ./compressed --quality 85
```

**Performance:** Processes ~500 images/minute on a 4-core machine.

### 3. `scout_scraper.py` — Price Monitor

Uses headless Selenium to monitor product pages and alert you when prices drop below your threshold.

```bash
# Monitor a product URL
python src/scout_scraper.py --url "https://amazon.com/dp/..." --threshold 29.99 --interval 3600

# With Telegram notifications
python src/scout_scraper.py --url "https://..." --threshold 49.99 --notify telegram
```

### 4. `auto_backup.py` — Cloud Backup

Compresses directories and uploads them to AWS S3 with automatic timestamping and rotation.

```bash
# Backup specific directories to S3
python src/auto_backup.py --dirs ~/Documents ~/Projects --bucket my-backups

# With retention policy (keep last 30 backups)
python src/auto_backup.py --dirs ~/Documents --bucket my-backups --retain 30
```

---

## 🏁 Before & After Examples

### Desktop Cleanup

**Before:**
```
~/Desktop/
├── report_final_v2.docx
├── IMG_2847.jpg
├── meeting_notes.txt
├── project.zip
├── vacation_photo.png
├── budget_2025.xlsx
├── song.mp3
├── presentation.pptx
└── screenshot_143.png
```

**After running `clean_desktop.py`:**
```
~/Desktop/
├── Documents/
│   ├── report_final_v2.docx
│   ├── meeting_notes.txt
│   ├── budget_2025.xlsx
│   └── presentation.pptx
├── Images/
│   ├── IMG_2847.jpg
│   ├── vacation_photo.png
│   └── screenshot_143.png
├── Music/
│   └── song.mp3
└── Archives/
    └── project.zip
```

---

## ⏰ Scheduling Automation

### Linux/macOS — Cron Jobs

Edit your crontab with `crontab -e`:

```bash
# Run desktop cleanup every day at 9 AM
0 9 * * * /usr/bin/python3 /path/to/src/clean_desktop.py --target ~/Desktop

# Run backup every Sunday at 2 AM
0 2 * * 0 /usr/bin/python3 /path/to/src/auto_backup.py --dirs ~/Documents --bucket my-backups

# Run price monitor every hour
0 * * * * /usr/bin/python3 /path/to/src/scout_scraper.py --url "https://..." --threshold 29.99

# Run duplicate finder weekly on Fridays at midnight
0 0 * * 5 /usr/bin/python3 /path/to/src/duplicate_finder.py --dir ~/Downloads --auto-clean
```

### Windows — Task Scheduler

1. Open **Task Scheduler** (`taskschd.msc`)
2. Click **Create Basic Task**
3. Set your trigger (Daily, Weekly, etc.)
4. Set the action:
   - **Program:** `C:\Python310\python.exe`
   - **Arguments:** `C:\path\to\src\clean_desktop.py --target C:\Users\You\Desktop`
5. Click **Finish**

Alternatively, use PowerShell:

```powershell
$action = New-ScheduledTaskAction -Execute "python" -Argument "C:\path\to\src\clean_desktop.py --target $env:USERPROFILE\Desktop"
$trigger = New-ScheduledTaskTrigger -Daily -At 9am
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "DesktopCleanup" -Description "Auto-organize desktop files"
```

---

## ⚙️ Configuration

Each script supports CLI arguments. Use `--help` to see all options:

```bash
python src/clean_desktop.py --help
python src/bulk_image_resizer.py --help
python src/scout_scraper.py --help
python src/auto_backup.py --help
```

### Global Configuration (`config.yaml`)

```yaml
notifications:
  telegram_bot_token: "your-bot-token"
  telegram_chat_id: "your-chat-id"
  email_smtp_host: "smtp.gmail.com"
  email_smtp_port: 587

aws:
  region: "us-east-1"
  bucket: "my-automation-backups"

defaults:
  image_quality: 85
  max_image_width: 1920
  backup_retention: 30
```

---

## 📁 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/razinahmed/python-automation-scripts.git
cd python-automation-scripts
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Run a Script

```bash
python src/clean_desktop.py --target ~/Desktop --dry-run
```

---

## 📁 Project Structure

```
python-automation-scripts/
├── src/
│   ├── clean_desktop.py          # File organizer script
│   ├── bulk_image_resizer.py     # Parallel image processor
│   ├── scout_scraper.py          # Price monitoring scraper
│   ├── auto_backup.py            # AWS S3 backup script
│   ├── pdf_merger.py             # PDF merge utility
│   ├── email_sender.py           # Bulk email sender
│   ├── log_analyzer.py           # Server log parser
│   └── duplicate_finder.py       # Duplicate file detector
├── config/
│   └── config.yaml               # Global configuration
├── templates/
│   └── email_template.html       # HTML email template
├── tests/                        # Unit tests
├── requirements.txt              # Python dependencies
├── LICENSE
└── README.md
```

---

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| **Language** | Python 3.10+ |
| **Web Scraping** | Selenium, BeautifulSoup4, requests |
| **Image Processing** | Pillow (PIL) |
| **Cloud** | boto3 (AWS S3) |
| **PDF** | PyPDF2 |
| **Email** | smtplib, email.mime |
| **CLI** | argparse, click |
| **Notifications** | python-telegram-bot, smtplib |
| **Hashing** | hashlib (SHA-256) |
| **Concurrency** | multiprocessing, concurrent.futures |

---

## 🤝 Contributing

Have a script that saves you hours of time? Contributions are welcome!

1. **Fork** this repository
2. **Create** a feature branch (`git checkout -b script/new-automation`)
3. **Add** your script to the `src/` directory
4. **Include** CLI argument support with `--help`
5. **Write** a brief description for the scripts table
6. **Submit** a Pull Request

### Script Guidelines
- Must be self-contained (single file preferred)
- Include `--help` and `--dry-run` flags where applicable
- Add error handling and meaningful log messages
- Follow PEP 8 style conventions

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with passion by [Razin Ahmed](https://github.com/razinahmed)**

If these scripts saved you time, please give the repo a ⭐

<img src="https://komarev.com/ghpvc/?username=razinahmed&style=flat-square&color=00d4aa&label=REPO+VIEWS" alt="Repo Views" />

</div>
