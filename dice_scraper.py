from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import pandas as pd
import datetime
import time
import json
import os
import re
import AutoEmailScript

# ========== Configuration Section ==========
# Replace with your own credentials before running
USER_EMAIL = "your_email@gmail.com" # Change to your dice email
USER_PASSWORD = "your_dice_password" # Change to your dice password

# Job title to search for
SEARCH_ROLE = "Software Engineer" # Change as needed

# Generate a unique profile directory based on the user email
user_id = USER_EMAIL.split('@')[0]
chrome_profile_dir = os.path.expanduser(f"~/automated-job-profile-{user_id}")
print(f"🛠️ Using browser session directory: {chrome_profile_dir}")

# Setup Chrome options
chrome_opts = webdriver.ChromeOptions()
chrome_opts.binary_location = "/usr/bin/google-chrome-stable"
chrome_opts.add_argument(f"--user-data-dir={chrome_profile_dir}")
chrome_opts.add_argument("--disable-popup-blocking")
chrome_opts.add_argument("--no-first-run")
chrome_opts.add_argument("--disable-background-networking")
chrome_opts.add_argument("--disable-sync")
chrome_opts.add_argument("--disable-features=NetworkService")
chrome_opts.add_argument("--enable-features=NetworkServiceInProcess")
chrome_opts.add_argument("--disable-features=CookiesWithoutSameSiteMustBeSecure")
# chrome_opts.add_argument("--headless=new") # Uncomment for headless mode
chrome_opts.add_argument("--disable-gpu")
chrome_opts.add_argument("--no-sandbox")
chrome_opts.add_argument("--disable-dev-shm-usage")

# Launch browser using undetected ChromeDriver
browser = uc.Chrome(options=chrome_opts)
time.sleep(2)
browser.maximize_window()

# Global job list to store extracted data
job_entries = []

# ========== Helper Functions ==========

def collect_job_info():
    """Parse job data from the job details page."""
    try:
        print("🔍 Parsing job details...")

        html_content = browser.page_source
        matched_data = re.search(r'"application":\s*({.*?})', html_content)

        if matched_data:
            job_info = json.loads(matched_data.group(1))
            to_email = job_info.get("email", "Not Available")
            cc_email = job_info.get("ccEmail", "Not Available")
        else:
            to_email, cc_email = "Not Available", "Not Available"

        try:
            company = WebDriverWait(browser, 5).until(
                EC.presence_of_element_located((By.XPATH, "//li[@class='mr']/a"))
            ).text
        except:
            company = "Unknown"

        try:
            title_element = WebDriverWait(browser, 5).until(
                EC.presence_of_element_located((By.XPATH, "//dhi-report-job-form"))
            )
            role_title = title_element.get_attribute("job-title")
        except:
            role_title = "Unknown"

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        job_entries.append([to_email, cc_email, company, role_title, timestamp, "No"])

        print(f"✅ Job extracted: {company} | {role_title} | {to_email}")

    except Exception as err:
        print(f"⚠️ Failed to extract job details: {err}")

def export_to_excel():
    """Save collected job records to an Excel file."""
    output_folder = "Dice-Job-SCRAPER/Job_List_Data" # Change to your desired output folder
    output_file = os.path.join(output_folder, "job_listings.xlsx")

    os.makedirs(output_folder, exist_ok=True)

    headers = ["To", "CC", "Company Name", "Job Title", "Timestamp", "Email Sent"]
    df_new = pd.DataFrame(job_entries, columns=headers)

    if os.path.exists(output_file):
        df_existing = pd.read_excel(output_file)
        combined = pd.concat([df_existing, df_new], ignore_index=True)
        combined.drop_duplicates(subset=["To", "CC", "Company Name", "Job Title"], keep="first", inplace=True)
        combined.to_excel(output_file, index=False, engine="openpyxl")
        print(f"📁 Updated: {output_file} with new unique entries.")
    else:
        df_new.to_excel(output_file, index=False, engine="openpyxl")
        print(f"📁 Created new file: {output_file}")

