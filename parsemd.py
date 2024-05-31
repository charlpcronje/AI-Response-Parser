# parsemd.py
# 1.0.0

import os
import json
import shutil
from datetime import datetime

# Constants
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(SCRIPT_DIR, "parsemd.log")
SETTINGS_FILE = os.path.join(SCRIPT_DIR, ".env")
HISTORY_FILE = os.path.join(SCRIPT_DIR, "run_history.json")
UNKNOWN_FOLDER = "__unknown__"
INDEX_FILE = "index.md"
OUTPUT_FILE = "output.md"
BASH_SCRIPT = "delete_files.sh"


class Logger:
    """
    A logger class for logging messages to a file and console.
    """

    def __init__(self, log_file):
        self.log_file = log_file

    def log(self, message):
        """
        Logs a message to the log file and console with a timestamp.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - {message}"
        print(log_entry)
        with open(self.log_file, "a") as file:
            file.write(log_entry + "\n")


logger = Logger(LOG_FILE)


def load_settings():
    """
    Loads settings from the .env file.
    """
    settings = {}
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            for line in file:
                key, value = line.strip().split("=")
                settings[key] = value
    return settings


def save_run_history(run_history):
    """
    Saves the run history to the run_history.json file.
    """
    with open(HISTORY_FILE, "w") as file:
        json.dump(run_history, file, indent=4)


def load_run_history():
    """
    Loads the run history from the run_history.json file.
    """
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as file:
            return json.load(file)
    return []


def get_user_input():
    """
    Prompts the user to enter the input and output paths.
    """
    input_path = input("Enter the input path: ")
    output_path = input("Enter the output path: ")
    return input_path, output_path


def zip_output_folder(output_path):
    """
    Zips the output folder with the current date and time as the zip file name.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_file_name = f"{timestamp}.zip"
    zip_file_path = os.path.join(os.path.dirname(output_path), zip_file_name)
    shutil.make_archive(zip_file_path[:-4], "zip", output_path)
    logger.log(f"Output folder zipped: {zip_file_path}")


def create_bash_script(output_path, created_files):
    """
    Creates a bash script with commands to delete the created files.
    """
    bash_script_path = os.path.join(output_path, BASH_SCRIPT)
    with open(bash_script_path, "w") as file:
        file.write("#!/bin/bash\n\n")
        for file_path in created_files:
            file.write(f"rm -rf {file_path}\n")
    logger.log(f"Bash script created: {bash_script_path}")


