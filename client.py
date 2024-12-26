import socket
import threading
from tkinter import Tk, Text, Entry, Button, Scrollbar, END
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from cryptography.fernet import Fernet
#https://github.com/SunilRavi7/GUI_Chat_Application
# https://pycryptodome.readthedocs.io/en/latest/src/installation.html

class Client:
    #this should work on most devices but if not, it should be changed to your ip addr host = "your ip"
    def __init__(self, host='127.0.0.1', port=12000):
        # Create a socket to connect to the server.
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
##https://github.com/SyedArsalan798/client-server_python-tkinter/blob/master/ServerTk.py
#https://github.com/git-haan/Tkinter-Chat-App
# Receive the server's public key for encryption
        public_key_data = self.client.recv(1024)
        self.public_key = RSA.import_key(public_key_data)
        
# it generates a Fernet symmetric encryption key
        self.fernet_key = Fernet.generate_key()
        
# encrypt the Fernet key using the server's public key (RSA encryption)
        cipher = PKCS1_OAEP.new(self.public_key)
        encrypted_key = cipher.encrypt(self.fernet_key)
        self.client.send(encrypted_key)

        # ask the user for their username and send it to the server.
        self.username = input(self.client.recv(1024).decode())
        self.client.send(self.username.encode())

        #
        self.gui_running = False
        self.init_gui()

    #Tkinter run
    def init_gui(self):
        self.root = Tk()
        self.root.title(f"Chat - {self.username}")

        # displaying messg.
        self.chat = Text(self.root, state="disabled", wrap="word", height=20, width=50)
        self.chat.pack(padx=10, pady=10)

        # scrollbar.
        scroll = Scrollbar(self.root, command=self.chat.yview)
        self.chat.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")

        #write down messg
        self.input_field = Entry(self.root, width=40)
        self.input_field.pack(padx=10, pady=5, side="left")

        # Send
        button = Button(self.root, text="Send", command=self.send_message)
        button.pack(pady=5, side="right")

        self.gui_running = True

    def receive_messages(self):
#recieve and decrpyt messages
        while self.gui_running:
            try:
                message = self.client.recv(1024)
                if message:
                    decr = Fernet(self.fernet_key).decrypt(message).decode()
                    self.display_message(decr)
            except Exception as e:
                self.display_message(f"Error: {e}")
                break

    def send_message(self):
#fernet key encrypt
        message = self.input_field.get()
        if message:
            try:
                encrypted_message = Fernet(self.fernet_key).encrypt(message.encode())
                self.client.send(encrypted_message)
                self.input_field.delete(0, END)
            except Exception as e:
                self.display_message(f"Error: {e}")

    def display_message(self, message):
        #for displaying the message
        self.chat.configure(state="normal")
        self.chat.insert(END, message + "\n")
        self.chat.configure(state="disabled")
        self.chat.see(END)

    def run(self):
#start the thread for messages
        threading.Thread(target=self.receive_messages, daemon=True).start()
        
        # tkinter is running
        self.root.mainloop()
        self.gui_running = False

if __name__ == "__main__":
    client = Client()
    client.run()
