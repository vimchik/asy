#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import asyncio

async def main():
    HOST = '127.0.0.1'
    PORT = 65432

    reader, writer = await asyncio.open_connection(HOST, PORT)

    # Получение общего простого числа и базы от сервера
    shared_prime = int(await reader.readline())
    shared_base = int(await reader.readline())

    # Вывод общего простого числа и базы для отладки
    print("Общее простое число:", shared_prime)
    print("Общая база:", shared_base)

    # Получение секретного ключа от пользователя
    client_secret = input("Введите ваш секретный ключ: ")

    # Генерация открытого ключа клиента
    client_public_key = (shared_base ** int(client_secret)) % shared_prime

    # Отправка открытого ключа клиента на сервер
    writer.write(f"{client_public_key}\n".encode())
    await writer.drain()

    # Получение открытого ключа сервера
    server_public_key = int(await reader.readline())

    # Вычисление общего секрета
    shared_secret = (server_public_key ** int(client_secret)) % shared_prime

    print("Вычислен общий секрет:", shared_secret)

    # Закрытие соединения
    writer.close()
    await writer.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())




