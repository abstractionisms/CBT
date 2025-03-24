# journal_core.py
import os
import base64
from textblob import TextBlob
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import configparser

# Load configuration from an external file
config = configparser.ConfigParser()
config.read('config.ini')
save_path = config.get('CONFIG', 'save_path')

def guide_meditation():
    """Provides a simple meditation prompt."""
    print("Take a deep breath, hold it for a moment, and slowly exhale. Repeat for a few breaths.") # Changed to print for refactor

def analyze_sentiment(entry):
    """Analyzes the sentiment of a given text entry."""
    sentiment = TextBlob(entry).sentiment
    return sentiment.polarity

def generate_salt():
    """Generates a random salt for encryption."""
    return os.urandom(16)

def generate_key(password: bytes, salt: bytes):
    """Generates a key from a password and salt using PBKDF2HMAC."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password))

def encrypt_message(message: bytes, password: str):
    """Encrypts a message using Fernet encryption."""
    salt = generate_salt()
    key = generate_key(password.encode(), salt)
    f = Fernet(key)
    encrypted_message = f.encrypt(message)
    return encrypted_message, salt

def decrypt_message(cipher_text: bytes, password: str, salt: bytes):
    """Decrypts a message using Fernet decryption."""
    key = generate_key(password.encode(), salt)
    cipher_suite = Fernet(key)
    plain_text = cipher_suite.decrypt(cipher_text)
    return plain_text.decode()