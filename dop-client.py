#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import socket
import os

def save_key_to_file(filename, key):
    with open(filename, 'w') as file:
        file.write(str(key))

def load_key_from_file(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return int(file.read())
    return None

def main():
    HOST = '127.0.0.1'
    PORT_ENCRYPTION = 65432 
    PORT_COMMUNICATION = 65433

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_encrypt:
        s_encrypt.connect((HOST, PORT_ENCRYPTION))

        shared_prime = int(s_encrypt.recv(1024).decode('utf-8'))
        shared_base = int(s_encrypt.recv(1024).decode('utf-8'))

        client_secret = load_key_from_file('client_secret.txt')
        if client_secret is None:
            client_secret = int(input("Enter your secret key: "))
            save_key_to_file('client_secret.txt', client_secret)

        client_public_key = (shared_base ** client_secret) % shared_prime
        save_key_to_file('client_public_key.txt', client_public_key)

        s_encrypt.sendall(bytes(str(client_public_key), 'utf-8'))

        server_public_key = int(s_encrypt.recv(1024).decode('utf-8'))

        shared_secret = (server_public_key ** client_secret) % shared_prime

        print("Shared secret for encryption:", shared_secret)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_communication:
            s_communication.connect((HOST, PORT_COMMUNICATION))

            while True:
                message = input("Введите сообщение: ")
                s_communication.sendall(bytes(message, 'utf-8'))
                if message.lower() == "exit":
                    break

            s_communication.shutdown(socket.SHUT_RDWR)

if __name__ == "__main__":
    main()


