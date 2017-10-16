# -*- coding: utf-8 -*-
import socket
import select
import sys
from thread import *
import time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
## Régi, paraméteres ip, portlekérés
#if len(sys.argv) != 3:
#	print "Így használd: <szkript> IP-cím Port"
#	exit()
#
#IP_address = str(sys.argv[1])
#
#Port = int(sys.argv[2])
## raw_inputos ip lekérés
#IP_address = str(raw_input('Ez a szerver IP címe:'))
## google-re csatlakozás, ennek a socketnek a hostname-jét kéri le 
IP_socket= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
IP_socket.connect(('google.com', 0))
IP_address = IP_socket.getsockname()[0]
print ('Szerver IP-címe: ' + IP_address)

Port = raw_input('Port: (alapértelmezett:5000) ')
if Port == '':
	Port = 5000

server.bind((IP_address,int(Port)))

server.listen(100)

list_of_clients = []
print ("Szerver elindult\n")

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

				print ("<" + addr[0] + "> " + message)

				message_to_send = "<" + addr[0] + "> " + message
				broadcast(message_to_send, conn)
	
			else:
				remove(conn)
			time.sleep(0.2)
						
		except:
			continue
					
def broadcast(message, connection):
	for clients in list_of_clients:
		if clients!=connection:
			try:
				clients.send(message+'\n')
			except:
				clients.close()

				remove(clients)

def remove(connection):
	if connection in list_of_clients:
		list_of_clients.remove(connection)
		quitstring = str(addr[0]) + ' kilépett.'
		broadcast(quitstring, conn)
		print (quitstring+'\n')

try:
	while True:
	
		conn, addr = server.accept()
		list_of_clients.append(conn)
	
		connectedstring = str(addr[0]) + " csatlakozott"
		broadcast(connectedstring, conn)
		print (connectedstring+'\n') 
	
		start_new_thread(clientthread,(conn,addr)) 
		time.sleep(0.2) # 0,1 másodpercig várakozik, hogy csökkentse a CPU-használatot
	
except KeyboardInterrupt:
	conn.close()
	server.close()

