#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import socket
import csv
def calculation_part_key(key_publ_1, key_prim, key_publ_2):
    key_part_2 = key_publ_1 ** key_prim % key_publ_2
    return key_part_2
def calculation_full_key(key_part_1, key_prim, key_publ_2):
    key_full = key_part_1 ** key_prim % key_publ_2
    return key_full
def encoding(msg, key):
    lst = list(msg)
    for i in range(len(lst)):
        variab = ord(lst[i])+key
        variab = chr(variab)
        lst[i] = variab
    return(''.join(lst))
def decoding(msg, key):
    lst = list(msg)
    for i in range(len(lst)):
        variab = ord(lst[i]) - key
        variab = chr(variab)
        lst[i] = variab
    return(''.join(lst))
def generate(flagg, key_prim, key_publ_2):
    global flag
    while flagg < 3:
        flagg += 1
        if flagg == 1:
            key_publ_1 = int(conn.recv(1024))
            if checking(key_publ_1):
                msg = str(key_publ_2)
                conn.send(msg.encode())
            else:
                print("Ошибка")
                flag = False
                break
        if flagg == 2:
            key_part_1 = int(conn.recv(1024))
            key_part_2 = calculation_part_key(key_publ_1, key_prim, key_publ_2)
            msg = str(key_part_2)
            conn.send(msg.encode())
        if flagg == 3:
            key_full_1 = int(conn.recv(1024))
            key_full_2 = calculation_full_key(key_part_1, key_prim, key_publ_2)
            msg = str(key_full_2)
            conn.send(msg.encode())
            print(key_full_1)
            with open('keys_s.txt', 'w') as f:
                f.write(str(key_full_2))
    return key_full_2
def send_msg(conn, key_full_2):
    msg = conn.recv(1024).decode()
    decod_msg = decoding(msg, key_full_2)
    print('Сообщение клиента', decod_msg)
    msg = input('Сообщение сервера')
    encod_msg = encoding(msg, key_full_2)
    conn.send(encod_msg.encode())
    return encod_msg
def port2(conn, key_full_2, port):
    msg = conn.recv(1024).decode()
    decod_msg = decoding(msg, key_full_2)
    print('Сообщение клиента', decod_msg)
    msg_port = str(port)
    print('Сообщение', msg_port)
    encod_msg = encoding(msg_port, key_full_2)
    conn.send(encod_msg.encode())
def checking(key_publ_1):
    i = False
    with open('keys_list.csv', 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            print(line[0])
            if line[0] == str(key_publ_1):
                i = True
    return i
def bind(host_str):
    sock = socket.socket()
    for prt in range(1024, 65536):
        try:
            sock.bind((host_str, prt))
            flg = prt
            sock.close()
            return flg
        except socket.error:
            pass
flag = True
print('Сервер работает')
port = bind('localhost')
print('Порт ', port)
sock = socket.socket()
sock.bind(('', 9090))
print('Соединение')
sock.listen(3)
conn, addr = sock.accept()
print('Клиент', addr[0][1], 'присоединился')
try:
    with open('keys_s.txt', 'r') as f:
        for line in f:
            key_full_2 = int(line)
except:
    key_publ_2 = 151
    key_prim = 157
    flagg = 0
    msg = ''
    key_full_2 = generate(flagg, key_prim, key_publ_2)
if flag:
    port2(conn, key_full_2, port)
    sock.close()
    sock = socket.socket()
    sock.bind(('localhost', int(port)))
    sock.listen(1)
    conn, addr = sock.accept()
    while True:
        send_msg(conn, key_full_2)
sock.close()
print('Остановвка сервера')