def scrape_jobs_for_city(city):
    """Search and collect jobs for a specific city/location."""
    try:
        print(f"\n🌎 Searching for jobs in: {city}")
        browser.get("https://www.dice.com/jobs")
        time.sleep(5)

        job_input = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.ID, "typeInput"))
        )
        job_input.clear()
        job_input.send_keys(SEARCH_ROLE + "\n")

        location_input = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.ID, "google-location-search"))
        )
        location_input.clear()
        location_input.send_keys(city + "\n")

        WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "search-card"))
        )
        print(f"🔎 Search results loaded for {city}.")

        # Apply filters
        try:
            filter_button = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-cy='posted-date-option' and contains(text(),'Today')]"))
            )
            filter_button.click()
            print("✅ Filter applied: Posted Today")
        except:
            print("⚠️ Could not apply 'Today' filter.")

        time.sleep(3)

        # Attempt to enable "Easy Apply" filter
        try:
            easy_filter_button = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(@aria-label, 'Filter Search Results by Easy Apply')]"))
            )
            is_selected = browser.execute_script("return arguments[0].getAttribute('aria-checked');", easy_filter_button)

            if is_selected != "true":
                browser.execute_script("arguments[0].scrollIntoView();", easy_filter_button)
                time.sleep(1)
                browser.execute_script("arguments[0].click();", easy_filter_button)
                print("✅ 'Easy Apply' filter enabled.")
            else:
                print("🔄 'Easy Apply' filter already active.")
        except Exception as err:
            print(f"⚠️ Couldn't activate 'Easy Apply': {err}")

        time.sleep(4)

        # Loop through job listings
        while True:
            listings = browser.find_elements(By.XPATH, "//a[@data-cy='card-title-link']")
            for i in range(len(listings)):
                try:
                    listings = browser.find_elements(By.XPATH, "//a[@data-cy='card-title-link']")
                    current_listing = listings[i]

                    browser.execute_script("arguments[0].scrollIntoView();", current_listing)
                    time.sleep(1)
                    browser.execute_script("arguments[0].click();", current_listing)
                    browser.switch_to.window(browser.window_handles[-1])
                    time.sleep(5)

                    if "dice.com" not in browser.current_url:
                        print("🔗 Redirected to external site. Skipping.")
                        browser.close()
                        browser.switch_to.window(browser.window_handles[0])
                        continue

                    collect_job_info()

                    # Attempt auto-application via Easy Apply
                    try:
                        shadow_host = WebDriverWait(browser, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "apply-button-wc"))
                        )
                        shadow_root = browser.execute_script("return arguments[0].shadowRoot", shadow_host)
                        apply_btn = shadow_root.find_element(By.CSS_SELECTOR, "button.btn.btn-primary")

                        if apply_btn.text.strip().lower() == "easy apply":
                            browser.execute_script("arguments[0].click();", apply_btn)
                            print("🟢 Easy Apply triggered!")

                            # Step through the application
                            next_btn = WebDriverWait(browser, 10).until(
                                EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']"))
                            )
                            next_btn.click()

                            submit_btn = WebDriverWait(browser, 10).until(
                                EC.element_to_be_clickable((By.XPATH, "//span[text()='Submit']"))
                            )
                            submit_btn.click()

                            print("🎉 Application submitted!")
                        else:
                            print("🛑 Apply button is not for Easy Apply. Skipping.")

                    except:
                        print("ℹ️ Application already submitted.")

                    browser.close()
                    browser.switch_to.window(browser.window_handles[0])

                except Exception as err:
                    print(f"⚠️ Skipped a listing due to error: {err}")
                    browser.switch_to.window(browser.window_handles[0])
                    continue

            try:
                next_btn_container = WebDriverWait(browser, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//li[contains(@class, 'pagination-next')]"))
                )
                if "disabled" in next_btn_container.get_attribute("class"):
                    print("📄 No more pages for this city.")
                    break
                next_page_btn = next_btn_container.find_element(By.TAG_NAME, "a")
                browser.execute_script("arguments[0].click();", next_page_btn)
                time.sleep(4)
            except:
                print("⛔ Pagination failed or end reached.")
                break

    except Exception as err:
        print(f"🚨 Error while scraping for {city}: {err}")

# ========== Login Check & Start ==========
browser.get("https://www.dice.com/home-feed")
time.sleep(5)

if "login" in browser.current_url.lower():
    print("🔐 Logging in...")
    try:
        browser.get("https://www.dice.com/dashboard/login")
        WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, "email"))).send_keys(USER_EMAIL)
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()
        WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, "password"))).send_keys(USER_PASSWORD)
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()
        WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/dashboard')]")))
        print("✅ Logged in successfully.")
    except Exception as err:
        print(f"❌ Login failed: {err}")
else:
    print("✅ Already logged in.")

# ========== Start the Scraper ==========
cities_to_check = ["New York", "Boston", "Irving"] # Add more cities as needed
for city in cities_to_check:
    scrape_jobs_for_city(city)

# ========== Save Collected Data ==========
export_to_excel()

# ========== Trigger Auto Email Script ==========
print("📬 Launching email automation...")
AutoEmailScript.send_emails()

# ========== Wrap Up ==========
print("🏁 All tasks finished. Closing browser.")
browser.quit()
