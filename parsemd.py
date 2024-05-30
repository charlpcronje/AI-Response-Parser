# project_parser.py
# 1.0.0

import os
import json
import argparse
from datetime import datetime

# Constants
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(SCRIPT_DIR, "project_parser.log")
SETTINGS_FILE = os.path.join(SCRIPT_DIR, ".env")
HISTORY_FILE = os.path.join(SCRIPT_DIR, "run_history.json")
UNKNOWN_FOLDER = "__unknown__"
INDEX_FILE = "index.md"

# Logger class


class Logger:
    def __init__(self, log_file):
        self.log_file = log_file

    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - {message}"
        print(log_entry)
        with open(self.log_file, "a") as file:
            file.write(log_entry + "\n")

# Load settings from .env file


def load_settings():
    settings = {}
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            for line in file:
                key, value = line.strip().split("=")
                settings[key] = value
    return settings

# Save run history to JSON file


def save_run_history(run_history):
    with open(HISTORY_FILE, "w") as file:
        json.dump(run_history, file, indent=4)

# Load run history from JSON file


def load_run_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as file:
            return json.load(file)
    return []

# Rest of the script code remains the same

# Main function


def main():
    logger = Logger(LOG_FILE)
    settings = load_settings()
    run_history = load_run_history()

    # Rest of the main function code remains the same


if __name__ == "__main__":
    main()
