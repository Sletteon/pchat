# -*- coding: utf-8 -*-
import socket
import select
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 2:
	print "Így használd: <szkript> IP-cím"
	exit()
IP_address = str(sys.argv[1])
#Port = int(sys.argv[2])
Port = 5000
server.connect((IP_address, Port))

while True:
	sockets_list = [sys.stdin, server]
	
	read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])
	
	for socks in read_sockets:
		if socks == server:
			message = socks.recv(2048)
			print message
		else:
			sys.stdout.write("<Te>")
			message = sys.stdin.readline()
			server.send(message)
			sys.stdout.write(message)
			sys.stdout.flush()
server.close()

