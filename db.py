# db.py
import mysql.connector
from config import DB_CONFIG
from datetime import datetime

def save_query(case_type, case_number, filing_year, raw_response):
    """Saves the query details into the MySQL database."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute("""
            INSERT INTO queries (case_type, case_number, filing_year, timestamp, raw_response)
            VALUES (%s, %s, %s, %s, %s)
        """, (case_type, case_number, filing_year, timestamp, raw_response))

        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Query logged to MySQL successfully.")
    except Exception as e:
        print(f"❌ Database insert error: {e}")
