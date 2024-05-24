#!/usr/bin/env python
# coding: utf-8

# In[ ]:

# server.py

import socket
from math import sqrt
from secrets import choice
import os

def is_prime(number: int) -> bool:
    if number == 2 or number == 3:
        return True
    elif number % 2 == 0 or number < 2:
        return False
    for current_number in range(3, int(sqrt(number)) + 1, 2):
        if number % current_number == 0:
            return False
    return True

def generate_prime_number(min_value=0, max_value=300):
    primes = [number for number in range(min_value, max_value) if is_prime(number)]
    return choice(primes)

def generate_public_key(base, secret, prime):
    return (base ** secret) % prime

def calculate_shared_secret(public_key, secret, prime):
    return (public_key ** secret) % prime

def save_key_to_file(filename, key):
    with open(filename, 'w') as file:
        file.write(str(key))

def load_key_from_file(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return int(file.read())
    return None

def save_exchange(p, g, a, b, A, B, a_s, b_s, path="exchange.txt"):
    exchange = "Exchange Details:\n\n"
    exchange += f"Shared Prime (p): {p}\nShared Base (g): {g}\n\n"
    exchange += f"Server's Secret (a): {a}\nClient's Secret (b): {b}\n\n"
    exchange += f"Server's Public Key (A): {A}\nClient's Public Key (B): {B}\n\n"
    exchange += f"Shared Secret (a_s, b_s): {a_s}\n\n"

    with open(path, "w+") as output_file:
        output_file.write(exchange)

    return exchange

def get_available_port(start_port, end_port):
    for port in range(start_port, end_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            result = s.connect_ex(('127.0.0.1', port))
            if result != 0:
                return port
    return None

def main():
    HOST = '127.0.0.1'
    PORT_ENCRYPTION = get_available_port(65432, 65500)
    PORT_COMMUNICATION = get_available_port(65433, 65500)

    if PORT_ENCRYPTION is None or PORT_COMMUNICATION is None:
        print("Нет доступных портов.")
        return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_encrypt:
        s_encrypt.bind((HOST, PORT_ENCRYPTION))
        s_encrypt.listen()

        conn_encrypt, addr_encrypt = s_encrypt.accept()
        with conn_encrypt:
            print('Установлено приватное соединение с', addr_encrypt)

            shared_prime = generate_prime_number()
            shared_base = int(choice(range(2, 20)))

            server_secret = load_key_from_file('server_secret.txt')
            if server_secret is None:
                server_secret = int(choice(range(2, shared_prime - 1)))
                save_key_to_file('server_secret.txt', server_secret)

            conn_encrypt.sendall(bytes(str(shared_prime), 'utf-8'))
            conn_encrypt.sendall(bytes(str(shared_base), 'utf-8'))

            client_public_key = int(conn_encrypt.recv(1024).decode('utf-8'))

            allowed_keys = ['client_public_key.txt']

            if any(client_public_key == load_key_from_file(key_file) for key_file in allowed_keys):
                print("Публичный ключ клиента подходит для работы.")

                server_public_key = generate_public_key(shared_base, server_secret, shared_prime)
                save_key_to_file('server_public_key.txt', server_public_key)

                conn_encrypt.sendall(bytes(str(server_public_key), 'utf-8'))

                shared_secret = calculate_shared_secret(client_public_key, server_secret, shared_prime)
                print("Общий секрет:", shared_secret)

                save_exchange(shared_prime, shared_base, server_secret, 0, server_public_key, 0, shared_secret, 0)

                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_communication:
                    s_communication.bind((HOST, PORT_COMMUNICATION))
                    s_communication.listen()

                    while True:
                        conn_communication, addr_communication = s_communication.accept()
                        with conn_communication:
                            print('Установлено коммуникационное соединение с', addr_communication)
                            while True:
                                data = conn_communication.recv(1024)
                                if not data:
                                    break
                                conn_communication.sendall(data)
            else:
                print("Публичный ключ клиента не подходит для работы.")

if __name__ == "__main__":
    main()

