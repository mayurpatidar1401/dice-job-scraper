# 🤖 Dice Job Scraper & Automated Email Sender

A flexible and automated Python tool to help you search job listings on [Dice.com](https://dice.com), collect job details, and send out personalized emails with your resume—all in just a few clicks.

Perfect for professionals from **any industry** who want to automate and simplify their job application process.

---

## 🚀 What It Does

- 🔐 Logs into your Dice account automatically
- 🔎 Searches for jobs based on any **custom job title** and **location**
- 📑 Extracts job information like recruiter email, job title, and company name
- 📤 Sends customized emails with your resume to recruiters
- 📁 Stores job listings and tracks which ones you've already applied to
- 🔄 Supports pagination, "Easy Apply", and skips external job listings

---

## 🧰 Requirements

- Python 3.8 or later
- Google Chrome (latest stable)
- ChromeDriver (must match your Chrome version)
- Gmail App Password (for sending emails securely)

---

## 📦 Installation

1. **Clone this repository**

```bash
git clone https://github.com/mayurpatidar1401/dice-job-scraper.git
cd dice-job-scraper
```

2. **Create and activate a virtual environment**

```bash
# Create a virtual environment (Linux/Mac)
python3 -m venv venv

# Activate it
source venv/bin/activate

# On Windows:
# python -m venv venv
# venv\Scripts\activate
```
3. **Install required dependencies**
```bash
pip install -r requirements.txt
```

## 🛠 Update Credentials & Paths
**🔧 dice_scraper.py – Job Search & Scraping**
Update the following values to match your setup:

USER_EMAIL = "your_email@gmail.com"            # Dice login email
USER_PASSWORD = "your_dice_password"           # Dice login password (or app password)
SEARCH_ROLE = "Software Engineer"              # Your target job title
cities_to_check = ["New York", "Boston", "Irving"]  # List of cities/locations to search
output_folder = "Dice-Job-SCRAPER/Job_List_Data" # Change to your desired output folder

**📧 AutoEmailScript.py – Resume & Email Sender**
Update your sender info and file paths here:

SENDER_EMAIL = "your_email@gmail.com"              # Gmail address used to send emails
SENDER_PASSWORD = "your_gmail_app_password"        # App password (NOT your real Gmail password)
resume_path = "/path/to/your_resume.docx"          # Path to your resume file
excel_path = "Job_List_Data/job_listings.xlsx"     # Path to your job tracking Excel file
⚠️ Make sure the file paths exist, and you've downloaded or created the Excel file if needed.

## 💬 Customize the Email Body

To edit the message sent with each application:

    Open AutoEmailScript.py

    Locate the body = f"""...""" block inside the send_emails() function

    Edit the text and use variables like {job_title} for personalization:

## ▶️ How to Use

### Step 1: Scrape Job Listings

```bash
python dice_scraper.py
```
This script logs into Dice, searches for jobs, extracts relevant details, and stores them in an Excel file.

### Step 2: Send Emails

```bash
python AutoEmailScript.py
```
This reads unsent jobs from the Excel sheet and emails recruiters with your resume.

## ⚠️ Error Handling

    Skips external job links

    Skips jobs without an "Easy Apply" button

    Continues if resume or fields are missing

    Handles dynamic content and pagination reliably

## Disclaimer

This project is for educational and personal automation only.
Automating interactions on job platforms may violate their terms of service. Use responsibly.
