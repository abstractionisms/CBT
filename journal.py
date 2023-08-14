import tkinter as tk
import datetime
import random
import textwrap
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
from tkinter import simpledialog, messagebox

def count_chars(event):
    s = text_box.get("1.0", 'end-1c')
    words = len(s.split())
    label.config(text = "Characters: " + str(len(s)) + " Words: " + str(words))
    if len(s) >= 1500:
        save_button.grid(row=4, column=0, columnspan=2)
    else:
        save_button.grid_remove()
    canvas.coords(rectangle, 0, 500, 20, 500 - min(len(s)*500/1500, 500))

def change_prompt():
    prompt_label.config(text = random.choice(prompts))

def encrypt_message(message, password):
    password_provided = password
    password = password_provided.encode()
    salt = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
    salt = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
root.title("Character Building")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

prompts = [
    # Reflection
    "Reflect on your personal growth since this time last year. Where were you at? What are some significant changes you've noticed?",
    "Reflect on a mistake you made in the past. What did you learn from it?",
    "Reflect on your values and how you came to them. How have they evolved over the years?",
    "Reflect on a time when you felt a strong emotional reaction to something somebody said. What triggered it and how did you handle it?",
    "Reflect on a time when you were extremely grateful. What made you feel this way?",
    "Reflect on a personal setback you experienced. How did you bounce back?",
    "Reflect on an achievement you are proud of. How did it shape your attitude towards success?",
    "Reflect on how your childhood experiences have shaped your current self.",
    "Reflect on a time when you had to adapt to a significant change in your life.",
    "Reflect on a moment when you experienced a major breakthrough in your personal or professional life.",
    "Reflect on a time when you misinterpreted another's words. How did you improve your listening and resolve that conflict?"

    # Memories
    "Describe a moment in your life you would like to relive. What makes this moment special?",
    "Write about a time when you made a difficult decision. How did it affect you and others around you?",
    "Describe an event that changed your perspective on life.",
    "Describe a moment when you felt extremely proud of yourself. What led to this feeling?",
    "Describe a time when you faced a fear. What was the outcome?",
    "Describe your most memorable travel experience. What did you learn about yourself or others on that trip?",
    "Describe a memorable celebration or event you attended.",
    "Describe a memorable childhood experience that left a lasting impression on you.",
    "Describe a time when you experienced a cultural shock.",
    "Describe a memorable time with a complete stranger or when you met someone for the first time unexpectedly.",

    # Goals
    "Write about a dream or goal that you have. What steps are you taking to achieve it?",
    "Reflect on your personal growth goals for the upcoming year.",
    "Write about a skill or hobby you want to learn or improve on. How do you plan on doing this?",
    "Describe a goal you've recently achieved. Reflect on the success and the impact its had on yourself and those in your life.",
    "Write about a personal milestone you aim to achieve in the next five years.",
    "Describe a long-term career goal you have. How do you plan to reach it?",
    "Write about a health or fitness goal you have. What steps are you taking to achieve it?",
    "Write about a personal project you want to start or complete this year.",
    "Describe a goal that seems out of reach right now. How can you break it down into smaller, achievable steps?",

    # Challenges
    "Write about a challenge you faced and the steps you took alone or with someone else to overcome adversity.",
    "Describe a time when you had to step out of your comfort zone. What did you learn from the experience?",
    "Describe a challenging work or school situation you encountered. Explain your approach and how you successfully managed it.",
    "Reflect on a time when you had to navigate a conflict with someone. What was the outcome?",
    "Write about a personal or professional obstacle you've recently overcome.",
    "Describe a challenge you're currently facing. How are you planning to overcome it?",
    "Write about a time when you had to stand up for what you believe in.",
    "Describe a tough experience that made you develop and improve.",
    "Write about a time when you had to make a tough choice between two equally appealing options.",
    "Describe a time when you had to solve a complex problem. What was your approach?",
    "Reflect on a challenging conversation that led you to change your mind about something or somebody else."

    # Relationships
    "Write about a person who has greatly influenced your life. How have they shaped you?",
    "Describe a moment when you had to forgive someone. How did it change your relationship with that person?",
    "Reflect on a meaningful conversation you recently had. Why was it significant?",
    "Write about a relationship in your life that has changed over the past year and why.",
    "Reflect on a time when you felt a deep connection with someone. What made this connection special?",
    "Write about a time when you had to let go of a relationship that was important to you.",
    "Reflect on a time when you had a misunderstanding with someone close to you. How did you resolve it?",
    "Write about a friend who has been with you through thick and thin.",
    "Reflect on a time when you provided support to someone during a tough time. How did it change your relationship or outlook?",
    "Describe an interaction with someone that changed your perspective on life."

    # CBT Therapy
    "Reflect on a situation where your initial emotional reaction might have clouded your judgement. How could you view the situation differently?",
    "Write about a time when you found yourself generalizing a single negative event as a never-ending pattern of defeat.",
    "Describe a moment when you caught yourself 'mind reading' or assuming you know what others are thinking about you.",
    "Reflect on a time when you 'catastrophized' or imagined the worst possible outcome in a situation. What might be a more balanced view?",
    "Write about an instance where you personalized a situation, blaming yourself for an event that was not entirely under your control.",
    "Describe a situation where you jumped to conclusions without enough evidence. How could you have gathered more information before reacting?",
    "Write about a time when you magnified the positive attributes of others while minimizing your own positive attributes.",
    "Reflect on a situation where you discounted the positive aspects and focused only on the negative. How could you have viewed it in a more balanced way?",
    "Write about a time when you 'should' or 'must' on yourself or others excessively, creating unrealistic expectations or demands."
]

prompt_label = tk.Label(root, text=random.choice(prompts), wraplength=500)
prompt_label.grid(row=2, column=0, columnspan=2)

change_prompt_button = tk.Button(root, text="Change Prompt", command=change_prompt)
change_prompt_button.grid(row=3, column=0, columnspan=2)

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
open_button.grid(row=5, column=0, columnspan=2)

root.mainloop()