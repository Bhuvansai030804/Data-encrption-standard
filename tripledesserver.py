# server.py
from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
import socket
import base64
import padding

def generate_key():
    """Generate a valid Triple DES key"""
    while True:
        try:
            key = DES3.adjust_key_parity(get_random_bytes(24))
            return key
        except ValueError:
            continue

def create_triple_des_cipher(key):
    """Create a Triple DES cipher object with the given key"""
    return DES3.new(key, DES3.MODE_ECB)

def decrypt_message(cipher, encrypted_message):
    """Decrypt a base64 encoded encrypted message"""
    encrypted_bytes = base64.b64decode(encrypted_message)
    decrypted_message = cipher.decrypt(encrypted_bytes)
    return padding.unpad(decrypted_message).decode('utf-8')

def encrypt_message(cipher, message):
    """Encrypt a message and return base64 encoded string"""
    padded_message = padding.pad(message.encode('utf-8'))
    encrypted_bytes = cipher.encrypt(padded_message)
    return base64.b64encode(encrypted_bytes).decode('utf-8')

def start_server():
    # Generate a valid Triple DES key (24 bytes)
    key = generate_key()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5000))
    server_socket.listen(1)
    print("Server started, waiting for connections...")

    while True:
        client_socket, address = server_socket.accept()
        print(f"Connection from {address} established")
        
        # Send the key to client (in real-world, use secure key exchange)
        client_socket.send(key)
        
        # Create cipher object
        cipher = create_triple_des_cipher(key)

        try:
            while True:
                # Receive encrypted message
                encrypted_message = client_socket.recv(1024).decode('utf-8')
                if not encrypted_message:
                    break
                
                # Decrypt and print message
                decrypted_message = decrypt_message(cipher, encrypted_message)
                print(f"Received: {decrypted_message}")
                
                # Send encrypted response
                response = f"Server received: {decrypted_message}"
                encrypted_response = encrypt_message(cipher, response)
                client_socket.send(encrypted_response.encode('utf-8'))
                
        except Exception as e:
            print(f"Error: {e}")
        finally:
            client_socket.close()

if __name__ == "__main__":
    start_server()