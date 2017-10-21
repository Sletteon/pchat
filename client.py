# -*- coding: utf-8 -*-
# importok
import socket
import re
import select
import sys
import time
import errno
from AESCipher import AESCipher
# server socket (objektum) létrehozása
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Ip-cím lekérése
IP_address = raw_input('Szerver IP címe: ')
# Port lekérése, ha nem adott meg semmit a felhasználó, akkor legyen 5000
Port = raw_input('Szerver port: (alapértelmezett:5000)')
if Port == '':
	Port = 5000

Key = raw_input('Kulcs: ')
aes = AESCipher(Key)
# Ha a felhasználó rossz IP-címet adott meg,
# vagy nem fut a szerver azon az IP-n
# beszéljen vissza
try:		
	server.connect((IP_address, Port))
except socket.error, v:
    errorcode=v[0]
    if errorcode==errno.ECONNREFUSED:
        print "Kapcsolat elutasítva." 
	exit()

# Egyetlen while loop,i
# figyeljen, hogy mikor a szervertől
# üzenet érkezik, írja ki azt.
# Valamint a felhasználótól kérje el az üzenetet.
# TODO: stdin.readline() kiírja a küldendő szöveget,
# valamint a szervertől érkező üzenet (amit az elöbb kértünk be)
# is látszódik. Tehát kétszer látszódik a message.
char1 = '<'
char2 = '>' 
while True:
	try:
		sockets_list = [sys.stdin, server]
		
		read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])
		
		for socks in read_sockets:
			if socks == server:
				try:
					message = socks.recv(2048)
				except socket.error, v:
					errorcode=v[0]
					if errorcode==errno.ENOTCONN:
						print("Hibás IP-cím")
						exit()

				ipsubstr = message[message.find(char1)+1 : message.find(char2)]
				noipmess = re.sub('<.*?>', '', message)
				noipmess.strip(' ')
				if ' ' not in noipmess:
					try:
						decrmes = aes.decrypt(noipmess)
					except ValueError:
						print('A szerver bezárt.')
						exit()
					print ('<' + ipsubstr +'>: '+ decrmes)
				else:
					print (message)
			else:
				message = sys.stdin.readline()
				encrmes = aes.encrypt(message)
				server.send(encrmes)
				sys.stdout.write('<Te>: ' + encrmes + '\n\n')
				sys.stdout.flush()
	except KeyboardInterrupt:
		exit()
	time.sleep(0.2)
server.close()

