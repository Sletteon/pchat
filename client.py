# -*- coding: utf-8 -*-
import socket
import select
import sys
import time
import errno

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#if len(sys.argv) != 3:
#	print "Így használd: <szkript> IP-cím, Port"
#	exit()
#IP_address = str(sys.argv[1])
#Port = int(sys.argv[2])
IP_address = raw_input('Szerver IP címe: ')
Port = raw_input('Szerver port: (alapértelmezett:5000)')
if Port == '':
	Port = 5000
try:		
	server.connect((IP_address, Port))
except socket.error, v:
    errorcode=v[0]
    if errorcode==errno.ECONNREFUSED:
        print "Kapcsolat elutasítva." 
	exit()

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

