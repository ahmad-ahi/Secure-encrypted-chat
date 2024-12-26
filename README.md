1. Title of the Project
A Secure LAN Chat Application with Encryption
2. Project Description
Secure LAN Chat will be a simple local area network (LAN) chat application that allows
users to communicate securely with each other. The application will have encryption to
make sure that messages sent between clients are secure and that users cannot pretend
they are one another.
3. Design Outline
Client-Server Model: The application will be built on a client-server architecture, where a
single server manages multiple clients. The server handles incoming connections and
broadcasts messages to all connected clients.
Server: Responsible for accepting connections from clients, decrypting incoming
messages, and broadcasting messages to all clients after encryption.
Client: Connects to the server, sends messages, and receives messages from other users.
Each client can encrypt messages before sending and decrypt incoming messages.
Socket, Pycryptdome and Cryptography libraries will be used
Asymmetric Encryption (RSA) is used first for secure key exchange and Fernet is used for
the actual message encryption during the chat.
The server will generate an RSA key when it starts, and the public key is shared with all
clients when they are connected. When the client connects, the server will generate a
personal key which is called a Fernet Key. The client receives the encrypted key and uses
its RSA private key to decrypt it which establishes the connection. Once the connection is
established through the symmetric key, all the communication between the server and
client is encrypted.
