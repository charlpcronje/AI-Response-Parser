# AI Response Parser

AI Response Parser is a Python script that parses a markdown file, extracts code blocks, and creates output files based on the specified rules and requirements.

## Features

- Logs all actions taking place to a file and to the terminal
- Modular script design
- Adds the relative file path to the first line of each created file as a comment
- Adds the version number to each file as the second line, starting at 1.0.0
- Stores app settings in a `.env` file
- Provides a list of the last 20 run arguments to choose from if no arguments are supplied
- Prompts for Input Path and Output Path if a new run is selected
- Creates an `index.md` file in the Output Path with the output of the `tree` command

## Usage

1. Make sure you have Python installed on your system.
2. Clone this repository or download the `project_parser.py` script.
3. Open a terminal and navigate to the directory where the script is located.
4. Run the script using the following command:

```bash
python project_parser.py
```

5. If no arguments are supplied, the script will provide a list of the last 20 run arguments to choose from. Enter the corresponding number to select a previous run or choose to start a new run.
6. If you choose a new run or if no previous runs are available, the script will prompt you for the Input Path and Output Path.
7. The script will parse the markdown file, create output files based on the code blocks, and generate an `index.md` file in the Output Path.

## For convenient usage
To create a bash script that allows you to run the `parsemd.py` script from anywhere on Rocky Linux 9.2, follow these steps:

1. Open a terminal and navigate to the `/usr/local/bin` directory:
```sh
cd /usr/local/bin
```

2. Create a new file named `parsemd` using a text editor (e.g., nano or vim):
```sh
sudo nano parsemd
```

3. Add the following content to the `parsemd` file:
```bash
#!/bin/bash
python /var/www/tools/AI\ Response\ Parser/parsemd.py "$@"
```

4. Save the file and exit the text editor. If you're using nano, press `Ctrl+X`, then `Y`, and finally `Enter` to save and exit.

5. Make the `parsemd` script executable:
```sh
sudo chmod +x parsemd
```

6. Verify that the script is accessible from anywhere by running:
```sh
parsemd
```

The `parsemd.py` script should now execute from its own folder.

Now, whenever you type `parsemd` in the terminal from any directory on Rocky Linux 9.2, it will run the `parsemd.py` script located at `/var/www/tools/AI Response Parser/parsemd.py`.

Note: Make sure that the `/usr/local/bin` directory is included in your system's `PATH` variable. You can check this by running `echo $PATH`. If `/usr/local/bin` is not listed, you can add it by modifying your shell's configuration file (e.g., `~/.bashrc` or `~/.bash_profile`) and adding the following line:

```sh
export PATH="/usr/local/bin:$PATH"
```
After adding the line, save the file and restart your terminal or run `source ~/.bashrc` (or the appropriate configuration file) for the changes to take effect.

## Questions

### Will the output path be created if it does not exist?

Yes, the script will create the output path if it does not exist. It uses the `os.makedirs()` function with the `exist_ok=True` parameter to create the necessary directories recursively.

## Roadmap

In the future, we plan to enhance the script to handle duplicate files using Git version control instead of creating numbered files. Here's how it will work:

1. When a duplicate file is detected, the script will check if a Git repository exists in the output folder. If it doesn't exist, a new Git repository will be initialized (assuming Git is already installed on the system).

2. All the files in the output folder will be committed to the Git repository with a commit message of "First Commit".

3. Instead of creating a numbered file for the duplicate, the script will overwrite the existing file with the new content.

4. The modified file will be committed to the Git repository with a commit message stating "{file name} - To be Merged".

5. When you open the file in VSCode or any other Git-enabled editor, you will be notified that the file needs to be merged.

This approach allows for better version control and collaborative editing of the output files. It eliminates the need for creating numbered files and promotes a more streamlined workflow using Git.

Please note that this feature is currently in the roadmap and not yet implemented in the script.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the GitHub repository.

## License

This project is licensed under the [MIT License](LICENSE).