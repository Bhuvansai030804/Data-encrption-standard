# client.py
from Crypto.Cipher import DES
import socket
import base64
import padding

def create_des_cipher(key):
    """Create a DES cipher object with the given key"""
    return DES.new(key, DES.MODE_ECB)

def encrypt_message(cipher, message):
    """Encrypt a message and return base64 encoded string"""
    padded_message = padding.pad(message.encode('utf-8'))
    encrypted_bytes = cipher.encrypt(padded_message)
    return base64.b64encode(encrypted_bytes).decode('utf-8')

def decrypt_message(cipher, encrypted_message):
    """Decrypt a base64 encoded encrypted message"""
    encrypted_bytes = base64.b64decode(encrypted_message)
    decrypted_message = cipher.decrypt(encrypted_bytes)
    return padding.unpad(decrypted_message).decode('utf-8')

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5000))
    print("Connected to server")

    # Receive the key from server
    key = client_socket.recv(8)
    cipher = create_des_cipher(key)

    try:
        while True:
            # Get message from user
            message = input("Enter message (or 'quit' to exit): ")
            if message.lower() == 'quit':
                break

            # Encrypt and send message
            encrypted_message = encrypt_message(cipher, message)
            client_socket.send(encrypted_message.encode('utf-8'))

            # Receive and decrypt response
            encrypted_response = client_socket.recv(1024).decode('utf-8')
            decrypted_response = decrypt_message(cipher, encrypted_response)
            print(f"Server response: {decrypted_response}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()