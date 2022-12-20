#!/usr/bin/env python
# coding: utf-8

# In[1]:


import socket
def сalculation_part_key(key_publ_2, key_prim, key_publ_1):
    key_part_2 = key_publ_2 ** key_prim % key_publ_1
    return key_part_2
def calculation_full_key(key_part_1, key_prim, key_publ_1):
    key_full = key_part_1 ** key_prim % key_publ_1
    return key_full
def encoding(msg, key):
    lst = list(msg)
    for i in range(len(lst)):
        variab = ord(lst[i]) + key
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
def generation(flagg, key_prim, key_publ_2):
    global flag
    while flagg < 3:
        flagg += 1
        if flagg == 1:
            msg = str(key_publ_2)
            sock.send(msg.encode())
            try:
                key_publ_1 = int(sock.recv(1024))
            except ValueError:
                print("Ошибка.")
                flag = False
                break
        if flagg == 2:
            key_part_2 = сalculation_part_key(key_publ_2, key_prim, key_publ_1)
            msg = str(key_part_2)
            sock.send(msg.encode())
            key_part_1 = int(sock.recv(1024))
        if flagg == 3:
            key_full_2 = calculation_full_key(key_part_1, key_prim, key_publ_1)
            print(key_part_1, key_prim, key_publ_1)
            msg = str(key_full_2)
            sock.send(msg.encode())
            key_full_1 = int(sock.recv(1024))
            print(key_full_1)
            with open('keys_c.txt', 'w') as f:
                f.write(str(key_full_1))
    return key_full_1
def send_msg(sock, key_full_2):
    msg = input('Сообщение ')
    encod_msg = encoding(msg, key_full_2)
    sock.send(encod_msg.encode())
    msg = sock.recv(1024).decode()
    decod_msg = decoding(msg, key_full_2)
    print('Сообщение сервера ', decod_msg)
    return decod_msg


flag = True
sock = socket.socket()
sock.setblocking(5)
sock.connect(('localhost', 9090))
print('Соединение')
try:
    with open('keys_c.txt', 'r') as f:
        for line in f:
            key_full_1 = int(line)
except:
    key_prim = 199
    key_publ_2 = 197
    flagg = 0
    msg = ''
    key_full_1 = generation(flagg, key_prim, key_publ_2)

if flag:
    port = send_msg(sock, key_full_1)
    sock.close()
    sock = socket.socket()
    sock.connect(('localhost', 1024))
    while True:
        send_msg(sock, key_full_1)
sock.close()
print('Разрыв соединения')


# In[ ]:




