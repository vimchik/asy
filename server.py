#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import socket
from math import sqrt
from secrets import choice

def is_prime(number: int) -> bool:
    # Проверяет, является ли переданное число простым
    if number == 2 or number == 3:
        return True
    elif number % 2 == 0 or number < 2:
        return False
    for current_number in range(3, int(sqrt(number)) + 1, 2):
        if number % current_number == 0:
            return False
    return True

def generate_prime_number(min_value=0, max_value=300):
    # Генерация случайного простого числа
    primes = [number for number in range(min_value, max_value) if is_prime(number)]
    return choice(primes)

def generate_public_key(base, secret, prime):
    # Генерация открытого ключа
    return (base ** secret) % prime

def calculate_shared_secret(public_key, secret, prime):
    # Вычисление общего секрета
    return (public_key ** secret) % prime

def save_exchange(p, g, a, b, A, B, a_s, b_s, path="exchange.txt"):
    # Сохранение деталей обмена
    exchange = "Начало обмена\n\n"
    exchange += f"Сначала были сгенерированы общее простое число (p) и общая база (g):\n\tp = {p}\n\tg = {g}\n\n"
    exchange += f"Затем Алиса и Боб сгенерировали свои собственные секреты (a и b соответственно):\n\ta = {a}\n\tb = {b}\n\n"
    exchange += f"Алиса и Боб теперь вычисляют свои открытые ключи и отправляют их друг другу.\nОни представлены как A и B соответственно:\n\tA = g^a mod p = {A}\n\tB = g^b mod p = {B}\n\n"
    exchange += f"Теперь Алиса и Боб могут вычислить общий секрет, который можно использовать для шифрования последующих передач данных:\n\tВычисление Алисы:\n\t\ts = B^a mod p = {a_s} \n\tВычисление Боба:\n\t\ts = A^b mod p = {b_s}"

    with open(path, "w+") as output_file:
        output_file.write(exchange)

    return exchange

def main():
    # Конфигурация сервера
    HOST = '127.0.0.1'
    PORT = 65432

    # Установка соединения
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        # Принятие входящего подключения
        conn, addr = s.accept()
        with conn:
            print('Подключение установлено с', addr)

            # Генерация общего простого числа и базы
            shared_prime = generate_prime_number()
            shared_base =  int(choice(range(2, 20)))  # Выбор случайной базы для простоты

            # Генерация секрета сервера
            server_secret = int(choice(range(2, shared_prime - 1)))

            # Отправка общего простого числа и базы клиенту
            conn.sendall(bytes(str(shared_prime), 'utf-8'))
            conn.sendall(bytes(str(shared_base), 'utf-8'))

            # Прием открытого ключа клиента
            client_public_key = int(conn.recv(1024).decode('utf-8'))

            # Генерация открытого ключа сервера
            server_public_key = generate_public_key(shared_base, server_secret, shared_prime)

            # Отправка открытого ключа сервера клиенту
            conn.sendall(bytes(str(server_public_key), 'utf-8'))

            # Вычисление общего секрета
            shared_secret = calculate_shared_secret(client_public_key, server_secret, shared_prime)

            # Сохранение деталей обмена
            save_exchange(shared_prime, shared_base, server_secret, 0, server_public_key, 0, shared_secret, 0)

            print("Общий секрет вычислен:", shared_secret)

if __name__ == "__main__":
    main()



