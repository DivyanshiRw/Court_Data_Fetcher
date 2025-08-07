# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# -------------------------------#
# MySQL Database Configuration
# -------------------------------#
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

# -------------------------------#
# Court URL + App Settings
# -------------------------------#
COURT_URL = os.getenv("COURT_URL", "https://delhihighcourt.nic.in/app/get-case-type-status")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
