# -*- coding: utf-8 -*-
import socket
import select
import sys
from thread import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if len(sys.argv) != 3:
	print "Használat: Így használd: <szkript> IP-cím Port"
	exit()

IP_address = str(sys.argv[1])

Port = int(sys.argv[2])

server.bind((IP_address, Port))

server.listen(100)

list_of_clients = []
print ("Szerver elindult")

def clientthread(conn, addr):

	conn.send("""
       .__          __          
______ |  |  __ ___/  |_  ____  
\____ \|  | |  |  \   __\/  _ \ 
|  |_> >  |_|  |  /|  | (  <_> )
|   __/|____/____/ |__|  \____/ 
|__|                            
Üdvözöllek, """ + str(addr[0]))

	while True:
			try:
				message = conn.recv(2048)
				if message:

					print "<" + addr[0] + "> " + message

					message_to_send = "<" + addr[0] + "> " + message
					broadcast(message_to_send, conn)

				else:
					remove(conn)
					
			except:
				continue
				broadcast(str(addr[0]) + ' kilépett.', conn)

def broadcast(message, connection):
	for clients in list_of_clients:
		if clients!=connection:
			try:
				clients.send(message)
			except:
				clients.close()

				remove(clients)

def remove(connection):
	if connection in list_of_clients:
		list_of_clients.remove(connection)

while True:

	conn, addr = server.accept()
	list_of_clients.append(conn)

	print addr[0] + " csatlakozott"

	start_new_thread(clientthread,(conn,addr)) 

conn.close()
server.close()
