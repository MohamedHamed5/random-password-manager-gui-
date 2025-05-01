

# Project Name: random Password Manager With GUI
# By: Mohamed Hamed
# Date: 2/5/2025

import tkinter as tk
from tkinter import messagebox, Listbox, Scrollbar, END, Label, Entry, Button, Frame
import string
import random
from pathlib import Path
import os
import sys

# --- Color Settings --- 
BG_COLOR = "#F0F0F0"  # Light background color
FG_COLOR = "#333333"  # Dark text color
BTN_COLOR = "#4CAF50" # Green button color
BTN_FG_COLOR = "#FFFFFF" # White button text color
ENTRY_BG_COLOR = "#FFFFFF"
LISTBOX_BG_COLOR = "#FFFFFF"
ERROR_COLOR = "#FF0000" # Red color for errors

# Saves the file in the same directory as the script
SCRIPT_DIR = Path(__file__).parent
PASSWORD_FILE = SCRIPT_DIR / "passwords_gui_en.txt"

def generate_password(length):
    """Generate a random password of the specified length."""
    if not (10 <= length <= 17):
        messagebox.showerror("Length Error", f"Length must be between 10 and 17. Entered: {length}")
        return None
    
    chars = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choices(chars, k=length))
    return password

def save_password(site, username, password):
    # Ensure header exists if the file is new or empty
    if not PASSWORD_FILE.exists() or PASSWORD_FILE.stat().st_size == 0:
        with open(PASSWORD_FILE, "w", encoding='utf-8') as file:
            file.write("Website | Username | Password\n")
            file.write("-------- | -------- | --------\n")
            
    with open(PASSWORD_FILE, "a", encoding='utf-8') as file:
        file.write(f"{site} | {username} | {password}\n")
    
    # Update the display list
    load_passwords()

def load_passwords(filter_text=""):
    password_listbox.delete(0, END) 
    if PASSWORD_FILE.exists():
        with open(PASSWORD_FILE, "r", encoding='utf-8') as file:
            lines = file.readlines()
            if len(lines) > 0:
                password_listbox.insert(END, lines[0].strip()) # header
            if len(lines) > 1:
                password_listbox.insert(END, lines[1].strip()) # separator
            for line in lines[2:]:
                try:
                    parts = line.strip().split(" | ")
                    if len(parts) == 3:
                        website, username, _ = parts
                        display_line = f"{website} | {username} | *****"
                        if filter_text.lower() in display_line.lower():
                            password_listbox.insert(END, display_line)
                    else:
                        if filter_text.lower() in line.lower():
                            password_listbox.insert(END, line.strip())
                except Exception:
                    password_listbox.insert(END, line.strip())

