# utils/csv_reader.py
# Helper utility to read test data from CSV file.

import csv
import os

def read_login_data():
    """Reads username, password, and expected_result from CSV file."""
    data = []
    file_path = "test_data/login_data.csv"
    
    if os.path.exists(file_path):
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append((row["username"], row["password"], row["expected_result"]))
    return data
