# idk what i'm doing
# Tutorial: https://www.geeksforgeeks.org/python/encrypt-and-decrypt-files-using-python/
# cryptography docs: https://cryptography.io/en/latest/installation/

# Import Fernet encryption method from cryptography library
# Fernet uses AES encryption
import base64
import sys
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# User selects file to decrypt
filename = input("Enter file to decrypt: ")

# User enters the password for the file
password = input("Enter password: ")
password = password.encode("utf-8")

# Read encrypted data
with open(filename, "rb") as f:
    encrypted_data = f.read()

# Extract salt (first 16 bytes)
salt = encrypted_data[:16]
# Actual data is the stuff after the salt
encrypted_data = encrypted_data[16:]

# Key Derivation Function
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=480000,
)
key = base64.urlsafe_b64encode(kdf.derive(password))

try:
    # Decrypt
    fernet_obj = Fernet(key)
    decrypted_data = fernet_obj.decrypt(encrypted_data)
    print("Decrypted file!")
except InvalidToken:
    print("Error: Incorrect password or corrupted file.")
    sys.exit(1)


# Write decrypted data back into file
with open(filename, "wb") as f:
    f.write(decrypted_data)