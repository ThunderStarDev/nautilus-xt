#  ▗▖  ▗▖ ▗▄▖ ▗▖ ▗▖▗▄▄▄▖▗▄▄▄▖▗▖   ▗▖ ▗▖ ▗▄▄▖    ▗▖  ▗▖▗▄▄▄▖
#  ▐▛▚▖▐▌▐▌ ▐▌▐▌ ▐▌  █    █  ▐▌   ▐▌ ▐▌▐▌        ▝▚▞▘   █  
#  ▐▌ ▝▜▌▐▛▀▜▌▐▌ ▐▌  █    █  ▐▌   ▐▌ ▐▌ ▝▀▚▖      ▐▌    █  
#  ▐▌  ▐▌▐▌ ▐▌▝▚▄▞▘  █  ▗▄█▄▖▐▙▄▄▖▝▚▄▞▘▗▄▄▞▘    ▗▞▘▝▚▖  █  
#
# By ThunderStar, version 07.25 
# visit https://github.com/ThunderStarDev
# This project is licensed under the Apache License, Version 2.0

import hashlib
import string
import random  
import customtkinter as ctk
from tkinter import messagebox
from pathlib import Path
import json
import os
import platform
from PIL import Image, ImageTk

# Attempt to load required files
def load_file_content(filepath, default_value=""):
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        messagebox.showerror("Error", f"Missing required file: {filepath}")
        return default_value

# Load BIP39 wordlist
BIP39_WORDLIST_PATH = Path("bip39_wordlist.txt")
if BIP39_WORDLIST_PATH.exists():
    with open(BIP39_WORDLIST_PATH, "r") as f:
        BIP39_WORDLIST = f.read().splitlines()
else:
    BIP39_WORDLIST = []
    messagebox.showerror("Error", "Missing BIP39 wordlist file")

# Load mask and seed phrase
hidden = load_file_content("mask.txt", "*") # Symbol that hides text
SEEDPHRASE = load_file_content("SEED.txt")  # Password = Passphrase + Account + SEED.txt

# Password generation (random letters)
def generate_password_symbols(master_password, service_name, length):
    combined_string = (master_password + service_name + SEEDPHRASE).upper() # all input characters (including SEED) are UPPERCASE
    hashed_string = hashlib.sha256(combined_string.encode()).hexdigest()

    seed = int(hashed_string[:16], 16)
    rng = random.Random(seed)

    special_characters = '!#$%*()-=_+.?'  # additional characters for extra security.
    valid_characters = string.ascii_letters + string.digits + special_characters

    password = ''.join(rng.choice(valid_characters) for _ in range(length))
    return password

# Password generation from mnemonic words
def generate_password_mnemonic(master_password, service_name, word_count):
    if not BIP39_WORDLIST:
        messagebox.showerror("Error", "BIP39 wordlist not loaded.")
        return ""

    combined_string = (master_password + service_name + SEEDPHRASE).upper()
    hashed_string = hashlib.sha256(combined_string.encode()).hexdigest()

    seed = int(hashed_string[:16], 16)
    rng = random.Random(seed)

    password_words = [rng.choice(BIP39_WORDLIST) for _ in range(word_count)]
    return ' '.join(password_words)

# Generate and display password
def generate_and_show_password():
    master_password = master_password_entry.get()
    service_name = service_name_entry.get()

    if mode_var.get() == "symbols":
        if length_entry.get().isdigit() or length_entry.get() == '':
            password_length = int(length_entry.get() or 12)
            generated_password = generate_password_symbols(master_password, service_name, password_length)
        else:
            messagebox.showwarning("Oops!", "Password length is wrong")
            return
    else:
        if length_entry.get().isdigit() or length_entry.get() == '':
            word_count = int(length_entry.get() or 5)
            generated_password = generate_password_mnemonic(master_password, service_name, word_count)
        else:
            messagebox.showwarning("Oops!", "The number of words is wrong")
            return

    password_display.configure(state="normal")
    password_display.delete("1.0", "end")
    password_display.insert("end", generated_password)
    password_display.configure(state="disabled")
    
# Toggle mode between symbols and mnemonic
def toggle_mode():
    mode_var.set("mnemonic" if mode_var.get() == "symbols" else "symbols")
    generate_button.configure(text="Generate mnemonic" if mode_var.get() == "mnemonic" else "Generate password")
    generate_and_show_password()

# Toggle password visibility
def toggle_password_visibility():
    master_password_entry.configure(show="" if show_password_var.get() else hidden)

# Clear all fields
def clear_fields():
    master_password_entry.delete(0, "end")
    service_name_entry.delete(0, "end")
    length_entry.delete(0, "end")
    password_display.configure(state="normal")
    password_display.delete("1.0", "end")
    password_display.configure(state="disabled")

# Main window setup
root = ctk.CTk()
root.title("Nautilus XT")
root.geometry("322x318") 
root.resizable(False, False)

icon_path_ico = os.path.join(os.path.dirname(__file__), "nautilus_xt_512.ico") # Windows
icon_path_png = os.path.join(os.path.dirname(__file__), "nautilus_xt.png") # Linux / Mac OS

if platform.system() == "Windows":
    if os.path.exists(icon_path_ico):
        root.iconbitmap(icon_path_ico)
else:
    if os.path.exists(icon_path_png):
        icon_image = ImageTk.PhotoImage(Image.open(icon_path_png))
        root.iconphoto(True, icon_image)

always_on_top_var = ctk.BooleanVar(value=False)

