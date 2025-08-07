# 🧾  “Court-Data Fetcher & Mini-Dashboard”

A lightweight web app that lets users search Delhi High Court case details by case type, number and year, then displays metadata and recent orders/judgments.

---

## 🏛️ Target Court

- ✅ **Delhi High Court**
- 📍 https://delhihighcourt.nic.in/

---

## 🚀 Features

- 🔍 Search by **Case Type**, **Case Number**, and **Filing Year**
- 📄 Displays:
  - **Parties involved**
  - **Filing date**
  - **Next hearing date**
- 📥 Download latest **PDF Order/Judgment**
- 🧠 Automatically handles **CAPTCHA**
- 🗂️ Logs each query with raw HTML in **MySQL**
- ✅ Clean and minimal **Streamlit UI**

---

## 💻 Tech Stack

| Layer      | Technology         |
|------------|--------------------|
| Frontend   | Streamlit          |
| Backend    | Python + Selenium  |
| Database   | MySQL              |
| Config     | `.env` for secrets |
| Parsing    | BeautifulSoup      |

---

## 🔒 CAPTCHA Strategy

The Delhi High Court website uses a **numeric text-based CAPTCHA**.  
This project **automatically bypasses it** legally:

### ✅ How it works:
- Uses Selenium to detect the CAPTCHA `<span>` element:
  ```python
  captcha_element = WebDriverWait(driver, 20).until(
      EC.presence_of_element_located(
          (By.XPATH, "//span[contains(@class,'captcha') or contains(@id,'captcha')]")
      )
  )
  captcha_text = captcha_element.text.strip()
  driver.find_element(By.XPATH, "//input[contains(@id,'captcha')]").send_keys(captcha_text)
  ```

* No manual input or OCR is needed.
* If the CAPTCHA becomes image-based, fallback strategies include:
- OCR with Tesseract
- Manual user input
- Court-provided API (if available)

---

## 🔧 Setup Instructions
Prerequisites
- Python 3.8+
- Chrome browser
- MySQL installed and running

1. Clone the Repository
```bash
git clone https://github.com/DivyanshiRw/Court-Data-Fetcher.git
cd court_data_fetcher
```

Create a Virtual Environment

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```
Linux / Mac:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install Dependencies
```bash
pip install -r requirements.txt
``` 

3. Create .env File
Create a .env file in the root folder with your DB credentials:

```ini
DB_HOST=localhost
DB_USER=youruser
DB_PASSWORD=yourpassword
DB_NAME=yourdatabase
```

4. Setup MySQL Database

Create a Database and Table
```sql
CREATE DATABASE court_data;
USE court_data;

CREATE TABLE queries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    case_type VARCHAR(50),
    case_number VARCHAR(50),
    filing_year VARCHAR(10),
    timestamp DATETIME,
    raw_response LONGTEXT
); 
```

5. Run the App
```bash
streamlit run app.py
```
---

## 🗃️ Data Logging

Each query is logged in the MySQL queries table with:
```ini
Field	         Description
case_type	     Case type
case_number	     Entered case number
filing_year	     Year of filing
timestamp	     When the query was made
raw_response	 Raw HTML of court response
```
---
## 📝 License

This project is licensed under the [MIT License](./LICENSE).