def handle_generate_save():
    site = site_entry.get()
    username = username_entry.get()
    
    try:
        length = int(length_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid integer for password length (between 10 and 17).")
        return

    if not site or not username:
        messagebox.showwarning("Missing Data", "Please enter both Website and Username.")
        return

    password = generate_password(length)
    
    if password:
        password_display_entry.config(state='normal')
        password_display_entry.delete(0, END)
        password_display_entry.insert(0, password)
        password_display_entry.config(state='readonly')
        
        save_password(site, username, password)
        site_entry.delete(0, END)
        username_entry.delete(0, END)
        
        messagebox.showinfo("Success", "Password generated and saved successfully!")

def open_password_file():
    if PASSWORD_FILE.exists():
        try:
            if os.name == 'nt':
                os.startfile(PASSWORD_FILE)
            elif os.name == 'posix':
                if sys.platform == 'darwin':
                    os.system(f'open "{PASSWORD_FILE}"')
                else:
                    os.system(f'xdg-open "{PASSWORD_FILE}"')
            else:
                messagebox.showinfo("Information", f"Cannot automatically open the file on this system. Path: {PASSWORD_FILE}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open the file: {e}")
    else:
        messagebox.showwarning("File Not Found", "Password file not found.")

def confirm_exit():
    if messagebox.askokcancel("Exit Confirmation", "Are you sure you want to exit?"):
        window.quit()

def search_passwords(*args):
    filter_text = search_var.get()
    load_passwords(filter_text)

# --- Main Window Setup --- 
window = tk.Tk()
window.title("Simple Password Manager")
window.config(bg=BG_COLOR, padx=20, pady=20)
window.resizable(False, False)

# --- Frames --- 
input_frame = Frame(window, bg=BG_COLOR)
input_frame.grid(row=0, column=0, pady=10, sticky="ew")

display_frame = Frame(window, bg=BG_COLOR)
display_frame.grid(row=1, column=0, pady=10, sticky="ew")

list_frame = Frame(window, bg=BG_COLOR)
list_frame.grid(row=2, column=0, pady=10, sticky="nsew")

button_frame = Frame(window, bg=BG_COLOR)
button_frame.grid(row=3, column=0, pady=10, sticky="ew")

window.grid_rowconfigure(2, weight=1)
window.grid_columnconfigure(0, weight=1)

# --- Input Frame Widgets --- 
site_label = Label(input_frame, text="Website:", bg=BG_COLOR, fg=FG_COLOR)
site_label.grid(row=0, column=0, padx=5, pady=5, sticky="w") 
site_entry = Entry(input_frame, width=35, bg=ENTRY_BG_COLOR, fg=FG_COLOR, justify='left') 
site_entry.grid(row=0, column=1, padx=5, pady=5) 
site_entry.focus()

username_label = Label(input_frame, text="Username:", bg=BG_COLOR, fg=FG_COLOR)
username_label.grid(row=1, column=0, padx=5, pady=5, sticky="w") 
username_entry = Entry(input_frame, width=35, bg=ENTRY_BG_COLOR, fg=FG_COLOR, justify='left')
username_entry.grid(row=1, column=1, padx=5, pady=5)

length_label = Label(input_frame, text="Password Length (10-17):", bg=BG_COLOR, fg=FG_COLOR)
length_label.grid(row=2, column=0, padx=5, pady=5, sticky="w") 
length_entry = Entry(input_frame, width=10, bg=ENTRY_BG_COLOR, fg=FG_COLOR, justify='left') 
length_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w") 
length_entry.insert(0, "12") 

# --- Display Frame Widgets --- 
password_display_label = Label(display_frame, text="Generated Password:", bg=BG_COLOR, fg=FG_COLOR)
password_display_label.grid(row=0, column=0, padx=5, pady=5, sticky="w") 
password_display_entry = Entry(display_frame, width=35, bg=ENTRY_BG_COLOR, fg=FG_COLOR, state='readonly', justify='left') 
password_display_entry.grid(row=0, column=1, padx=5, pady=5) 

# --- List Frame Widgets --- 
list_label = Label(list_frame, text="Saved Passwords:", bg=BG_COLOR, fg=FG_COLOR)
list_label.pack(pady=(0,5))

# Search box
search_var = tk.StringVar()
search_entry = Entry(list_frame, textvariable=search_var, width=40, bg=ENTRY_BG_COLOR, fg=FG_COLOR)
search_entry.pack(pady=(0, 5))
search_entry.insert(0, "Search...")

scrollbar_y = Scrollbar(list_frame, orient="vertical")
scrollbar_x = Scrollbar(list_frame, orient="horizontal") 
password_listbox = Listbox(list_frame, height=10, width=50, bg=LISTBOX_BG_COLOR, fg=FG_COLOR, 
                           yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set, justify='left') 
scrollbar_y.config(command=password_listbox.yview)
scrollbar_x.config(command=password_listbox.xview)

scrollbar_y.pack(side="right", fill="y") 
scrollbar_x.pack(side="bottom", fill="x")
password_listbox.pack(side="left", fill="both", expand=True)

# Link search input to update function
search_var.trace_add("write", search_passwords)

# --- Button Frame Widgets --- 
generate_button = Button(button_frame, text="Generate & Save Password", width=25, bg=BTN_COLOR, fg=BTN_FG_COLOR, command=handle_generate_save)
generate_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

open_file_button = Button(button_frame, text="Open Passwords File", width=20, command=open_password_file)
open_file_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

exit_button = Button(button_frame, text="Exit", width=10, command=confirm_exit)
exit_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

button_frame.grid_columnconfigure(0, weight=2)
button_frame.grid_columnconfigure(1, weight=1)
button_frame.grid_columnconfigure(2, weight=1)

# --- Load Data and Start App ---
load_passwords()
window.mainloop()
