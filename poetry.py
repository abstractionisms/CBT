import tkinter as tk
import datetime
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import webbrowser
from tkinter import simpledialog, messagebox, ttk

poetry_styles = {
    'France': {
        'Alexandrine': 'A line of poetic meter with 12 syllables.',
        'Rondeau': 'A short verse form with 13 to 15 lines that repeat in a specific pattern.',
        'Ballade': 'A form of medieval and Renaissance French poetry, usually set to music.',
        'Bref Double': 'French quatorzain.',
        'Chanso': 'Five to six stanzas with an envoy.',
        'Chant Royal': '60 lines',
        'Dansa': 'Occitan form',
        'Descort': 'French form that makes each line special.',
        'Dizain': 'French 10x10 form',
        'Huitain': 'French 8-liner with an ababbcbc rhyme scheme',
        'Kyrielle': 'Adjustable French form',
        'Lai': 'Nine-liner from the French',
        'Quatern': 'French 4x4 form',
        'Rimas Dissolutas': 'Old French form',
        'Rime Couee': 'French 6-liner',
        'Rondeau Redouble': '25-liner invented by Clement Marot',
        'Rondel': '13 lines in 3 stanzas',
        'Rondel Supreme': 'French 14-liner',
        'Rondelet': 'French 7-liner',
        'Rondine': '12-liner with a refrain',
        'Triolet': '8-line French form',
        'Virelai': 'French 9-liner with alternatin line lengths and rhymes'
    },
    'Spain': {
        'Endecha': 'Quatrain form',
        'Espinela': 'Spanish 10-liner named after Vincente Espinel',
        'Flamenca': 'Spanish quatrain form',
        'Ovillejo': '10-liner popularized by Miguel de Cervantes',
        'Pregunta': 'Spanish collaborative poem',
        'Quintilla': 'Spanish 5-liner',
        'Seguidilla': 'Spanish 7-liner that began as a dance song.',
        'Shadorma': 'Spanish 6-liner.',
        'Soledad': 'Spanish tercet form'
    },
    'US': {
        'Free Verse': 'Poetry that does not rhyme or have a regular meter.',
        'Blank Verse': 'Poetry with a regular meter, but no rhyme.',
        'Interlocking Rubaiyat': 'Used by Omar Khayyam, Robert Frost, and many others.',
        'Lune': 'Robert Kelly invention also known as the American haiku',
        'Madrigal': 'An American twist on the Italian form: Madrigal',
        'Novem': 'Robin Skelton 3-obssessed form inspired by Burmese form than-bauk',
        'Palindrome': 'Also known as mirror poetry',
        'Tricube': '3 stanzas by 3 lines by 3 syllables',
        'Trimeric': 'Invented by Charles A. Stone - it has 4 stanzas.'
    },
    'Asia': {
        'Haiku': 'A Japanese form of poetry consisting of 3 lines with 5, 7, and 5 syllables.',
        'Ghazal': 'A form of amatory poem or ode, originating in Arabic poetry.',
        'Tang Poetry': 'Poetry from the Tang dynasty, often regarded as the high point of Chinese literature.',
        'Chueh-chu':  'Chinese 8-line sonnet cut short.',
        'Cinquain': 'Popular Japanese five liner',
        'Dodoitsu': '4-line Japanese form',
        'Gogyohka': '5-line poem developed by Enta Kusakabe in Japan',
        'Haibun': 'Popularized by Matsuo Basho in Japan',
        'Imayo': '4-line Japanese poem with a pause in the middle of each line',
        'Kouta': 'Japanese quatrain form',
        'Luc Bat': 'Vietnamese "6-8" form',
        'Pantoum': 'Repetive form from Malay',
        'Renga': 'Japanese collaborative form',
        'Sedoka': 'Japanese Q&A 6-liner',
        'Sijo': 'Korean poetic form',
        'Somonka': 'Japanese collaborative form',
        'Tanka': 'Kinda like a haiku plus a couplet',
        'Than-bauk': 'Burmese descending rhyme tercet or linked verse',
        'Tripadi': 'Bengali tercet form',
        'Waka': 'Japanese 5-liner',
        'Ya-du': 'Burmese quintain form'
    },
    'England': {
        'Sonnet': 'A poem of 14 lines using any of a number of formal rhyme schemes.',
        'Limerick': 'A humorous verse of five lines with a defined meter and rhyme scheme.',
        'Epic': 'A long narrative poem in elevated or dignified language, celebrating the feats of a deity or demigod.',
        'Clerihew': 'English quatrain form.',
        'Italian Octave': 'First 8 lines of Petrarchan sonnet',
        'Roundel': 'English 11-line variant of the rondeau'
    },
    'Italy': {
        'Terza Rima': 'A rhyming verse stanza form that consists of an interlocking three-line rhyme scheme.',
        'Ottava Rima': 'A rhymed stanza form of Italian origin.',
        'Rispetto': 'A form of Tuscan folk verse associated with love and courtship.',
        'Barzeletta': 'Sometimes called the Frottola-barzelletta.',
        'Madrigal': 'Three stanza form: a tercet, quatrain, and sestet.',
        'Sicilian Octave': '8-liner with abababab rhyme scheme and iambic pentameter.',
        'Stornello': 'Italian tercet form',
        'Strambotto': 'Hendecasyllabic octave with abababab rhyme scheme.',
        'Terzanelle': 'Terza rima and villanelle combined',
        'Trena-sei': '36-liner invented by John Ciardi',
        'Villanelle': 'Five tercets and a quatrain'
    },
    'Irish & Welsh': {
        'Ae Freislighe': 'Quatrain with intense rhyme scheme',
        'Awdl Gywydd': 'Welsh quatrain with end and internal rhymes',
        'Breccbairdne': 'Quatrain form with 4 syllables in first line, 6 in the others.',
        'Byr a Thoddaid': 'Welsh quatrain',
        'Casbairdne': 'Irish quatrain form',
        'Cethramtu Rannaigechta Moire': 'Irish quatrain form with 3-syllable lines.',
        'Clogyrnach': '6-line Welsh form',
        'Cro Cumaisc Etir Casbairdni Ocus Lethrannaighecht': 'Irish quatrain form.',
        'Cyhydedd Fer': 'Welsh couplet form.'
        'Cyhydedd Hir'': Welsh quatrain form.',
        'Cyhydedd Naw Ban': 'Welsh couplet form with 9-syllable lines.',
        'Cyrch A Chwta': '8-line Welsh form with 7 syllables per line.',
        'Cywydd Deuair Fyrion': 'Welsh couplet form with 4 syllables.',
        'Cywydd Deuair Hirion': 'Welsh couplet form with 7 syllables.',
        'Cywydd Llosgyrnog': '6-liner with internal rhymes and variable syllables.',
        'Dechnad Cummaisc': 'Irish quatrain form with alternating line lengths.',
        'Dechnad Mor': 'Variation on the dechnad cummaisc.',
        'Droigneach': 'Irish 4-liner',
        'Englyn Byr Cwca': 'Welsh tercet form with internal rhymes.',
        'Englyn Cyrch': 'Welsh 4-liner with 7 syllables per line',
        'Gwawdodyn': 'Welsh poetic form',
        'Gwawdodyn Byr': 'Welsh quatrain form with 9 and 10 syllable lines',
        'Gwawdodyn Hir': 'Welsh 6-liner',
        'Hir a Thoddaid': '6 lines that mostly all share the same rhyme',
        'Lethrannaegecht Mor': 'Irish quatrain form with 5 syllable lines',
        'Rannaigheact Mhor': 'Irish form that fits a lot of rules into 28 syllables',
        'Rhupunt': 'Welsh form that offers variability and rigidity simultaneously',
        'Rinnard': 'Irish quatrain form with 6-syllable lines',
        'Seadna': 'Irish quatrain form',
        'Snam Suad': 'Irish 8-liner',
        'Tawddgyrch Cadwynog': 'Welsh form comprised of pairs of quatrains',
        'Toddaid': 'Welsh quatrain form',
        'Treochair': 'Alliterative tercets that rhyme with variable 3/7/7 lines',
        'Trian Rannaigechta Moire': 'Irish quatrain form in which all end words consonate'
    },
    'Latin America': {
        'Décima': 'A Spanish style of poetry with 10 lines.',
        'Payada': 'A competitive composing and singing of verses native to the Southern Cone.',
        'Cordel': 'A type of popular, often rhymed, literature in Brazil.'
    },
    'Africa & the Middle East': {
        'Griot': 'A West African historian, storyteller, praise singer, poet, or musician.',
        'Mabuta': 'A form of Zimbabwean oral poetry.',
        'Qasida': 'A form of Persian poetry.',
        'Kimo': 'Israeli form of haiku',
        'Landay': 'Poem comprised of self-contained couplets',
        'Masnavi': 'Sometimes called Mathnawi, it is an older form with Arabic, Persian, Turkish, and Urdu variants'
    }
}

