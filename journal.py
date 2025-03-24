
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import datetime
import random
import os
import configparser
from textblob import TextBlob  # For sentiment analysis
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64
from cryptography.fernet import Fernet

# Load configuration from an external file
config = configparser.ConfigParser()
config.read('config.ini')
save_path = config.get('CONFIG', 'save_path')

def guide_meditation():
    messagebox.showinfo("Meditation", "Take a deep breath, hold it for a moment, and slowly exhale. Repeat for a few breaths.")

def analyze_sentiment(entry):
    sentiment = TextBlob(entry).sentiment
    return sentiment.polarity  # Returns a polarity score between -1 and 1

def generate_salt():
    return os.urandom(16)

def generate_key(password: bytes, salt: bytes):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password))

def encrypt_message(message: bytes, password: str):
    salt = os.urandom(16)  # Generates a secure random salt
    key = generate_key(password.encode(), salt)  # Generates a key using the provided password and salt
    f = Fernet(key)
    encrypted_message = f.encrypt(message)  # Encrypts the message using the generated key
    return encrypted_message, salt  # Returns the encrypted message and the salt used for key generation


def decrypt_message(cipher_text: bytes, password: str, salt: bytes):
    key = generate_key(password.encode(), salt)
    cipher_suite = Fernet(key)
    plain_text = cipher_suite.decrypt(cipher_text)
    return plain_text.decode()

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
            salt = generate_salt()  # Use your generate_salt function
            key = generate_key(password.encode(), salt)  # Use your generate_key function to derive a Fernet key
            f = Fernet(key)
            encrypted_message = f.encrypt(message)  # Encrypts the message using the generated key

            with open(file_path, 'wb') as file:
                file.write(salt + b'\n' + encrypted_message)

            messagebox.showinfo("Success", f"Journal entry saved successfully with sentiment: {sentiment_feedback}")
        else:
            messagebox.showwarning("Warning", "No password provided. Entry not saved.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

root = tk.Tk()
root.title("Character Building")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

prompts = {
    "Creative Reflection": [
        "Imagine you could have a conversation with your past self from 10 years ago. What advice would you give them, and what questions would you ask?",
        "If your life were a book, what would the current chapter be called, and why?",
        "If you could design a museum exhibit showcasing your life's journey, what three artifacts would you include and why?",
        "If you could plant a 'seed' of change in your life a year ago, what would it be, and what would the 'grown' version look like today?",
        "Write a letter to your future self, outlining your hopes and dreams for the next decade.",
        "Reflect on a metaphor that represents your current state of mind or life situation. Explain why you chose it.",
        "If you could create a soundtrack for your life right now, what three songs would be on it and why?",
        "Reflect on a dream you've had recently. What symbolic meanings might it hold for your waking life?",
        "If you could have a 'redo' button for one moment in your life, would you use it? Why or why not?",
        "Reflect on a personal 'myth' or story you tell yourself about your life. How can you rewrite it for a more empowering narrative?"
    ],
    "Sensory Memories": [
        "Describe a memory triggered by a specific smell. What emotions and images does it evoke?",
        "Recall a moment where a particular sound was deeply impactful. What was the sound, and what was happening?",
        "Describe a time when a texture or touch created a vivid memory. What was the sensation, and what did it remind you of?",
        "Describe a memory associated with a specific taste. What made the taste memorable?",
        "Describe a moment where a particular sight was incredibly striking. What did you see, and how did it affect you?",
        "Describe a memory linked to a specific time of day and the quality of light. How did the light enhance the experience?",
        "Recall a memory where the weather played a significant role. How did it influence your experience?",
        "Describe a memory centered around a physical object. What emotions and stories are tied to it?",
        "Describe a moment where you were fully present in your body and senses. What were you experiencing?",
        "Recall a memory that feels like a specific color. What color is it, and what does it represent?"
    ],
    "Future-Oriented Goals": [
        "Design a 'future self' vision board. What images and words represent the person you want to become?",
        "If you could master any skill in a year, what would it be, and how would it transform your life?",
        "Write a 'manifesto' outlining your personal values and goals for the next chapter of your life.",
        "Imagine you are giving a TED Talk in five years about a major achievement. What would your topic be, and what key points would you make?",
        "If you could 'time capsule' a goal for your future self, what would it be, and what items would you include?",
        "Design a personal 'quest' or adventure to achieve a major goal. What steps would it involve?",
        "If you could have a mentor for a specific goal, who would it be, and what wisdom would you seek?",
        "Create a 'reverse bucket list' of things you want to stop doing to achieve your goals.",
        "If you could 'gamify' your goal achievement, what levels and rewards would you design?",
        "Write a 'contract' with yourself, outlining your commitment to a specific goal and the consequences of not achieving it."
    ],
    "Resilience and Growth": [
        "Describe a time when you turned a setback into a setup for something better. How did you reframe the situation?",
        "Write about a moment when you discovered an inner strength you didn't know you had.",
        "Describe a time when you had to 'unlearn' something to grow. What was it, and why was it necessary?",
        "Reflect on a moment where you chose courage over comfort. What was the outcome?",
        "Write about a time when you had to navigate uncertainty. What strategies did you use?",
        "Describe a challenging situation that ultimately led to a significant personal transformation.",
        "Reflect on a time when you had to rebuild something after it was broken. What did you learn in the process?",
        "Write about a moment when you found beauty or meaning in a difficult experience.",
        "Describe a time when you had to 'pivot' or change direction unexpectedly. How did you adapt?",
        "Reflect on a time when you found a creative solution to a complex problem."
    ],
    "Interpersonal Dynamics": [
        "Describe a moment when you felt truly seen and understood by another person. What made it feel significant?",
        "Write about a relationship where you learned a valuable lesson about communication.",
        "Reflect on a time when you had to navigate a power dynamic in a relationship. What did you learn?",
        "Describe a moment when you experienced a deep sense of belonging with a group or community.",
        "Write about a relationship that challenged your assumptions or beliefs.",
        "Reflect on a time when you had to set a boundary in a relationship. How did it impact you and the other person?",
        "Describe a moment when you experienced empathy for someone with a very different perspective.",
        "Write about a relationship where you felt inspired or motivated by the other person.",
        "Reflect on a time when you had to navigate a conflict of values in a relationship.",
        "Describe a moment when you felt a sense of reciprocity or mutual support in a relationship."
    ],
    "Advanced CBT Techniques": [
        "Reflect on a situation where you engaged in 'emotional reasoning' (believing your feelings reflect reality). How could you have used evidence-based thinking?",
        "Write about a time when you used 'labeling' (assigning negative labels to yourself or others). How could you reframe the situation with more neutral language?",
        "Describe a moment when you engaged in 'filtering' (focusing only on negatives). How could you have expanded your focus to include positives?",
        "Reflect on a situation where you engaged in 'always being right' (putting others on trial). How could you have approached it with more openness?",
        "Write about a time when you engaged in 'blaming' (holding others responsible for your pain). How could you have taken more personal responsibility?",
        "Describe a moment when you engaged in 'comparing' (seeing others as superior). How could you have focused on your own unique strengths?",
        "Reflect on a situation where you engaged in 'heaven's reward fallacy' (expecting sacrifice to pay off). How could you have managed your expectations more realistically?",
        "Write about a time when you engaged in 'control fallacies' (feeling either victimized or overly responsible). How could you have found a middle ground?",
        "Describe a moment when you engaged in 'change fallacies' (expecting others to change for your happiness). How could you have focused on changing your own responses?",
        "Reflect on a situation where you engaged in 'globalizing' (seeing a single event as a universal pattern). How could you have viewed it as an isolated incident?"
    ]
}

# Corrected prompt selection
def get_random_prompt(prompt_dict):
    category = random.choice(list(prompt_dict.keys()))
    prompt = random.choice(prompt_dict[category])
    return prompt

prompt_label = tk.Label(root, text=get_random_prompt(prompts), wraplength=500)
prompt_label.grid(row=2, column=0, columnspan=2)

def change_prompt():
    new_prompt = get_random_prompt(prompts)
    prompt_label.config(text=new_prompt)

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

def open_text():
    # Let the user select a file to open
    file_path = filedialog.askopenfilename(initialdir=save_path, title="Select file", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    
    if file_path:  # Proceed if the user selected a file
        password = simpledialog.askstring("Password", "Enter your password:", show='*')
        if password:
            try:
                with open(file_path, 'rb') as file:
                    # Read the salt and encrypted message from the file
                    salt = file.readline().strip()  # Assuming the salt is on the first line
                    encrypted_message = file.read()
                    
                    # Decrypt the message
                    decrypted_message = decrypt_message(encrypted_message, password, salt)
                    
                    # Display the decrypted text in the text_box
                    text_box.delete('1.0', tk.END)  # Clear the current text
                    text_box.insert(tk.END, decrypted_message)  # Insert the decrypted text
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open and decrypt the file: {e}")
        else:
            messagebox.showwarning("Warning", "No password provided. Cannot decrypt the file.")

def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode  # Flip the dark_mode flag
    
    bg_color = "black" if dark_mode else "white"
    fg_color = "white" if dark_mode else "black"
    
    # Update the colors of your widgets
    root.config(bg=bg_color)
    text_box.config(bg=bg_color, fg=fg_color)

dark_mode = False  # Initial mode
toggle_button = tk.Button(root, text="Toggle Dark/Light Mode", command=toggle_theme)
toggle_button.grid(row=6, column=0, columnspan=2)

save_button = tk.Button(root, text = "Encrypt & Save", command = save_text)
open_button = tk.Button(root, text = "Open", command = open_text)
open_button.grid(row=5, column=0, columnspan=2)

root.mainloop()
