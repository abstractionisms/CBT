import tkinter as tk
import os
from tkinter import simpledialog, messagebox, filedialog, font
import datetime
import random
from journal_core import analyze_sentiment, encrypt_message, decrypt_message, save_path # Import necessary functions
from prompts_data import prompts

root = tk.Tk()
root.title("Character Building")

# Configure resizing behavior
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Prompt Selection
def get_random_prompt(prompt_dict):
    category = random.choice(list(prompt_dict.keys()))
    prompt = random.choice(prompt_dict[category])
    return prompt

def change_prompt():
    new_prompt = get_random_prompt(prompts)
    prompt_label.config(text=new_prompt)

# Font customization
font_family = tk.StringVar(root)
font_family.set("Calibri")  # Default font
font_size = tk.IntVar(root)
font_size.set(12)  # Default size

text_box = tk.Text(root, width=50, height=10, wrap=tk.WORD, font=(font_family.get(), font_size.get()))
text_box.grid(row=0, column=1, sticky='nsew')

prompt_label = tk.Label(root, text=get_random_prompt(prompts), wraplength=500)
prompt_label.grid(row=1, column=1, sticky='nsew')

change_prompt_button = tk.Button(root, text="Change Prompt", command=change_prompt)
change_prompt_button.grid(row=2, column=0, padx=5, pady=5, sticky='ew')

font_family_menu = tk.OptionMenu(root, font_family, "Calibri", "Arial", "Times", "Courier")
font_family_menu.grid(row=2, column=1, padx=5, pady=5, sticky='ew')

font_size_menu = tk.OptionMenu(root, font_size, 10, 12, 14, 16, 18)
font_size_menu.grid(row=2, column=2, padx=5, pady=5, sticky='ew')

def update_font():
    text_box.config(font=(font_family.get(), font_size.get()))

update_font_button = tk.Button(root, text="Update Font", command=update_font)
update_font_button.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky='ew')

def count_chars(event):
    s = text_box.get("1.0", 'end-1c')
    words = len(s.split())
    label.config(text = "Characters: " + str(len(s)) + " Words: " + str(words))
    if len(s) >= 1500:
        save_button.grid(row=4, column=0, columnspan=2)
    else:
        save_button.grid_remove()
    if len(s) % 10 == 0:
        canvas.coords(rectangle, 0, 500, 20, 500 - min(len(s)*500/1500, 500))

text_box.bind('<KeyRelease>', count_chars)

canvas = tk.Canvas(root, width=20, height=500)
canvas.grid(row=0, column=2, sticky='ns')
rectangle = canvas.create_rectangle(0, 500, 20, 500, fill="black")

def open_text():
    file_path = filedialog.askopenfilename(initialdir=save_path, title="Select file", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    
    if file_path:
        password = simpledialog.askstring("Password", "Enter your password:", show='*')
        if password:
            try:
                with open(file_path, 'rb') as file:
                    salt = file.readline().strip()
                    encrypted_message = file.read()
                    decrypted_message = decrypt_message(encrypted_message, password, salt)
                    text_box.delete('1.0', tk.END)
                    text_box.insert(tk.END, decrypted_message)
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open and decrypt the file: {e}")
        else:
            messagebox.showwarning("Warning", "No password provided. Cannot decrypt the file.")

# Initialize dark_mode variable
dark_mode = False

def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode

    bg_color = "black" if dark_mode else "white"
    fg_color = "white" if dark_mode else "black"

    root.config(bg=bg_color)
    text_box_bg = "black" if dark_mode else "white"
    text_box_fg = "white" if dark_mode else "black"
    text_box.config(bg=text_box_bg, fg=text_box_fg, bd=2, relief=tk.SOLID)

    button_bg = "black" if dark_mode else "SystemButtonFace"
    button_fg = "white" if dark_mode else "black"
    button_activebg = "#333333" if dark_mode else "SystemButtonFace"
    
    change_prompt_button.config(bg=button_bg, fg=button_fg, activebackground=button_activebg, relief=tk.GROOVE)
    update_font_button.config(bg=button_bg, fg=button_fg, activebackground=button_activebg, relief=tk.GROOVE)
    save_button.config(bg=button_bg, fg=button_fg, activebackground=button_activebg, relief=tk.GROOVE)
    open_button.config(bg=button_bg, fg=button_fg, activebackground=button_activebg, relief=tk.GROOVE)
    toggle_button.config(bg=button_bg, fg=button_fg, activebackground=button_activebg, relief=tk.GROOVE)
    font_family_menu.config(bg=button_bg, fg=button_fg, activebackground=button_activebg, relief=tk.GROOVE)
    font_size_menu.config(bg=button_bg, fg=button_fg, activebackground=button_activebg, relief=tk.GROOVE)

    prompt_label.config(bg=bg_color, fg=fg_color, highlightbackground="white" if dark_mode else "black", highlightthickness=1)


def save_text():
    try:
        date = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        sentiment_score = analyze_sentiment(text_box.get("1.0", 'end-1c'))
        sentiment_feedback = "Positive" if sentiment_score > 0 else "Negative" if sentiment_score < 0 else "Neutral"
        filename = f'journal_{date}_{sentiment_feedback}.txt'
        file_path = os.path.join(save_path, filename)
        
        message = text_box.get("1.0", 'end-1c').encode()
        password = simpledialog.askstring("Password", "Enter your password:", show='*')
        
        if password:
            encrypted_message, salt = encrypt_message(message, password) # Use encrypt_message from journal_core

            with open(file_path, 'wb') as file:
                file.write(salt + b'\n' + encrypted_message)

            messagebox.showinfo("Success", f"Journal entry saved successfully with sentiment: {sentiment_feedback}")
        else:
            messagebox.showwarning("Warning", "No password provided. Entry not saved.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        
# Button layout
save_button = tk.Button(root, text="Encrypt & Save", command=save_text)
save_button.grid(row=5, column=0, padx=5, pady=5, sticky='ew')

open_button = tk.Button(root, text="Open", command=open_text)
open_button.grid(row=5, column=1, padx=5, pady=5, sticky='ew')

toggle_button = tk.Button(root, text="Toggle Dark/Light Mode", command=toggle_theme)
toggle_button.grid(row=6, column=0, columnspan=3, sticky='ew')

label = tk.Label(root, text="Characters: 0 Words: 0")
label.grid(row=7, column=0, columnspan=2, sticky='ew')

save_button = tk.Button(root, text="Encrypt & Save", command=save_text)

root.mainloop()