region_codes = {
    'France': 'FR',
    'Spain': 'ES',
    'US': 'US',
    'Asia': 'As',
    'England': 'En',
    'Italy': 'IT',
    'Irish & Welsh': "GB",
    'Latin America': 'LA',
    'Africa & the Middle East': 'A'
}

def open_wikipedia(*args):
    selected_style = style_var.get().replace(" ", "_")
    url = "https://en.wikipedia.org/wiki/" + selected_style
    webbrowser.open(url)

def update_region_label():
    selected_region = region_var.get()
    region_code = region_codes[selected_region]  # Access the region_code using the region_codes dictionary
    region_count = len(poetry_styles[selected_region])
    total_count = sum(len(styles) for styles in poetry_styles.values())
    region_label.config(text="{} {}/{}".format(region_count, region_code, total_count))

def update_styles(*args):
    styles = list(poetry_styles[region_var.get()].keys())
    style_var.set(styles[0])
    style_combobox['values'] = styles
    update_region_label()  # Update the region label here

def count_chars(event):
    s = text_box.get("1.0", 'end-1c')
    words = len(s.split())
    label.config(text = "Characters: " + str(len(s)) + " Words: " + str(words))
    if len(s) <= 1000000:
        save_button.grid(row=5, column=0, columnspan=2)
    else:
        save_button.grid_remove()

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
    region_codes = {
        'France': 'FR',
        'Spain': 'ES',
        'US': 'US',
        'Asia': 'As',
        'England': 'En',
        'Italy': 'IT',
        'Latin America': 'LA',
        'Africa': 'Af'
    }

    region = region_var.get()
    region_code = region_codes[region]
    style = style_var.get()
    style_code = ''.join(word[0] for word in style.split()) # Takes the first letter of each word in the style

    date = datetime.datetime.now().strftime('%m.%d.%y')
    filename = '{}{}{}.txt'.format(region_code, style_code, date) # Concatenates the region code, style code, and date

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
region_var.set(regions[0])
region_menu = tk.OptionMenu(root, region_var, *regions)
region_menu.grid(row=3, column=0)

region_label = tk.Label(root, text="")
region_label.grid(row=2, column=0)

style_var = tk.StringVar(root)
style_var.set(styles[0])
style_combobox = ttk.Combobox(root, textvariable=style_var, values=styles)
style_combobox.grid(row=4, column=0, columnspan=2)

style_var.trace('w', select_poetry_style)
region_var.trace('w', update_styles)
update_region_label()
poetry_style_description = tk.Label(root, text = poetry_styles[regions[0]][styles[0]])
poetry_style_description.grid(row=6, column=0, columnspan=2)

text_box = tk.Text(root, width = 50, height = 10, wrap=tk.WORD, font=("Calibri", 12))
text_box.grid(row=0, column=0, sticky='nsew')
text_box.bind('<KeyRelease>', count_chars)

label = tk.Label(root, text = "Characters: 0 Words: 0")
label.grid(row=1, column=0, columnspan=2)

save_button = tk.Button(root, text = "Encrypt & Save", command = save_text)
open_button = tk.Button(root, text = "Open", command = open_text)
example_button = tk.Button(root, text = "Example", command = open_wikipedia)
example_button.grid(row=7, column=0, columnspan=2) 
open_button.grid(row=8, column=0, columnspan=2)   

root.mainloop()