def parse_markdown(input_path, output_path, logger):
    """
    Parses the markdown file and creates output files based on the code blocks.
    """
    # Open the input file and read its content
    with open(input_path, "r") as file:
        content = file.read()

    # Initialize variables to hold the new content, flags, and blocks
    new_content = ""
    lines = content.split("\n")
    in_code_block = False
    in_markdown_block = False
    in_doc_block = False
    current_block = []
    created_files = []
    last_line = ""

    # Iterate over each line in the text
    for line in lines:
        # Check if the line starts with ```
        if line.startswith("```"):
            # If in_markdown_block is True, append the line to the current_block
            if in_markdown_block:
                current_block.append(line)
            # If in_code_block is True
            elif in_code_block:
                # Check if the last line in current_block is empty and remove it if so
                if not current_block[-1].strip():
                    current_block.pop()
                # If the last line and current block are not comments or headers, add a warning
                if last_line and not current_block[0].startswith("#") and not current_block[0].startswith("//") and not current_block[0].startswith("<!--"):
                    current_block.insert(0, "# WARNING: CODE BLOCKS APPENDED")
                    current_block.insert(0, last_line)
                    last_line = ""
                # Join the current block to form the code block
                code_block = "\n".join(current_block)
                # Process the code block and create the corresponding file
                file_path = process_code_block(code_block, output_path, logger)
                if file_path:
                    created_files.append(file_path)
                    new_content += f"[{os.path.basename(file_path)}]({file_path})\n\n"
                else:
                    new_content += f"```\n{code_block}\n```\n\n"
                # Reset current_block and in_code_block flag
                current_block = []
                in_code_block = False
            # If in_code_block is False, set in_code_block to True
            else:
                in_code_block = True
        # Check if the line starts with """ or contains """
        elif line.startswith("\"\"\"") or "\"\"\"" in line:
            # If in_doc_block is True, set in_doc_block to False
            if in_doc_block:
                in_doc_block = False
            # If in_doc_block is False, set in_doc_block to True
            else:
                in_doc_block = True
            # Append the line to the current_block
            current_block.append(line)
        # If in_code_block is True and in_doc_block is False
        else:
            if in_code_block and not in_doc_block:
                # Check if the line starts with #, //, or <!--
                if line.startswith("#") or line.startswith("//") or line.startswith("<!--"):
                    # Extract the relative path from the line
                    relative_path = line.strip(
                        "# /").strip().strip("-->").strip()
                    # If the relative path ends with .md, set in_markdown_block to True
                    if relative_path.endswith(".md"):
                        in_markdown_block = True
                # Append the line to the current_block
                current_block.append(line)
            # If in_markdown_block or in_doc_block is True, append the line to the current_block
            elif in_markdown_block or in_doc_block:
                current_block.append(line)
            # If not in_code_block, append the line to new_content
            else:
                new_content += line + "\n"

        # If in_code_block and not a code delimiter, set last_line to the current line
        if in_code_block and not line.startswith("```"):
            last_line = line

    # If there is any remaining content in current_block, process it as a code block
    if current_block:
        code_block = "\n".join(current_block)
        file_path = process_code_block(code_block, output_path, logger)
        if file_path:
            created_files.append(file_path)
            new_content += f"[{os.path.basename(file_path)}]({file_path})\n\n"
        else:
            new_content += f"```\n{code_block}\n```\n\n"

    # Write the new_content to the output markdown file
    output_file_path = os.path.join(output_path, OUTPUT_FILE)
    with open(output_file_path, "w") as file:
        file.write(new_content.strip())
    logger.log(f"Output markdown file created: {output_file_path}")

    # Create index.md with tree output
    tree_output = os.popen(f"tree {output_path}").read()
    index_path = os.path.join(output_path, INDEX_FILE)
    with open(index_path, "w") as file:
        file.write(f"# Output Index\n```\n{tree_output}\n```\n")
    logger.log(f"Index file created: {index_path}")

    # Create bash script to delete created files
    create_bash_script(output_path, created_files)

    return created_files


def process_code_block(code_block, output_path, logger):
    """
    Processes a code block and creates the corresponding file.
    """
    lines = code_block.split("\n")
    relative_path = None
    file_content = []

    # Iterate over each line in the code block
    for line in lines:
        # Check if the line starts with #, //, or <!--
        if line.startswith("#") or line.startswith("//") or line.startswith("<!--"):
            # Extract the relative path from the line
            relative_path = line.strip("# /").strip().strip("-->").strip()
        else:
            file_content.append(line)

    if relative_path:
        file_path = os.path.join(output_path, relative_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if os.path.exists(file_path):
            file_name, ext = os.path.splitext(file_path)
            counter = 1
            while os.path.exists(f"{file_name}_{counter}{ext}"):
                counter += 1
            file_path = f"{file_name}_{counter}{ext}"
        with open(file_path, "w") as file:
            file.write("\n".join(file_content))
        logger.log(f"Created file: {file_path}")
        return file_path
    else:
        return None


def main():
    """
    The main function of the script.
    """
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

    # Check if the output folder already exists
    if os.path.exists(output_path):
        zip_output_folder(output_path)

    created_files = parse_markdown(input_path, output_path, logger)

    run_history.append({"input_path": input_path, "output_path": output_path})
    save_run_history(run_history)


if __name__ == "__main__":
    main()
