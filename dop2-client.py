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
    # Конфигурация клиента
    HOST = '127.0.0.1'  # IP-адрес сервера
    PORT = 65432        # Порт, используемый сервером

    # Установка соединения через сокет
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        # Получение общего простого числа и базы от сервера
        shared_prime = int(s.recv(1024).decode('utf-8'))
        shared_base = int(s.recv(1024).decode('utf-8'))

        # Загрузка или генерация секрета клиента
        client_secret = load_key_from_file('client_secret.txt')
        if client_secret is None:
            client_secret = int(input("Введите ваш секретный ключ: "))
            save_key_to_file('client_secret.txt', client_secret)

        # Генерация и сохранение открытого ключа клиента
        client_public_key = (shared_base ** client_secret) % shared_prime
        save_key_to_file('client_public_key.txt', client_public_key)

        # Отправка открытого ключа клиента серверу
        s.sendall(bytes(str(client_public_key), 'utf-8'))

        # Получение открытого ключа сервера
        server_public_key = int(s.recv(1024).decode('utf-8'))

        # Вычисление общего секрета
        shared_secret = (server_public_key ** client_secret) % shared_prime

        print("Общий секрет вычислен:", shared_secret)

if __name__ == "__main__":
    main()
