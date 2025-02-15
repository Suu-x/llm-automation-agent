import subprocess
import requests
import json
import sqlite3
from datetime import datetime


# 📌 Task A1: Install uv (if required) and run datagen.py
def install_uv_and_run_datagen(user_email: str):
    """Install uv (if required) and run datagen.py with user email"""
    subprocess.run(["pip", "install", "uv"], check=True)

    url = "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"
    response = requests.get(url)

    if response.status_code == 200:
        with open("datagen.py", "wb") as f:
            f.write(response.content)
        subprocess.run(["python", "datagen.py", user_email], check=True)
        return "✅ Data generation complete."
    return "❌ Failed to download datagen.py."

# 📌 Task A3: Count the number of Wednesdays
def count_wednesdays():
    """Count the number of Wednesdays in /data/dates.txt"""
    with open("data/dates.txt", "r") as f:
        dates = [datetime.strptime(line.strip(), "%Y-%m-%d") for line in f]
    
    wednesday_count = sum(1 for date in dates if date.weekday() == 2)

    with open("data/dates-wednesdays.txt", "w") as f:
        f.write(str(wednesday_count))
    
    return f"✅ Counted {wednesday_count} Wednesdays."

# 📌 Task A4: Sort contacts by last_name, then first_name
def sort_contacts():
    """Sort contacts.json by last_name, then first_name"""
    with open("data/contacts.json", "r") as f:
        contacts = json.load(f)

    contacts.sort(key=lambda c: (c["last_name"], c["first_name"]))

    with open("data/contacts-sorted.json", "w") as f:
        json.dump(contacts, f, indent=2)

    return "✅ Contacts sorted."

