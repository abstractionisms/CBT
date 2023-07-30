import tkinter as tk
import datetime
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import webbrowser
from tkinter import simpledialog, messagebox

# Definitions of different poetry styles
poetry_styles = {
    'France': {
        'Alexandrine': 'A line of poetic meter with 12 syllables.',
        'Rondeau': 'A short verse form with 13 to 15 lines that repeat in a specific pattern.',
        'Ballade': 'A form of medieval and Renaissance French poetry, usually set to music.'
    },
    'US': {
        'Free Verse': 'Poetry that does not rhyme or have a regular meter.',
        'Blank Verse': 'Poetry with a regular meter, but no rhyme.',
        'Haiku': 'A Japanese form of poetry consisting of 3 lines with 5, 7, and 5 syllables.'
    },
    'Asia': {
        'Haiku': 'A Japanese form of poetry consisting of 3 lines with 5, 7, and 5 syllables.',
        'Ghazal': 'A form of amatory poem or ode, originating in Arabic poetry.',
        'Tang Poetry': 'Poetry from the Tang dynasty, often regarded as the high point of Chinese literature.'
    },
    'England': {
        'Sonnet': 'A poem of 14 lines using any of a number of formal rhyme schemes.',
        'Limerick': 'A humorous verse of five lines with a defined meter and rhyme scheme.',
        'Epic': 'A long narrative poem in elevated or dignified language, celebrating the feats of a deity or demigod.'
    },
    'Italy': {
        'Terza Rima': 'A rhyming verse stanza form that consists of an interlocking three-line rhyme scheme.',
        'Ottava Rima': 'A rhymed stanza form of Italian origin.',
        'Rispetto': 'A form of Tuscan folk verse associated with love and courtship.'
    },
    'South America': {
        'Décima': 'A Spanish style of poetry with 10 lines.',
        'Payada': 'A competitive composing and singing of verses native to the Southern Cone.',
        'Cordel': 'A type of popular, often rhymed, literature in Brazil.'
    },
    'Africa': {
        'Griot': 'A West African historian, storyteller, praise singer, poet, or musician.',
        'Mabuta': 'A form of Zimbabwean oral poetry.',
        'Qasida': 'A form of Persian poetry.'
    }
}

def open_wikipedia(*args):
    selected_style = style_var.get().replace(" ", "_")
    url = "https://en.wikipedia.org/wiki/" + selected_style
    webbrowser.open(url)

def update_styles(*args):
    styles = list(poetry_styles[region_var.get()].keys())
    style_var.set(styles[0])
    menu = style_menu["menu"]
    menu.delete(0, "end")
    for style in styles:
        menu.add_command(label=style, command=lambda s=style: style_var.set(s))

def count_chars(event):
    s = text_box.get("1.0", 'end-1c')
    words = len(s.split())
    label.config(text = "Characters: " + str(len(s)) + " Words: " + str(words))
    if len(s) >= 500:
        save_button.grid(row=5, column=0, columnspan=2)
    else:
        save_button.grid_remove()
    canvas.coords(rectangle, 0, 500, 20, 500 - min(len(s)*500/500, 500))

def select_poetry_style(*args):
    selected_region = region_var.get()
    selected_style = style_var.get()
    poetry_description = poetry_styles[selected_region][selected_style]
    poetry_style_description.config(text = poetry_description)

def encrypt_message(message, password):
    password_provided = password
    password = password_provided.encode()
    salt = b'\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    cipher_suite = Fernet(key)
    cipher_text = cipher_suite.encrypt(message)
    return cipher_text

def decrypt_message(cipher_text, password):
    password_provided = password
    password = password_provided.encode()
    salt = b'\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    cipher_suite = Fernet(key)
    plain_text = cipher_suite.decrypt(cipher_text)
    return plain_text.decode()

def save_text():
    date = datetime.datetime.now().strftime('%m.%d.%y')
    filename = 'journal_{}.txt'.format(date)
    text = text_box.get("1.0", "end-1c").encode()
    password = simpledialog.askstring("Password", "Enter password:", show='*')
    cipher_text = encrypt_message(text, password)
    with open(filename, 'wb') as f:
        f.write(cipher_text)
    root.quit()

def open_text():
    filename = simpledialog.askstring("Filename", "Enter filename:")
    password = simpledialog.askstring("Password", "Enter password:", show='*')
    try:
        with open(filename, 'rb') as f:
            cipher_text = f.read()
        plain_text = decrypt_message(cipher_text, password)
        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, plain_text)
    except Exception:
        messagebox.showerror("Error", "Failed to open and decrypt the file. Check your filename and password.")

root = tk.Tk()
root.title("Poetry Journal")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

regions = list(poetry_styles.keys())
styles = list(poetry_styles[regions[0]].keys())

region_var = tk.StringVar(root)
region_var.set(regions[0])  # set the default option
region_menu = tk.OptionMenu(root, region_var, *regions)
region_menu.grid(row=2, column=0, columnspan=2)

style_var = tk.StringVar(root)
style_var.set(styles[0])  # set the default option
style_menu = tk.OptionMenu(root, style_var, *styles)
style_menu.grid(row=3, column=0, columnspan=2)

region_var.trace('w', update_styles)
style_var.trace('w', select_poetry_style)

poetry_style_description = tk.Label(root, text = poetry_styles[regions[0]][styles[0]])
poetry_style_description.grid(row=4, column=0, columnspan=2)

text_box = tk.Text(root, width = 50, height = 10, wrap=tk.WORD, font=("Calibri", 12))
text_box.grid(row=0, column=0, sticky='nsew')
text_box.bind('<KeyRelease>', count_chars)

label = tk.Label(root, text = "Characters: 0 Words: 0")
label.grid(row=1, column=0, columnspan=2)

canvas = tk.Canvas(root, width=20, height=500)
canvas.grid(row=0, column=1, sticky='ns')
rectangle = canvas.create_rectangle(0, 500, 20, 500, fill="black")

save_button = tk.Button(root, text = "Encrypt & Save", command = save_text)
open_button = tk.Button(root, text = "Open", command = open_text)
example_button = tk.Button(root, text = "Example", command = open_wikipedia)
example_button.grid(row=6, column=0, columnspan=2)
open_button.grid(row=5, column=0, columnspan=2)

root.mainloop()