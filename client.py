#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import socket

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

        # Генерация секрета клиента
        client_secret = int(input("Введите ваш секретный ключ: "))

        # Генерация открытого ключа клиента
        client_public_key = (shared_base ** client_secret) % shared_prime

        # Отправка открытого ключа клиента серверу
        s.sendall(bytes(str(client_public_key), 'utf-8'))

        # Получение открытого ключа сервера
        server_public_key = int(s.recv(1024).decode('utf-8'))

        # Вычисление общего секрета
        shared_secret = (server_public_key ** client_secret) % shared_prime

        print("Общий секрет вычислен:", shared_secret)

if __name__ == "__main__":
    main()



