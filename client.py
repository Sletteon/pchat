# -*- coding: utf-8 -*-
# importok
import socket
import select
import sys
import time
import errno
# server socket (objektum) létrehozása
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Ip-cím lekérése
IP_address = raw_input('Szerver IP címe: ')
# Port lekérése, ha nem adott meg semmit a felhasználó, akkor legyen 5000
Port = raw_input('Szerver port: (alapértelmezett:5000)')
if Port == '':
	Port = 5000
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

				print (message)
			else:
				sys.stdout.write("<Te>")
				message = sys.stdin.readline()
				server.send(message)
				sys.stdout.write(message)
				sys.stdout.flush()
	except KeyboardInterrupt:
		exit()
	time.sleep(0.2)
server.close()

