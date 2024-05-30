# project_parser.py
# 1.0.0

import os
import json
import argparse
from datetime import datetime

# Constants
LOG_FILE = "project_parser.log"
SETTINGS_FILE = ".env"
HISTORY_FILE = "run_history.json"
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

# Get user input for input and output paths


def get_user_input():
    input_path = input("Enter the input path: ")
    output_path = input("Enter the output path: ")
    return input_path, output_path

# Parse markdown file and create output files


def parse_markdown(input_path, output_path, logger):
    with open(input_path, "r") as file:
        content = file.read()

    code_blocks = []
    lines = content.split("\n")
    in_code_block = False
    current_block = []

    for line in lines:
        if line.startswith("```"):
            if in_code_block:
                code_blocks.append("\n".join(current_block))
                current_block = []
            else:
                current_block = []
            in_code_block = not in_code_block
        else:
            if in_code_block:
                current_block.append(line)

    if in_code_block:
        code_blocks.append("\n".join(current_block))

    for code_block in code_blocks:
        lines = code_block.split("\n")
        relative_path = None
        for line in lines:
            if line.startswith("#") or line.startswith("//") or line.startswith("<!--"):
                relative_path = line.strip("# /").strip().strip("-->").strip()
                break

        if relative_path:
            file_path = os.path.join(output_path, relative_path)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            version = "1.0.0"
            if os.path.exists(file_path):
                file_name, ext = os.path.splitext(file_path)
                counter = 1
                while os.path.exists(f"{file_name}_{counter}{ext}"):
                    counter += 1
                file_path = f"{file_name}_{counter}{ext}"
            with open(file_path, "w") as file:
                file.write(f"# {relative_path}\n")
                file.write(f"# {version}\n")
                file.write(code_block)
            logger.log(f"Created file: {file_path}")
        else:
            unknown_folder = os.path.join(output_path, UNKNOWN_FOLDER)
            os.makedirs(unknown_folder, exist_ok=True)
            counter = 1
            while os.path.exists(os.path.join(unknown_folder, f"unknown_{counter}.md")):
                counter += 1
            file_path = os.path.join(unknown_folder, f"unknown_{counter}.md")
            with open(file_path, "w") as file:
                file.write(code_block)
            logger.log(f"Created file: {file_path}")

    # Create index.md with tree output
    tree_output = os.popen(f"tree {output_path}").read()
    index_path = os.path.join(output_path, INDEX_FILE)
    with open(index_path, "w") as file:
        file.write(f"# Output Index\n```\n{tree_output}\n```\n")
    logger.log(f"Created index file: {index_path}")

# Main function


def main():
    logger = Logger(LOG_FILE)
    settings = load_settings()
    run_history = load_run_history()

    if len(run_history) > 0:
        print("Recent runs:")
        for i, run in enumerate(run_history[-20:], start=1):
            print(
                f"{i}. Input Path: {run['input_path']}, Output Path: {run['output_path']}")
        print(f"{len(run_history[-20:]) + 1}. New run")

        choice = input(
            "Enter the number of the run you want to execute (or press Enter for a new run): ")
        if choice.isdigit() and 1 <= int(choice) <= len(run_history[-20:]):
            selected_run = run_history[-20:][int(choice) - 1]
            input_path = selected_run["input_path"]
            output_path = selected_run["output_path"]
        else:
            input_path, output_path = get_user_input()
    else:
        input_path, output_path = get_user_input()

    logger.log(f"Input Path: {input_path}")
    logger.log(f"Output Path: {output_path}")

    parse_markdown(input_path, output_path, logger)

    run_history.append({"input_path": input_path, "output_path": output_path})
    save_run_history(run_history)


if __name__ == "__main__":
    main()
