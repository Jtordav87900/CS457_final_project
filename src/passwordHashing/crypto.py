from cryptography.fernet import Fernet
import os
import base64
KEY_PATH = r"D:\Code\Password Manager\secret\key.key"  # Make sure to use raw strings for paths on Windows


def load_key(user_id):
    # Load the key from the file\
    key_path = os.path.join("D:\Code\Password Manager\secret", f"{user_id}_key.key")
    if not os.path.exists(key_path): #if file does not exist, generate new key
        key = Fernet.generate_key()
        with open(key_path, "wb") as key_file:
            key_file.write(key)
    else:
        key = open(key_path, "rb").read() #else get key from file
    return key


def encrypt_text(message, user_id):
    print("Type of message: " + str(type(message)))
    key = load_key(user_id)  # Load encryption key
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())  # Encrypt message (bytes)
    encrypted_message_b64 = base64.urlsafe_b64encode(encrypted_message).decode('utf-8')  # Convert to Base64 string
    print("in encrpyt-Type of encrypted_message_b64: " + str(type(encrypted_message_b64)))
    return encrypted_message_b64  # Store Base64 string in DB

def decrypt_text(encrypted_message_b64, user_id):
    print("in decrypt-Type of encrypted_message_b64: " + str(type(encrypted_message_b64)))
    key = load_key(user_id)  # Load decryption key
    f = Fernet(key)
    encrypted_message = base64.urlsafe_b64decode(encrypted_message_b64)  # Convert Base64 string back to bytes
    print("type of encrypted_message: " + f.decrypt(encrypted_message).decode("utf-8") + str(type(f.decrypt(encrypted_message).decode("utf-8"))))
    return f.decrypt(encrypted_message).decode("utf-8")  # Decrypt and return original string