def toggle_always_on_top():
    always_on_top_state = always_on_top_var.get()
    root.attributes('-topmost', always_on_top_state)

def save_theme_state():
    theme_state = {
        "appearance_mode": ctk.get_appearance_mode().lower()  # Get the current theme
    }
    
    with open("theme_state.json", "w") as f:
        json.dump(theme_state, f)

def load_theme_state():
    try:
        with open("theme_state.json", "r") as f:
            theme_state = json.load(f)
            return theme_state.get("appearance_mode", "dark")
    except FileNotFoundError:
        return "dark"

def toggle_theme():
    current_theme = ctk.get_appearance_mode().lower()
    new_theme = "dark" if current_theme == "light" else "light"
    ctk.set_appearance_mode(new_theme)
    update_colors()
    save_theme_state()

dark_theme_colors = {
    "button_color": "#173745",
    "border_color": "#166079",
    "hover_color": "#124f63",
    
    "checkbox_fg_color": "#173745",
    "checkbox_border_color": "#166079",
    "checkbox_hover_color": "#124f63",
    "checkbox_checkmark_color": "#FFFFFF"
}

light_theme_colors = {
    "button_color": "#8bc2d9",
    "border_color": "#16607a",
    "hover_color": "#32b2dc",
    
    "checkbox_fg_color": "#8bc2d9",
    "checkbox_border_color": "#16607a",
    "checkbox_hover_color": "#32b2dc",
    "checkbox_checkmark_color": "#000000"
}

def create_embossed_button(text, command, button_color, border_color, hover_color, **kwargs):
    return ctk.CTkButton(
        root, text=text, command=command, 
        fg_color=button_color, corner_radius=7,
        border_color=border_color, hover_color=hover_color, border_width=3
    )


def update_colors():
    theme_colors = dark_theme_colors if ctk.get_appearance_mode().lower() == "dark" else light_theme_colors

    for button in [generate_button, toggle_button, clear_button, theme_button]:
        button.configure(
            fg_color=theme_colors["button_color"],
            border_color=theme_colors["border_color"],
            hover_color=theme_colors["hover_color"]
        )
    
    if ctk.get_appearance_mode().lower() == "dark":
        generate_button.configure(text="Generate password", text_color="white")
        toggle_button.configure(text="Switch mode", text_color="white")
        clear_button.configure(text="Clear", text_color="white")
        theme_button.configure(text="Toggle theme", text_color="white")
    else:
        generate_button.configure(text="Generate password", text_color="black")
        toggle_button.configure(text="Switch mode", text_color="black")
        clear_button.configure(text="Clear", text_color="black")
        theme_button.configure(text="Toggle theme", text_color="black")


    for checkbox in [show_password_checkbox, always_on_top_checkbox]:
        checkbox.configure(
            fg_color=theme_colors["checkbox_fg_color"],
            checkmark_color=theme_colors["checkbox_checkmark_color"],
            hover_color=theme_colors["checkbox_hover_color"],
            border_color=theme_colors["checkbox_border_color"]
        )

# Ctrl + A
def select_all_text(event):
    password_display.tag_add("sel", "1.0", "end")
    return "break" 

# Interface elements
ctk.CTkLabel(root, text="Passphrase:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
ctk.CTkLabel(root, text="Account:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
ctk.CTkLabel(root, text="Length:").grid(row=2, column=0, sticky="w", padx=10, pady=5)

master_password_entry = ctk.CTkEntry(root, show=hidden, border_color="#565B5E")
service_name_entry = ctk.CTkEntry(root, border_color="#565B5E")
length_entry = ctk.CTkEntry(root, border_color="#565B5E")

password_display = ctk.CTkTextbox(root, height=30, width=300, state="normal", border_width=2, border_color="#565B5E", corner_radius=8)
password_display.bind("<Control-a>", select_all_text)

password_display.bind("<Command-a>", select_all_text)  # Uh...

# Password generation mode switch
mode_var = ctk.StringVar(value="symbols")
generate_button = create_embossed_button("Generate password", generate_and_show_password, **dark_theme_colors)
toggle_button = create_embossed_button("Switch mode", toggle_mode, **dark_theme_colors)
clear_button = create_embossed_button("Clear", clear_fields, **dark_theme_colors)
theme_button = create_embossed_button("Toggle theme", toggle_theme, **dark_theme_colors)

show_password_var = ctk.BooleanVar()
show_password_checkbox = ctk.CTkCheckBox(
    root, text=" Show passphrase", variable=show_password_var, 
    command=toggle_password_visibility
)

always_on_top_checkbox = ctk.CTkCheckBox(
    root, text="    Always on top    ", variable=always_on_top_var,
    command=toggle_always_on_top
)

initial_theme = load_theme_state()
ctk.set_appearance_mode(initial_theme)

# Place elements
master_password_entry.grid(row=0, column=1, padx=10, pady=5)
service_name_entry.grid(row=1, column=1, padx=10, pady=5)
length_entry.grid(row=2, column=1, padx=10, pady=5)
password_display.grid(row=3, column=0, columnspan=2, pady=10, padx=10)
toggle_button.grid(row=4, column=1, pady=10, padx=10)
generate_button.grid(row=4, column=0, pady=10, padx=10)
clear_button.grid(row=5, column=0, pady=10, padx=10) 
show_password_checkbox.grid(row=5, column=1, pady=10)
always_on_top_checkbox.grid(row=6, column=1, pady=10, padx=10)
theme_button.grid(row=6, column=0, pady=10, padx=10)

update_colors()
root.mainloop()
