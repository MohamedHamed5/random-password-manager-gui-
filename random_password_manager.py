

# Project Name: random Password Manager (No GUI)
# By: Al-Arif Team
# Date: 1/5/2025

import string
import random
from pathlib import Path
import os

print("**In our program, we generate randomly suggested passwords for each user, consisting of 10 to 17 characters that include letters, numbers, and symbols. These passwords are valid for use on your online accounts in any website.**")

def generate_passwords():
    number = int(input("Enter the size of chars (10 to 17): "))
    if 17 >= number >= 10:
        chars = string.ascii_letters + string.digits + string.punctuation
        password = "".join(random.choices(chars, k=number))
        return password
    else:
        return None

file_path = Path("D:/PDFs/1st/python/random password manager/passwords.txt")

if not file_path.exists():
    with open(file_path, "w") as file:
        file.write("Website | Username | Password\n")
        print("📁 A new password file has been created.")
else:
    print("📁 Existing password file found, data will be preserved.")


while True:
    print("\n🔐 New Password Entry:")
    
    site = input("Enter the name of the website (or type 'exit' to stop): ")
    if site.lower() == "exit":
        print("👋 Exiting the password manager.")
        break
    
    user_name = input("Enter the username: ")
    password = generate_passwords()
    
    if password:
        with open(file_path, "a") as file:
            file.write(f"{site} | {user_name} | {password}\n")
        
        print("\n✅ Password saved successfully!\n📄 Current saved passwords:\n")
        with open(file_path, "r") as file:
            content = file.read()
            print(content)

        os.startfile(file_path)
    else:
        print("❌ Only the correct input from (10 to 17) is allowed. Please try again.")



