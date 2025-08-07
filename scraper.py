# scraper.py
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin
from datetime import datetime
import time
import mysql.connector
from db import save_query
from config import DB_CONFIG, COURT_URL

BASE_URL = "https://delhihighcourt.nic.in/"


def fetch_case_details(case_type, case_number, filing_year):
    """Fetches Delhi High Court case details and returns structured data + message."""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(COURT_URL)

    try:
        # ---------------- CAPTCHA ----------------
        captcha_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(@class,'captcha') or contains(@id,'captcha')]"))
        )
        captcha_text = captcha_element.text.strip()

        # ---------------- FORM FILL ----------------
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[contains(@id,'case_type')]"))
        ).send_keys(case_type)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[contains(@id,'case_number')]"))
        ).send_keys(case_number)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[contains(@id,'case_year')]"))
        ).send_keys(filing_year)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[contains(@id,'captcha')]"))
        ).send_keys(captcha_text)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Submit')]"))
        ).click()

        time.sleep(5)
        raw_response = driver.page_source
        soup = BeautifulSoup(raw_response, "html.parser")
        table = soup.find("table")

        if not table or len(table.find_all("tr")) < 2:
            raise Exception("No result or insufficient data found.")

        tds = table.find_all("tr")[1].find_all("td")

        parties_full = tds[2].get_text(" ", strip=True) if len(tds) >= 3 else "Not Found"
        parties = parties_full.upper().split("VS.")[0].strip() if "VS." in parties_full.upper() else parties_full

        listing_text = tds[3].get_text(" ", strip=True) if len(tds) >= 4 else ""
        filing_date, next_hearing = "Not Found", "Not Found"
        for part in listing_text.split():
            if part.count("/") == 2:
                if filing_date == "Not Found":
                    filing_date = part
                else:
                    next_hearing = part

        # ---------------- PDF Search ----------------
        most_recent_pdf = None

        # Method 1: Main table
        for link in tds[1].find_all("a", href=True):
            if ".pdf" in link["href"].lower():
                most_recent_pdf = urljoin(BASE_URL, link["href"])
                break

        # Method 2: Orders tab
        if not most_recent_pdf:
            try:
                orders_link = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.LINK_TEXT, "Orders"))
                )
                driver.execute_script("arguments[0].click();", orders_link)
                time.sleep(3)

                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//table"))
                )

                pdf_links = driver.find_elements(By.XPATH, "//table//tr[position()>1]/td[1]//a[contains(@href, '.pdf')]")

                if pdf_links:
                    most_recent_pdf = urljoin(BASE_URL, pdf_links[0].get_attribute("href"))
            except Exception:
                pass

        # Method 3: Fallback - all links
        if not most_recent_pdf:
            try:
                for link in driver.find_elements(By.TAG_NAME, "a"):
                    href = link.get_attribute("href")
                    if href and ".pdf" in href.lower():
                        most_recent_pdf = urljoin(BASE_URL, href)
                        break
            except:
                pass

        # ---------------- Result ----------------
        result_data = {
            "parties": parties,
            "filing_date": filing_date,
            "next_hearing": next_hearing,
            "pdf_link": most_recent_pdf
        }

        # ---------------- Log Query ----------------
        save_query(case_type, case_number, filing_year, raw_response)

        return result_data, "✅ Case details fetched successfully!"

    except Exception as e:
        return None, f"❌ Error: {str(e)}"
    finally:
        driver.quit()
