import socket
import threading
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from cryptography.fernet import Fernet

#also used the code we did in class
#https://github.com/SyedArsalan798/client-server_python-tkinter/blob/master/ServerTk.py
# https://realpython.com/python-sockets/
# https://www.geeksforgeeks.org/socket-programming-python/
# https://realpython.com/intro-to-python-threading/
# https://www.geeksforgeeks.org/multithreading-python-set-1/

class server:
    def __init__(self, host='0.0.0.0', port=12000):
# TCP protocol, it uses the sock_stream
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        
 #maximum of 5 pending connections
        self.server.listen(5)
        self.clients = {}
        
        # Generate RSA key pair 
        # (2048-bit) for asymmetric encryption
        # The private key is used for decryption, and the public key is shared with clients
        self.rsa_key = RSA.generate(2048)
        self.public_key = self.rsa_key.publickey()
        print("server start and waiting for connections from anyon")
#https://www.geeksforgeeks.org/socket-programming-python/
    def broadcast(self, message, sender_socket=None):
        # Send a message to all clients
        for client_socet in list(self.clients.keys()):
            if client_socet != sender_socket:
                try:
 # encrypt the message using the client's Fernet key before sending
                    encrypted_message = self.clients[client_socet][0].encrypt(message.encode())
                    client_socet.send(encrypted_message)
                except Exception:
# If the client is disconnected, remove them
                    self.disconnect_client(client_socet)

    def disconnect_client(self, client_socet):
# disconnect a client from the server
        if client_socet in self.clients:
            username = self.clients[client_socet][1]
            print(f"{username} disconnected.")
            del self.clients[client_socet]
            client_socet.close()
            self.broadcast(f"{username} has left the chat, they wont see ur message.")

    def client_handler(self, client_socet, address):
        try:
#send a the server's public key to the client for encryption
            client_socet.send(self.public_key.export_key())
            
# receive the encrypted Fernet key from the client and decrypt it using the server's private key
            encrypted_key = client_socet.recv(256)
            cipher = PKCS1_OAEP.new(self.rsa_key)
            fernet_key = cipher.decrypt(encrypted_key)
#ask them to enter name
            client_socet.send("Enter your username: ".encode())
            username = client_socet.recv(1024).decode()
            self.clients[client_socet] = (Fernet(fernet_key), username)
            print(f"{username} connected from {address}.")
            self.broadcast(f"{username} has joined the chat.")

            while True:
#receive and broadcast messages
                message = client_socet.recv(1024)
                if message:
#decrypt the received message using the client's Fernet key
                    decrypted_message = self.clients[client_socet][0].decrypt(message).decode()
                    broadcast_message = f"{username}: {decrypted_message}"
                    print(broadcast_message)
                    self.broadcast(broadcast_message, sender_socket=client_socet)
        except Exception as e:
            print(f"Error with client {address}: {e}")
        finally:
# disconnect the client in case of an error or when the client disconnects
            self.disconnect_client(client_socet)

    def run(self):
 # accept connections from clients
        while True:
            client_socet, addr = self.server.accept()
            threading.Thread(target=self.client_handler, args=(client_socet, addr)).start()

if __name__ == "__main__":
    server = server()
    server.run()
