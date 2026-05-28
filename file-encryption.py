# idk what i'm doing
# Tutorial: https://www.geeksforgeeks.org/python/encrypt-and-decrypt-files-using-python/
# cryptography docs: https://cryptography.io/en/latest/installation/

# Import Fernet encryption method from cryptography library
import base64
import getpass
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# User provides file path
filepath = input("Enter path of file to encrypt: ")

# User chooses a password for the file
password = getpass.getpass("Enter password: ")
# Save password in a byte format
password = password.encode("utf-8")

# Generate salt for the key generation
salt = os.urandom(16)

# Key Derivation Function
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=480000,
)
key = base64.urlsafe_b64encode(kdf.derive(password))

# Create Fernet object with key
fernet_obj = Fernet(key)

# Open file to be encrypted
with open(filepath, "rb") as f:
    unencrypted_data = f.read()

# Encrypt file
encrypted_data = fernet_obj.encrypt(unencrypted_data)

# Include salt at top of encrypted data file
with open(filepath, "wb") as f:
    f.write(salt)

# Append encrypted data to encrypted file
with open(filepath, "ab") as f:
    f.write(encrypted_data)
    print("Encrypted file!")